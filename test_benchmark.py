import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('benchmark', ROOT / 'src/benchmark.py')
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)


class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / 'configs/config.json').read_text())
        with (ROOT / 'data/sample/participants.csv').open(newline='') as stream:
            self.rows = list(csv.DictReader(stream))

    def load(self, rows):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'input.csv'
            with path.open('w', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=benchmark.FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            return benchmark.load_rows(path, self.config)

    def test_known_means_and_difference(self):
        result = benchmark.summarize(self.load(self.rows), self.config)
        self.assertAlmostEqual(result['groups']['traditional']['means']['learning_gain_percentage_points'], 10.2)
        self.assertAlmostEqual(result['groups']['genai']['means']['learning_gain_percentage_points'], 16.0)
        self.assertAlmostEqual(result['treatment_minus_control']['learning_gain_percentage_points'], 5.8)
        self.assertAlmostEqual(result['treatment_minus_control']['task_minutes'], -5.4)
        self.assertEqual(result['groups']['genai']['n'], 5)

    def test_reject_invalid_measurements(self):
        cases = [('posttest_score', 'NaN'), ('posttest_score', '101'),
                 ('pretest_score', '-1'), ('task_minutes', '0'),
                 ('task_minutes', 'inf'), ('critical_thinking_score', '21'),
                 ('group', 'unknown'), ('participant_id', ''), ('posttest_score', '')]
        for key, value in cases:
            with self.subTest(key=key, value=value):
                rows = [dict(r) for r in self.rows]
                rows[0][key] = value
                with self.assertRaises(ValueError):
                    self.load(rows)

    def test_duplicate_and_missing_arm(self):
        for rows in [self.rows + [self.rows[0]], self.rows[:5], []]:
            with self.subTest(size=len(rows)), self.assertRaises(ValueError):
                self.load(rows)

    def test_guardrail_detects_decline_and_time_cap(self):
        rows = [dict(r) for r in self.rows]
        for row in rows[5:]:
            row['critical_thinking_score'] = '0'
            row['task_minutes'] = '40'
        result = benchmark.summarize(self.load(rows), self.config)
        self.assertFalse(result['guardrails']['critical_thinking_descriptive_check'])
        self.assertEqual(result['groups']['genai']['time_capped_count'], 5)


if __name__ == '__main__':
    unittest.main()
