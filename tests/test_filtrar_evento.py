import math
import unittest

from filtrar_evento import (
    CLASS_OTHER,
    CLASS_TARGET,
    CLASS_UNCONFIRMED,
    choose_target_cluster,
    classify_component,
    cluster_detections,
)


PARAMETERS = {
    "seed_max_distance_m": 1_500,
    "component_hotspot_max_distance_m": 1_000,
    "component_link_max_distance_m": 800,
}


class ClusterDetectionsTests(unittest.TestCase):
    def test_cluster_detections_separates_distant_fires(self):
        detections = [
            {"longitude": -71.44, "latitude": -42.29, "date": "2025-01-15"},
            {"longitude": -71.435, "latitude": -42.29, "date": "2025-01-16"},
            {"longitude": -71.40, "latitude": -42.13, "date": "2025-02-10"},
        ]

        clusters = cluster_detections(detections, radius_m=1_500)

        self.assertEqual(len(clusters), 2)
        self.assertEqual(sorted(len(cluster["members"]) for cluster in clusters), [1, 2])

    def test_choose_target_cluster_uses_ignition_seed(self):
        detections = [
            {"longitude": -71.44, "latitude": -42.29, "date": "2025-01-15"},
            {"longitude": -71.40, "latitude": -42.13, "date": "2025-02-10"},
        ]
        clusters = cluster_detections(detections, radius_m=1_000)

        target = choose_target_cluster(clusters, (-71.441, -42.291))

        self.assertAlmostEqual(target["longitude"], -71.44, places=3)


class ClassifyComponentTests(unittest.TestCase):
    def test_seed_proximity_has_priority(self):
        classification, reason = classify_component(
            seed_distance_m=100,
            target_hotspot_distance_m=math.inf,
            other_hotspot_distance_m=50,
            target_component_distance_m=math.inf,
            parameters=PARAMETERS,
        )

        self.assertEqual(classification, CLASS_TARGET)
        self.assertIn("semilla", reason)

    def test_distinct_hotspot_cluster_marks_other_fire(self):
        classification, _ = classify_component(
            seed_distance_m=10_000,
            target_hotspot_distance_m=9_000,
            other_hotspot_distance_m=200,
            target_component_distance_m=5_000,
            parameters=PARAMETERS,
        )

        self.assertEqual(classification, CLASS_OTHER)

    def test_spatial_link_preserves_fragment_without_hotspot(self):
        classification, reason = classify_component(
            seed_distance_m=5_000,
            target_hotspot_distance_m=5_000,
            other_hotspot_distance_m=math.inf,
            target_component_distance_m=300,
            parameters=PARAMETERS,
        )

        self.assertEqual(classification, CLASS_TARGET)
        self.assertIn("fragmento", reason)

    def test_unsupported_change_remains_auditable(self):
        classification, _ = classify_component(
            seed_distance_m=8_000,
            target_hotspot_distance_m=8_000,
            other_hotspot_distance_m=8_000,
            target_component_distance_m=8_000,
            parameters=PARAMETERS,
        )

        self.assertEqual(classification, CLASS_UNCONFIRMED)


if __name__ == "__main__":
    unittest.main()
