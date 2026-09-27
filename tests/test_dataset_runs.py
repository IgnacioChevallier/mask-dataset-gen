import unittest

from dataset_runs import (
    ConfigError,
    build_tiles,
    config_hash,
    effective_config,
    list_events,
    load_event,
    validate_id,
)


class ConfigFilesTests(unittest.TestCase):
    def test_every_configured_run_is_valid(self):
        events = list_events()
        self.assertTrue(events)
        for event in events:
            for run_id in load_event(event["event_id"])["runs"]:
                with self.subTest(event=event["event_id"], run=run_id):
                    effective_config(event["event_id"], run_id)


class EffectiveConfigTests(unittest.TestCase):
    def test_run_overrides_merge_into_defaults(self):
        config = effective_config("cholila-2015", "baseline-002")
        self.assertEqual(config["rois"][0]["bbox"], [-72.05, -42.65, -71.38, -42.15])
        self.assertEqual(config["mask"]["dnbr_threshold"], 0.3)
        self.assertEqual(config["grid"]["scale_m"], 30)

    def test_derived_run_overrides_algorithm_version(self):
        config = effective_config("cholila-2015", "event-filter-001")
        self.assertEqual(config["algorithm_version"], "event-filter-v1-1")
        self.assertEqual(config["parent_run"], "baseline-002")

    def test_unknown_run_is_rejected(self):
        with self.assertRaises(ConfigError):
            effective_config("cholila-2015", "no-existe")

    def test_unsafe_id_is_rejected(self):
        with self.assertRaises(ConfigError):
            validate_id("../dataset", "run_id")


class TilesAndHashTests(unittest.TestCase):
    CONFIG = {
        "grid": {"scale_m": 20, "tile_pixels": 256},
        "rois": [{"id": "a", "bbox": [0.0, 0.0, 0.1, 0.05]}],
    }

    def test_build_tiles_grid_and_names(self):
        tiles = build_tiles(self.CONFIG)
        # tile ≈ 0.046°: 3 columnas × 2 filas.
        self.assertEqual(len(tiles), 6)
        self.assertEqual(tiles[0]["tile_id"], "roi_01_r000_c000")
        self.assertEqual(tiles[-1]["tile_id"], "roi_01_r001_c002")
        self.assertEqual(tiles[-1]["bbox"][2:], [0.1, 0.05])

    def test_config_hash_ignores_key_order(self):
        reordered = {"rois": self.CONFIG["rois"], "grid": self.CONFIG["grid"]}
        self.assertEqual(config_hash(self.CONFIG), config_hash(reordered))
        self.assertNotEqual(config_hash(self.CONFIG), config_hash({**self.CONFIG, "grid": {}}))


if __name__ == "__main__":
    unittest.main()
