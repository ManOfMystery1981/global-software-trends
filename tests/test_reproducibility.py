#!/usr/bin/env python3
import json
import unittest
from signal_engine import generate_signal

class TestSignalEngineReproducibility(unittest.TestCase):
    """
    Diligence Proof: Verifies that the multi-factor signal engine is completely
    deterministic and independent of random runtime generation.
    """
    def test_deterministic_reproducibility(self):
        fixture_input = {
            "price_change_24h_pct": 2.5, "price_change_7d_pct": 5.0, "price_change_30d_pct": 12.0,
            "volume_delta": 1.5, "volume_change_24h_pct": 20.0, "turnover_ratio": 0.05,
            "market_cap": 1000000000.0, "volume_24h": 50000000.0, "bid_ask_spread_pct": 0.1,
            "exchange_count": 10, "source_count": 5, "mention_velocity": 1.5,
            "repo_activity_score": 75, "news_count_24h": 4, "social_volume_delta": 1.2,
            "volatility_30d_pct": 25, "max_drawdown_30d_pct": 10, "concentration_top10_pct": 40,
            "data_completeness_pct": 100, "volatility": 0.15
        }
        
        # Run identical calculation loops sequentially
        run_a = generate_signal("TEST_ASSET", fixture_input).to_dict()
        run_b = generate_signal("TEST_ASSET", fixture_input).to_dict()
        
        # Enforce exact identity matches across input and output cryptographic hashes
        self.assertEqual(run_a["input_hash"], run_b["input_hash"])
        self.assertEqual(run_a["output_hash"], run_b["output_hash"])
        self.assertEqual(run_a["composite_score"], run_b["composite_score"])
        print("\n✅ DETERMINISM VERIFIED: Run A Hash matches Run B Hash exactly.")

if __name__ == "__main__":
    unittest.main()
