"""Task 3: descriptive analysis of the fixed Task 2 SYNTHETIC fixture."""
import csv
import hashlib
import json
from pathlib import Path
import statistics

from benchmark import FIELDS, load_rows, summarize

ROOT = Path(__file__).resolve().parents[1]
METRICS = FIELDS[2:] + ['learning_gain_percentage_points']


def analyze(raw_path=None):
    raw_path = Path(raw_path) if raw_path else ROOT / 'data/raw/test_run.jsonl'
    config = json.loads((ROOT / 'configs/config.json').read_text(encoding='utf-8'))
    records = [json.loads(line) for line in raw_path.read_text(encoding='utf-8').splitlines() if line.strip()]
    if not records:
        raise ValueError('Empty raw input')
    # No cold execution runs exist in participant-level educational measurements.
    # Do not silently remove slow learners as if they were system warm-up runs.
    for row in records:
        if row.get('data_kind') != 'synthetic_smoke_test' or row.get('phase') != 'evaluation':
            raise ValueError('This demonstration accepts synthetic evaluation records only')
        if set(row) != set(FIELDS) | {'data_kind', 'phase'}:
            raise ValueError('Unexpected or missing raw fields')
    import tempfile
    # Reuse the original Task 2 validator without changing its public interface.
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / 'validated.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows({key: row[key] for key in FIELDS} for row in records)
        rows = load_rows(path, config)
    summary = summarize(rows, config)
    aggregates = []
    for group in config['groups'].values():
        subset = [row for row in rows if row['group'] == group]
        if len(subset) < 2:
            raise ValueError('At least two records per group are needed for sample SD')
        for metric in METRICS:
            values = [row[metric] for row in subset]
            aggregates.append(dict(group=group, metric=metric, n=len(values),
                                   mean=statistics.mean(values), median=statistics.median(values),
                                   sd=statistics.stdev(values), minimum=min(values), maximum=max(values)))
    summary['task3'] = {
        'raw_records': len(records), 'excluded_records': 0,
        'warmup': 'Not applicable: educational measurements, not inference latency.',
        'dispersion': 'Sample SD (n-1); not a confidence interval.',
        'raw_sha256': hashlib.sha256(raw_path.read_bytes()).hexdigest(),
        'randomness': 'None: fixed Task 2 fixture; no sampling or bootstrap.',
    }
    return rows, aggregates, summary


def run():
    rows, aggregates, summary = analyze()
    out = ROOT / 'data/processed'
    out.mkdir(parents=True, exist_ok=True)
    for name, values in [('participants_clean.csv', rows), ('metrics_summary.csv', aggregates)]:
        with (out / name).open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(values[0]))
            writer.writeheader()
            writer.writerows(values)
    (out / 'summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    return rows, aggregates, summary


if __name__ == '__main__':
    _, _, summary = run()
    print(json.dumps(summary, indent=2))
