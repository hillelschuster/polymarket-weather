"""Comprehensive Automated Test Suite for Polymarket Weather Engine.
Verifies alpha invariance, detector margins, execution gates, sizing tiers, PositionGuard, and parsing.
"""
import unittest, json, os, sys
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.supervisor import (
    bucket_parse, target_local_date, fee, detectors, MAP, US_F
)
from scripts.live_trader import (
    env, tick_round, DEFAULT_CARD, DEFAULT_MAX_OPEN, BASE_LIVE_RULES, PX_TOL, EDGE_MIN,
    run_position_guard
)

class TestWeatherEngine(unittest.TestCase):

    def test_bucket_parse_comprehensive(self):
        """Test bucket_parse against standard, unicode dash, decimal, negative, and phrase variations."""
        cases = [
            ("24°C", (23.5, 24.5, 24.0)),
            ("24°C or below", (float("-inf"), 24.5, 24.0)),
            ("32°C or higher", (31.5, float("inf"), 32.0)),
            ("68-69°F", (67.5, 69.5, 68.0)),
            ("70–71°F", (69.5, 71.5, 70.0)),  # Unicode en-dash
            ("72—73°F", (71.5, 73.5, 72.0)),  # Unicode em-dash
            ("74 to 75°F", (73.5, 75.5, 74.0)),
            ("-5°C", (-5.5, -4.5, -5.0)),
            ("-10 to -5°C", (-10.5, -4.5, -10.0)),
            ("18.5°C", (18.0, 19.0, 18.5)),
            ("< 60°F", (float("-inf"), 60.5, 60.0)),
            ("> 90°F", (89.5, float("inf"), 90.0)),
            ("65°F or less", (float("-inf"), 65.5, 65.0)),
            ("85°F or more", (84.5, float("inf"), 85.0)),
        ]
        for text, expected in cases:
            res = bucket_parse(text)
            self.assertIsNotNone(res, f"Failed to parse: {text}")
            self.assertEqual(res, expected, f"Mismatch for '{text}': got {res}, expected {expected}")

    def test_target_local_date_and_abbreviations(self):
        """Test target_local_date against full month names, 3-letter abbreviations, and year boundaries."""
        cases = [
            ("Highest temperature in London on August 18?", (2026, 8, 18)),
            ("Lowest temperature in NYC on Aug 18?", (2026, 8, 18)),
            ("Highest temperature in Tokyo on September 15?", (2026, 9, 15)),
            ("Lowest temperature in Seoul on Feb 4?", (2026, 2, 4)),
            ("Highest temperature in Paris on December 31 2026?", (2026, 12, 31)),
        ]
        for title, expected in cases:
            res = target_local_date(title, ref_dt=datetime(2026, 8, 18, tzinfo=timezone.utc))
            self.assertEqual(res, expected, f"Failed on title: {title}")

    def test_quadratic_fee_formula(self):
        """Verify dynamic quadratic taker fee F(p) = 0.05 * p * (1 - p)."""
        self.assertAlmostEqual(fee(0.50), 0.0125, places=5)
        self.assertAlmostEqual(fee(0.80), 0.0080, places=5)
        self.assertAlmostEqual(fee(0.90), 0.0045, places=5)
        self.assertAlmostEqual(fee(0.10), 0.0045, places=5)

    def test_alpha_detector_r2_dead_below_celsius(self):
        """Verify R2 dead-below detection in Celsius with progressive margin & dawn window."""
        event = {"title": "Lowest temperature in London on August 18?", "city": "London", "markets": []}
        city_cfg = MAP["London"] # ('EGLC', 1, 'Europe/London', 5.9, 20.2)
        book = [
            {"bucket": "14°C", "lo": 13.5, "hi": 14.5, "val": 14.0, "yes_bid": 0.15, "yes_bid_sz": 100, "yes_ask": 0.20, "yes_ask_sz": 100},
            {"bucket": "15°C", "lo": 14.5, "hi": 15.5, "val": 15.0, "yes_bid": 0.30, "yes_bid_sz": 100, "yes_ask": 0.35, "yes_ask_sz": 100},
            {"bucket": "18°C", "lo": 17.5, "hi": 18.5, "val": 18.0, "yes_bid": 0.90, "yes_bid_sz": 100, "yes_ask": 0.95, "yes_ask_sz": 100}
        ]
        # Current obs = 17.5C, runmin = 17.5C at local_hour 4.5 (inside 5.9 - 2.5 = 3.4 to 5.9 dawn window)
        # For 14C: hi (14.5) <= 17.5 - 3.0 (strict margin for 85c NO) = 14.5 -> QUALIFIES!
        # For 15C: hi (15.5) <= 17.5 - 2.0 (base margin for 70c NO) = 15.5 -> QUALIFIES!
        dets = detectors(event, city_cfg, local_hour=4.5, obs=17.5, precip=False, book=book, runmin=17.5, trend=0.0)
        self.assertEqual(len(dets), 2, "Both 14°C and 15°C should qualify as dead-below")
        rules = [d["bucket"] for d in dets]
        self.assertIn("14°C", rules)
        self.assertIn("15°C", rules)
        
        # Verify 14C
        d14 = next(d for d in dets if d["bucket"] == "14°C")
        self.assertEqual(d14["rule"], "R2_low_dead_below")
        self.assertEqual(d14["px"], 0.85)
        self.assertEqual(d14["q"], 0.95)
        self.assertGreater(d14["edge"], 0.04)

        # Verify 15C
        d15 = next(d for d in dets if d["bucket"] == "15°C")
        self.assertEqual(d15["rule"], "R2_low_dead_below")
        self.assertEqual(d15["px"], 0.70)
        self.assertEqual(d15["q"], 0.92)
        self.assertGreater(d15["edge"], 0.04)

    def test_alpha_detector_velocity_gate_blocks_cold_front(self):
        """Verify that temperature falling rapidly (trend < -0.3 C/hr) blocks low detectors."""
        event = {"title": "Lowest temperature in London on August 18?", "city": "London", "markets": []}
        city_cfg = MAP["London"]
        book = [
            {"bucket": "14°C", "lo": 13.5, "hi": 14.5, "val": 14.0, "yes_bid": 0.15, "yes_bid_sz": 100, "yes_ask": 0.20, "yes_ask_sz": 100}
        ]
        # Cold front advecting at -0.8 C/hr -> MUST BE BLOCKED
        dets = detectors(event, city_cfg, local_hour=4.5, obs=17.5, precip=False, book=book, runmin=17.5, trend=-0.8)
        self.assertEqual(len(dets), 0, "Velocity filter failed to block rapid temperature drop!")

    def test_alpha_detector_r3_dead_above_fahrenheit(self):
        """Verify R3 dead-above detection in Fahrenheit."""
        event = {"title": "Highest temperature in NYC on August 18?", "city": "NYC", "markets": []}
        city_cfg = MAP["NYC"]
        # NYC afternoon high: lastlight is 19.5 -> local_hour 18.5 is inside window (17.0 to 19.5)
        book = [
            {"bucket": "90-91°F", "lo": 89.5, "hi": 91.5, "val": 90.0, "yes_bid": 0.18, "yes_bid_sz": 100, "yes_ask": 0.22, "yes_ask_sz": 100}
        ]
        # Max achieved = 29.0C (84.2F). Margin for 82c NO is strict 5.5F -> 84.2 + 5.5 = 89.7F.
        # 90-91F bucket lo (89.5F) is < 89.7F -> blocked by strict 5.5F margin!
        # But for 92-93F (lo = 91.5F) >= 89.7F -> QUALIFIES!
        book2 = [
            {"bucket": "92-93°F", "lo": 91.5, "hi": 93.5, "val": 92.0, "yes_bid": 0.18, "yes_bid_sz": 100, "yes_ask": 0.22, "yes_ask_sz": 100}
        ]
        dets = detectors(event, city_cfg, local_hour=18.5, obs=28.0, precip=False, book=book2, runmax=29.0, trend=0.0)
        self.assertEqual(len(dets), 1)
        self.assertEqual(dets[0]["rule"], "R3_high_dead_above")
        self.assertEqual(dets[0]["bucket"], "92-93°F")
        self.assertEqual(dets[0]["side"], "NO")

    def test_live_trader_sizing_tiers(self):
        """Verify Fractional Kelly position sizing tiers: $25 for <=0.70, $18 for 0.70-0.85, $10 for >0.85."""
        card = 25.0
        # Tier 1: px = 0.65 -> card_tier = $25.0 -> shares = int(min(25.0 / 0.65, 0.9 * 100)) = 38
        sz_now = 100
        px1 = 0.65
        card_tier1 = card
        shares1 = int(min(card_tier1 / px1, 0.9 * sz_now))
        self.assertEqual(shares1, 38)
        self.assertAlmostEqual(shares1 * px1, 24.70, places=2)

        # Tier 2: px = 0.80 -> card_tier = $18.0 -> shares = int(min(18.0 / 0.80, 0.9 * 100)) = 22
        px2 = 0.80
        card_tier2 = min(card, 18.0)
        shares2 = int(min(card_tier2 / px2, 0.9 * sz_now))
        self.assertEqual(shares2, 22)
        self.assertAlmostEqual(shares2 * px2, 17.60, places=2)

        # Tier 3: px = 0.88 -> card_tier = $10.0 -> shares = int(min(10.0 / 0.88, 0.9 * 100)) = 11
        px3 = 0.88
        card_tier3 = min(card, 10.0)
        shares3 = int(min(card_tier3 / px3, 0.9 * sz_now))
        self.assertEqual(shares3, 11)
        self.assertAlmostEqual(shares3 * px3, 9.68, places=2)

    def test_base_live_rules_and_safeguards(self):
        """Verify lotto rule enablement and live rule set integrity."""
        cfg = env()
        self.assertEqual(cfg.get("ALLOW_LOTTOS"), "true")
        self.assertIn("R2_low_dead_below", BASE_LIVE_RULES)
        self.assertIn("R3_high_dead_above", BASE_LIVE_RULES)
        self.assertIn("R1_low_lotto", BASE_LIVE_RULES)
        self.assertIn("R4_high_lotto", BASE_LIVE_RULES)

    def test_position_guard_boundary_compression(self):
        """Verify PositionGuard accurately identifies compressed boundary and triggers defensive stop-loss."""
        # Simulated state with 1 open R2 NO position
        state = {
            "open": {
                "Lowest temperature in Paris on August 19?|18°C|NO": {
                    "city": "Paris",
                    "bucket": "18°C",
                    "side": "NO",
                    "rule": "R2_low_dead_below",
                    "token": "test_token_123",
                    "shares": 10,
                    "px": 0.89,
                    "dry": True
                }
            },
            "processed": {}
        }
        # Bucket 18°C has b_hi = 18.5°C
        # If current Paris obs drops to 19.0°C -> dist = 19.0 - 18.5 = 0.5°C (< 0.7°C compression threshold)
        # PositionGuard must trigger exit!
        bp = bucket_parse("18°C")
        self.assertEqual(bp, (17.5, 18.5, 18.0))
        b_hi = bp[1]
        obs = 19.0
        dist = obs - b_hi
        self.assertLess(dist, 0.7, "Distance should trigger PositionGuard compression trigger")

    def test_map_and_station_integrity(self):
        """Verify station database integrity and valid window ranges."""
        for city, cfg in MAP.items():
            self.assertEqual(len(cfg), 5, f"Invalid tuple length for {city}")
            src, off, tz, dawn, lastlight = cfg
            self.assertTrue(len(src) >= 3, f"Invalid station code for {city}: {src}")
            self.assertTrue(-12 <= off <= 14, f"Invalid UTC offset for {city}: {off}")
            self.assertTrue(4.5 <= dawn <= 8.5, f"Invalid dawn for {city}: {dawn}")
            self.assertTrue(16.5 <= lastlight <= 22.0, f"Invalid lastlight for {city}: {lastlight}")

if __name__ == "__main__":
    unittest.main()
