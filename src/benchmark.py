"""Validate measurements and summarize a planned two-arm learning study."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['participant_id', 'group', 'pretest_score', 'posttest_score',
          'task_minutes', 'critical_thinking_score']


def load_rows(path, config):
    groups = set(config['groups'].values())
    if len(groups) != 2:
        raise ValueError('Control and treatment group labels must differ.')
    limits = {
        'pretest_score': config['score_max'],
        'posttest_score': config['score_max'],
        'task_minutes': config['task_time_limit_minutes'],
        'critical_thinking_score': config['critical_thinking_max'],
    }
    for name, limit in limits.items():
        if not isinstance(limit, (int, float)) or not math.isfinite(limit) or limit <= 0:
            raise ValueError(f'Invalid positive limit for {name}.')
    rows, ids = [], set()
    with Path(path).open(newline='', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError('CSV header must exactly match: ' + ','.join(FIELDS))
        for line, raw in enumerate(reader, 2):
            if None in raw or any(v is None or not v.strip() for v in raw.values()):
                raise ValueError(f'Row {line}: missing or excess fields.')
            row = {k: v.strip() for k, v in raw.items()}
            pid = row['participant_id']
            if pid in ids:
                raise ValueError(f'Row {line}: duplicate participant ID.')
            ids.add(pid)
            if row['group'] not in groups:
                raise ValueError(f'Row {line}: unknown group.')
            for key, limit in limits.items():
                try:
                    value = float(row[key])
                except ValueError as error:
                    raise ValueError(f'Row {line}: {key} must be numeric.') from error
                if not math.isfinite(value) or not 0 <= value <= limit:
                    raise ValueError(f'Row {line}: {key} out of range or non-finite.')
                if key == 'task_minutes' and value == 0:
                    raise ValueError(f'Row {line}: time must be positive.')
                row[key] = value
            row['learning_gain_percentage_points'] = row['posttest_score'] - row['pretest_score']
            rows.append(row)
    if {r['group'] for r in rows} != groups:
        raise ValueError('At least one valid record per group is required.')
    return rows


def summarize(rows, config):
    metrics = FIELDS[2:] + ['learning_gain_percentage_points']
    grouped = {}
    for group in config['groups'].values():
        sample = [r for r in rows if r['group'] == group]
        grouped[group] = {
            'n': len(sample),
            'means': {metric: statistics.mean(r[metric] for r in sample) for metric in metrics},
            'time_capped_count': sum(r['task_minutes'] == config['task_time_limit_minutes'] for r in sample)
        }
    control = grouped[config['groups']['control']]['means']
    treatment = grouped[config['groups']['treatment']]['means']
    differences = {metric: treatment[metric] - control[metric] for metric in metrics}
    margin = config['critical_thinking_guardrail_margin']
    if not isinstance(margin, (int, float)) or not math.isfinite(margin) or margin < 0:
        raise ValueError('Critical-thinking guardrail margin must be finite and nonnegative.')
    return {
        'study_title': config['study_title'],
        'data_kind': config['data_kind'],
        'interpretation': 'Descriptive output only. Synthetic inputs are not evidence of research effects.',
        'primary_metric': config['primary_metric'],
        'groups': grouped,
        'treatment_minus_control': differences,
        'guardrails': {
            'input_validation_passed': True,
            'critical_thinking_descriptive_check': differences['critical_thinking_score'] >= -margin,
            'critical_thinking_margin_points': margin,
            'assessment_no_ai_adherence': 'not assessed by this script',
            'note': 'A descriptive mean check does not establish statistical non-inferiority.'
        }
    }


def run(config_path):
    config_path = Path(config_path)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    config = json.loads(config_path.read_text(encoding='utf-8'))
    if config['data_kind'] not in ('synthetic_smoke_test', 'real_pilot'):
        raise ValueError('Set data_kind explicitly to synthetic_smoke_test or real_pilot.')
    if config['primary_metric'] != 'learning_gain_percentage_points':
        raise ValueError('This protocol requires learning_gain_percentage_points as primary metric.')
    input_path = (ROOT / config['input_csv']).resolve()
    outputs = [(ROOT / config[k]).resolve() for k in ('output_json', 'output_log')]
    if len(set([input_path, config_path.resolve()] + outputs)) != 4:
        raise ValueError('Input, configuration and output paths must be distinct.')
    result = summarize(load_rows(input_path, config), config)
    result['provenance'] = {
        'python_version': platform.python_version(),
        'reference_python': '3.12.14',
        'input_sha256': hashlib.sha256(input_path.read_bytes()).hexdigest(),
        'config_sha256': hashlib.sha256(config_path.read_bytes()).hexdigest(),
    }
    rendered = json.dumps(result, indent=2, allow_nan=False)
    for path in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
    outputs[0].write_text(rendered + '\n', encoding='utf-8')
    outputs[1].write_text(
        f"SUCCESS | data_kind={config['data_kind']} | records={sum(g['n'] for g in result['groups'].values())}\n"
        'Descriptive pipeline completed. No hypothesis test was performed.\n', encoding='utf-8')
    print(rendered)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default='configs/config.json')
    args = parser.parse_args()
    try:
        run(args.config)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
