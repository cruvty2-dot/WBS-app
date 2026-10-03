"""Check source joins, a known experimental point, and circuit limits."""
import csv
import hashlib
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import analyze_eis_soc as eis


class EISChecks(unittest.TestCase):
    def test_known_source_point_and_frequency_join(self):
        _, points, _, selected = eis.load_data()
        self.assertEqual(len(points), 3360)
        self.assertEqual(sum(map(len, selected.values())), 42)
        point = next(p for p in selected[50] if p['frequency_id'] == '4')
        self.assertEqual((point['source_line'], point['frequency_hz']), (967, 1))
        self.assertAlmostEqual(point['real_mohm'], 99.9931838023928, places=10)
        self.assertAlmostEqual(point['minus_imag_mohm'], 1.83267524145727, places=10)
        self.assertAlmostEqual(point['magnitude_mohm'], 100.0099770296932, places=10)
        self.assertAlmostEqual(point['phase_deg'], -1.0499995836962, places=10)

    def test_duplicate_frequency_rejected_even_with_valid_file_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            for file in eis.INPUT.iterdir():
                if file.is_file():
                    (target / file.name).write_bytes(file.read_bytes())
            with (target / 'impedance.csv').open(newline='', encoding='utf-8-sig') as stream:
                reader = csv.DictReader(stream)
                fields = reader.fieldnames
                rows = list(reader)
            original = rows[0]
            other = next(row for row in rows if all(row[key] == original[key] for key in
                         ['MEASURE_ID', 'SOC', 'BATTERY_ID']) and row['FREQUENCY_ID'] != original['FREQUENCY_ID'])
            rows[0]['FREQUENCY_ID'] = other['FREQUENCY_ID']
            with (target / 'impedance.csv').open('w', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader(); writer.writerows(rows)
            manifest = json.loads((target / 'source-manifest.json').read_text(encoding='utf-8'))
            for file in manifest['files']:
                file['sha256'] = hashlib.sha256((target / file['filename']).read_bytes()).hexdigest()
            (target / 'source-manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
            with patch.object(eis, 'INPUT', target), self.assertRaises(AssertionError):
                eis.load_data()

    def test_ideal_circuit_peak_and_series_shift(self):
        frequency = 1 / (2 * math.pi * .010 * .05)
        peak = eis.rc_impedance(frequency, .014, .010, .05)
        self.assertAlmostEqual(peak.real, .019)
        self.assertAlmostEqual(-peak.imag, .005)
        self.assertAlmostEqual(eis.rc_impedance(0, .014, .010, .05).real, .024)
        for f in [.05, 1, 1000]:
            delta = eis.rc_impedance(f, .019, .010, .05) - eis.rc_impedance(f, .014, .010, .05)
            self.assertAlmostEqual(delta.real, .005)
            self.assertAlmostEqual(delta.imag, 0)


if __name__ == '__main__':
    unittest.main()
