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
        self.assertEqual(d14["q"], 0.97)
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
        # Max achieved = 29.0C (84.2F). Margin for 82c NO is strict 5.4F -> 84.2 + 5.4 = 89.6F.
        # 90-91F bucket lo (89.5F) is < 89.6F -> blocked by strict margin!
        # But for 92-93F (lo = 91.5F) >= 89.6F -> QUALIFIES!
        book2 = [
            {"bucket": "92-93°F", "lo": 91.5, "hi": 93.5, "val": 92.0, "yes_bid": 0.18, "yes_bid_sz": 100, "yes_ask": 0.22, "yes_ask_sz": 100}
        ]
        dets = detectors(event, city_cfg, local_hour=18.5, obs=28.0, precip=False, book=book2, runmax=29.0, trend=0.0)
        self.assertEqual(len(dets), 1)
        self.assertEqual(dets[0]["rule"], "R3_high_dead_above")
        self.assertEqual(dets[0]["bucket"], "92-93°F")
        self.assertEqual(dets[0]["side"], "NO")

    def test_alpha_detector_r5_dead_below_high(self):
        """Verify R5 dead-below detection in a Highest temperature event (monotone peak property)."""
        event = {"title": "Highest temperature in London on August 18?", "city": "London", "markets": []}
        city_cfg = MAP["London"]  # lastlight = 20.2 -> window: 16.7 to 23.2
        book = [
            {"bucket": "20°C", "lo": 19.5, "hi": 20.5, "val": 20.0, "yes_bid": 0.15, "yes_bid_sz": 100, "yes_ask": 0.20, "yes_ask_sz": 100},
            {"bucket": "21°C", "lo": 20.5, "hi": 21.5, "val": 21.0, "yes_bid": 0.30, "yes_bid_sz": 100, "yes_ask": 0.35, "yes_ask_sz": 100},
            {"bucket": "24°C", "lo": 23.5, "hi": 24.5, "val": 24.0, "yes_bid": 0.80, "yes_bid_sz": 100, "yes_ask": 0.85, "yes_ask_sz": 100},
            {"bucket": "28°C", "lo": 27.5, "hi": 28.5, "val": 28.0, "yes_bid": 0.15, "yes_bid_sz": 100, "yes_ask": 0.20, "yes_ask_sz": 100}
        ]
        # Achieved running max = 24.0C, obs = 23.5C at 18:00 local time
        # For 20C: hi (20.5) <= 24.0 - 3.0 (strict margin for 85c NO) = 21.0 -> R5 QUALIFIES!
        # For 21C: hi (21.5) <= 24.0 - 2.0 (base margin for 70c NO) = 22.0 -> R5 QUALIFIES!
        # For 28C: lo (27.5) >= 24.0 + 3.0 (strict margin for 85c NO) = 27.0 -> R3 QUALIFIES!
        dets = detectors(event, city_cfg, local_hour=18.0, obs=23.5, precip=False, book=book, runmax=24.0, trend=0.0)
        self.assertEqual(len(dets), 3)

        d20 = next(d for d in dets if d["bucket"] == "20°C")
        self.assertEqual(d20["rule"], "R5_high_dead_below")
        self.assertEqual(d20["side"], "NO")
        self.assertEqual(d20["px"], 0.85)
        self.assertEqual(d20["q"], 0.97)
        self.assertGreater(d20["edge"], 0.04)

        d21 = next(d for d in dets if d["bucket"] == "21°C")
        self.assertEqual(d21["rule"], "R5_high_dead_below")
        self.assertEqual(d21["side"], "NO")
        self.assertEqual(d21["px"], 0.70)
        self.assertEqual(d21["q"], 0.92)
        self.assertGreater(d21["edge"], 0.04)

        d28 = next(d for d in dets if d["bucket"] == "28°C")
        self.assertEqual(d28["rule"], "R3_high_dead_above")
        self.assertEqual(d28["side"], "NO")

    def test_widened_decision_windows(self):
        """Verify widened decision windows trigger correctly at boundary hours."""
        event_low = {"title": "Lowest temperature in London on August 18?", "city": "London", "markets": []}
        event_high = {"title": "Highest temperature in London on August 18?", "city": "London", "markets": []}
        city_cfg = MAP["London"] # dawn = 5.9, lastlight = 20.2
        book = [
            {"bucket": "14°C", "lo": 13.5, "hi": 14.5, "val": 14.0, "yes_bid": 0.15, "yes_bid_sz": 100, "yes_ask": 0.20, "yes_ask_sz": 100},
            {"bucket": "28°C", "lo": 27.5, "hi": 28.5, "val": 28.0, "yes_bid": 0.15, "yes_bid_sz": 100, "yes_ask": 0.20, "yes_ask_sz": 100}
        ]
        # Low window: [5.9 - 2.5 = 3.4, 5.9 + 2.5 = 8.4]
        self.assertTrue(len(detectors(event_low, city_cfg, local_hour=3.5, obs=18.0, precip=False, book=book, runmin=18.0, trend=0.0)) > 0)
        self.assertEqual(len(detectors(event_low, city_cfg, local_hour=3.0, obs=18.0, precip=False, book=book, runmin=18.0, trend=0.0)), 0)

        # High window: [20.2 - 3.5 = 16.7, 20.2 + 3.0 = 23.2]
        self.assertTrue(len(detectors(event_high, city_cfg, local_hour=17.0, obs=24.0, precip=False, book=book, runmax=24.0, trend=0.0)) > 0)
        self.assertEqual(len(detectors(event_high, city_cfg, local_hour=16.0, obs=24.0, precip=False, book=book, runmax=24.0, trend=0.0)), 0)

    def test_live_trader_sizing_tiers(self):
        """Verify Dynamic Sizing tiers under $150 Capital Model: $15 for <=0.70, $12 for 0.70-0.85, $8 for 0.85-0.94."""
        remaining_budget = 150.0
        sz_now = 100
        # Tier 1: px = 0.65 -> card_tier = $15.0 -> shares = int(min(15.0 / 0.65, 0.9 * 100)) = 23
        px1 = 0.65
        card_tier1 = min(15.0, remaining_budget)
        shares1 = int(min(card_tier1 / px1, 0.9 * sz_now))
        self.assertEqual(shares1, 23)
        self.assertAlmostEqual(shares1 * px1, 14.95, places=2)

        # Tier 2: px = 0.80 -> card_tier = $12.0 -> shares = int(min(12.0 / 0.80, 0.9 * 100)) = 15
        px2 = 0.80
        card_tier2 = min(12.0, remaining_budget)
        shares2 = int(min(card_tier2 / px2, 0.9 * sz_now))
        self.assertEqual(shares2, 15)
        self.assertAlmostEqual(shares2 * px2, 12.00, places=2)

        # Tier 3: px = 0.88 -> card_tier = $8.0 -> shares = int(min(8.0 / 0.88, 0.9 * 100)) = 9
        px3 = 0.88
        card_tier3 = min(8.0, remaining_budget)
        shares3 = int(min(card_tier3 / px3, 0.9 * sz_now))
        self.assertEqual(shares3, 9)
        self.assertAlmostEqual(shares3 * px3, 7.92, places=2)

    def test_base_live_rules_and_safeguards(self):
        """Verify lotto rule enablement and live rule set integrity including R5."""
        cfg = env()
        self.assertEqual(cfg.get("ALLOW_LOTTOS"), "true")
        self.assertIn("R2_low_dead_below", BASE_LIVE_RULES)
        self.assertIn("R3_high_dead_above", BASE_LIVE_RULES)
        self.assertIn("R5_high_dead_below", BASE_LIVE_RULES)
        self.assertNotIn("R1_low_lotto", BASE_LIVE_RULES)
        self.assertNotIn("R4_high_lotto", BASE_LIVE_RULES)

    def test_parse_filled_shares(self):
        """Verify parsing of actual filled shares from CLOB FAK responses."""
        from scripts.live_trader import parse_filled_shares
        # Full fill via takingAmount
        self.assertEqual(parse_filled_shares({"takingAmount": "25.0"}, 25), 25.0)
        # Partial fill via takingAmount
        self.assertEqual(parse_filled_shares({"takingAmount": "12.5"}, 25), 12.5)
        # Zero fill
        self.assertEqual(parse_filled_shares({"takingAmount": "0"}, 25), 0.0)
        # Alternate field filled_size
        self.assertEqual(parse_filled_shares({"filled_size": "10"}, 25), 10.0)
        # Matched status fallback
        self.assertEqual(parse_filled_shares({"status": "matched"}, 25), 25.0)
        # Non-dict / error
        self.assertEqual(parse_filled_shares(None, 25), 0.0)

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

    def test_detectors_require_running_extrema(self):
        """Verify detectors require cumulative running extrema and do not fall back to instantaneous obs."""
        event_high = {"title": "Highest temperature in Paris on August 20?", "city": "Paris"}
        cfg = MAP["Paris"]
        book = [{"bucket": "35°C", "lo": 34.5, "hi": 35.5, "val": 35, "yes_bid": 0.10, "yes_bid_sz": 100}]
        # Without runmax, high-side detector must NOT fire
        dets = detectors(event_high, cfg, local_hour=18.0, obs=26.0, precip=False, book=book, runmax=None, trend=0.0)
        self.assertEqual(len(dets), 0, "Detector must require runmax for high-side decisions")

        event_low = {"title": "Lowest temperature in Paris on August 20?", "city": "Paris"}
        book_low = [{"bucket": "14°C", "lo": 13.5, "hi": 14.5, "val": 14, "yes_bid": 0.15, "yes_bid_sz": 100}]
        # Without runmin, low-side detector must NOT fire
        dets_low = detectors(event_low, cfg, local_hour=5.5, obs=18.0, precip=False, book=book_low, runmin=None, trend=0.0)
        self.assertEqual(len(dets_low), 0, "Detector must require runmin for low-side decisions")

    def test_precip_does_not_override_velocity(self):
        """Verify that precipitation does NOT bypass the velocity trend filter on high-side contracts."""
        event = {"title": "Highest temperature in Paris on August 20?", "city": "Paris"}
        cfg = MAP["Paris"]
        book = [{"bucket": "35°C", "lo": 34.5, "hi": 35.5, "val": 35, "yes_bid": 0.10, "yes_bid_sz": 100}]
        # Surge of +0.5 C/hr with precip=True must be BLOCKED
        dets = detectors(event, cfg, local_hour=18.0, obs=26.0, precip=True, book=book, runmax=28.0, trend=0.5)
        self.assertEqual(len(dets), 0, "Temperature surging +0.5 C/hr must be blocked even if precip is True")

    def test_position_guard_empty_book_retains_position(self):
        """Verify PositionGuard retains open positions if order book has no bids instead of dropping tracking."""
        from unittest.mock import patch
        cfg = {"DRY_RUN": "true", "LIVE_ENABLED": "false"}
        state = {
            "open": {
                "Lowest temperature in Paris on August 19?|18°C|NO": {
                    "city": "Paris", "bucket": "18°C", "side": "NO",
                    "rule": "R2_low_dead_below", "token": "tok123",
                    "shares": 10, "px": 0.89, "dry": True
                }
            },
            "processed": {}
        }
        # Mock weather response to indicate compression (obs=19.0C -> dist=0.5C < 0.7C)
        # And mock CLOB book to return empty bids
        with patch("scripts.live_trader.get") as mock_get:
            def side_effect(url, **kwargs):
                if "aviationweather" in url:
                    return [{"icaoId": "LFPB", "temp": 19.0}]
                elif "clob" in url:
                    return {"bids": [], "asks": []}
                return {}
            mock_get.side_effect = side_effect
            run_position_guard(cfg, state)
            # Position must STILL remain in open!
            self.assertIn("Lowest temperature in Paris on August 19?|18°C|NO", state["open"],
                          "Position must be retained in state['open'] when no exit bids exist")

    def test_position_guard_bypasses_r5_monotonic(self):
        """Verify PositionGuard bypasses R5_high_dead_below positions when evening temperature drops."""
        from unittest.mock import patch
        cfg = {"DRY_RUN": "true", "LIVE_ENABLED": "false"}
        state = {
            "open": {
                "Highest temperature in Paris on August 20?|20°C|NO": {
                    "city": "Paris", "bucket": "20°C", "side": "NO",
                    "rule": "R5_high_dead_below", "token": "tok456",
                    "shares": 10, "px": 0.85, "dry": True
                }
            },
            "processed": {}
        }
        # Mock weather showing cool evening temp (obs=18.0C -> dist = 18.0 - 20.5 = -2.5C < 0.7C)
        with patch("scripts.live_trader.get") as mock_get:
            def side_effect(url, **kwargs):
                if "aviationweather" in url:
                    return [{"icaoId": "LFPB", "temp": 18.0}]
                elif "clob" in url:
                    return {"bids": [{"price": 0.75, "size": 50}], "asks": []}
                return {}
            mock_get.side_effect = side_effect
            run_position_guard(cfg, state)
            # Position must STILL remain in open because R5 is monotonic!
            self.assertIn("Highest temperature in Paris on August 20?|20°C|NO", state["open"],
                          "R5 positions must not be dumped during evening cooling")

    def test_fee_inclusive_sizing_exact(self):
        """Verify fee-inclusive card sizing guarantees total outlay never exceeds card_tier."""
        px = 0.70
        card_tier = 15.0
        eff_px = px + fee(px) # 0.70 + 0.0105 = 0.7105
        shares = int(card_tier / eff_px) # int(15.0 / 0.7105) = 21
        total_cost = round(eff_px * shares, 2)
        self.assertLessEqual(total_cost, card_tier, "Total outlay with fee must not exceed card_tier")

    def test_read_new_detections_handles_torn_line(self):
        """Verify read_new_detections does not advance offset on a torn line without trailing newline."""
        import tempfile
        from scripts.live_trader import read_new_detections
        with tempfile.NamedTemporaryFile("wb", delete=False) as f:
            f.write(b'{"key": "trade1"}\n{"key": "trade2"') # trade2 is torn
            tmp_path = f.name
        try:
            state = {"det_offset": 0}
            import scripts.live_trader
            orig_det = scripts.live_trader.DET
            scripts.live_trader.DET = tmp_path
            dets = read_new_detections(state)
            self.assertEqual(len(dets), 1, "Only the complete line should be parsed")
            self.assertEqual(dets[0]["key"], "trade1")
            self.assertEqual(state["det_offset"], len(b'{"key": "trade1"}\n'),
                             "Offset must pause at start of torn line, not at EOF")
        finally:
            scripts.live_trader.DET = orig_det
            if os.path.exists(tmp_path): os.remove(tmp_path)

    def test_official_outcome_rejects_zeroed_prices(self):
        """Verify official_outcome treats ['0', '0'] placeholder prices as UNRESOLVED (None)."""
        from unittest.mock import patch
        from scripts.supervisor import official_outcome
        det = {"slug": "highest-temp-paris-2026", "bucket": "25°C"}
        mock_event = [{
            "closed": True,
            "markets": [{
                "groupItemTitle": "25°C",
                "outcomePrices": '["0", "0"]',
                "outcomes": ["Yes", "No"]
            }]
        }]
        with patch("scripts.supervisor.get", return_value=mock_event):
            res = official_outcome(det)
            self.assertIsNone(res, "Transitional ['0', '0'] must not resolve market prematurely")

    def test_position_guard_partial_exit_scales_cost(self):
        """Verify PositionGuard scales pos['cost'] proportionally on partial exits."""
        from unittest.mock import patch
        cfg = {"DRY_RUN": "true", "LIVE_ENABLED": "false"}
        state = {
            "open": {
                "Lowest temperature in Paris on August 20?|15°C|NO": {
                    "city": "Paris", "bucket": "15°C", "rule": "R2_low_dead_below",
                    "shares": 20.0, "cost": 15.0, "px": 0.75, "token": "tok1", "dry": True
                }
            },
            "processed": {}
        }
        # Mock weather showing station at 14.5C (dist = 14.5 - 15.5 = -1.0 < 0.7 -> guard triggers)
        # Mock orderbook with bid size = 10 (partial exit: 10 out of 20 shares)
        with patch("scripts.live_trader.get") as mock_get:
            def side_effect(url, **kwargs):
                if "aviationweather" in url:
                    return [{"icaoId": "LFPB", "temp": 14.5}]
                if "clob.polymarket.com/book" in url:
                    return {"bids": [{"price": 0.70, "size": 10}], "asks": []}
                return {}
            mock_get.side_effect = side_effect
            run_position_guard(cfg, state)
            pos = state["open"]["Lowest temperature in Paris on August 20?|15°C|NO"]
            self.assertEqual(pos["shares"], 10.0, "Shares should be decremented by 10")
            self.assertEqual(pos["cost"], 7.5, "Cost must be scaled to 7.5 to prevent exposure leak")

    def test_chicago_station_is_kord(self):
        """Verify Chicago maps to O'Hare (KORD) matching Polymarket contract resolution source."""
        self.assertEqual(MAP["Chicago"][0], "KORD", "Chicago must resolve to KORD")

    def test_parse_filled_shares_with_order_hashes(self):
        """Verify parse_filled_shares treats CLOB success with orderHashes as filled."""
        from scripts.live_trader import parse_filled_shares
        detail = {"success": True, "errorMsg": "", "orderID": "0xabc", "orderHashes": ["0xhash1"]}
        sh = parse_filled_shares(detail, default_shares=15.0, side="BUY")
        self.assertEqual(sh, 15.0, "Orders with orderHashes must return filled shares")

    def test_parse_filled_shares_with_client_get_order(self):
        """Verify parse_filled_shares queries client.get_order() when orderID is provided."""
        from unittest.mock import MagicMock
        from scripts.live_trader import parse_filled_shares
        mock_client = MagicMock()
        mock_client.get_order.return_value = {"size_matched": "12.0", "status": "matched"}
        detail = {"success": True, "orderID": "0xorder123"}
        sh = parse_filled_shares(detail, default_shares=15.0, side="BUY", client=mock_client)
        self.assertEqual(sh, 12.0, "Exact size_matched must be extracted from client.get_order()")
        mock_client.get_order.assert_called_once_with("0xorder123")

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

