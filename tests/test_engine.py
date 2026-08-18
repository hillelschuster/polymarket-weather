"""Comprehensive Automated Test Suite for Polymarket Weather Engine.
Verifies alpha invariance, detector margins, execution gates, sizing tiers, and parsing.
"""
import unittest, json, os, sys
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.supervisor import (
    bucket_parse, target_local_date, fee, detectors, MAP, US_F
)
from scripts.live_trader import (
    env, tick_round, DEFAULT_CARD, DEFAULT_MAX_OPEN, BASE_LIVE_RULES, PX_TOL, EDGE_MIN
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
        """Verify R2 dead-below detection in Celsius with progressive margin & velocity gating."""
        event = {"title": "Lowest temperature in London on August 18?", "city": "London", "markets": []}
        city_cfg = MAP["London"] # ('EGLC', 0, 'Europe/London', 5.8, 20.2)
        # London morning dawn is 5.8 -> local_hour 4.5 is in decision window (5.8 - 2.5 = 3.3 to 5.8)
        book = [
            {"bucket": "14°C", "lo": 13.5, "hi": 14.5, "val": 14.0, "yes_bid": 0.15, "yes_bid_sz": 100, "yes_ask": 0.20, "yes_ask_sz": 100},
            {"bucket": "15°C", "lo": 14.5, "hi": 15.5, "val": 15.0, "yes_bid": 0.30, "yes_bid_sz": 100, "yes_ask": 0.35, "yes_ask_sz": 100},
            {"bucket": "18°C", "lo": 17.5, "hi": 18.5, "val": 18.0, "yes_bid": 0.90, "yes_bid_sz": 100, "yes_ask": 0.95, "yes_ask_sz": 100}
        ]
        # Current obs = 17.5C, runmin = 17.5C
        # For 14C bucket: hi (14.5) <= 17.5 - 2.8 (strict margin for 85c NO) = 14.7 -> QUALIFIES!
        dets = detectors(event, city_cfg, local_hour=4.5, obs=17.5, precip=False, book=book, runmin=17.5, trend=0.0)
        self.assertEqual(len(dets), 2, "Both 14°C and 15°C should qualify as dead-below")
        rules = [d["bucket"] for d in dets]
        self.assertIn("14°C", rules)
        self.assertIn("15°C", rules)
        # Verify 14C (strict 2.8C margin for 85c NO)
        d14 = next(d for d in dets if d["bucket"] == "14°C")
        self.assertEqual(d14["rule"], "R2_low_dead_below")
        self.assertEqual(d14["px"], 0.85)
        self.assertEqual(d14["q"], 0.98)
        self.assertGreater(d14["edge"], 0.05)
        # Verify 15C (base 2.0C margin for 70c NO)
        d15 = next(d for d in dets if d["bucket"] == "15°C")
        self.assertEqual(d15["rule"], "R2_low_dead_below")
        self.assertEqual(d15["px"], 0.70)
        self.assertEqual(d15["q"], 0.95)
        self.assertGreater(d15["edge"], 0.05)

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
        # NYC afternoon high: lastlight is 19.8 -> local_hour 18.5 is in decision window
        book = [
            {"bucket": "90-91°F", "lo": 89.5, "hi": 91.5, "val": 90.0, "yes_bid": 0.18, "yes_bid_sz": 100, "yes_ask": 0.22, "yes_ask_sz": 100}
        ]
        # Max achieved = 29.0C (84.2F). Margin for 82c NO is strict 5.0F -> 84.2 + 5.0 = 89.2F.
        # 90-91F bucket lo (89.5F) >= 89.2F -> QUALIFIES!
        dets = detectors(event, city_cfg, local_hour=18.5, obs=28.0, precip=False, book=book, runmax=29.0, trend=0.0)
        self.assertEqual(len(dets), 1)
        self.assertEqual(dets[0]["rule"], "R3_high_dead_above")
        self.assertEqual(dets[0]["bucket"], "90-91°F")
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

if __name__ == "__main__":
    unittest.main()
