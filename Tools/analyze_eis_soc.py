"""Validate published EIS CSVs and generate separate educational figures.

Source: Buchicchio et al., Mendeley Data v3, doi:10.17632/mbv3bx847g.3,
CC BY 4.0. Raw files stay unchanged. Markdown is reviewed and edited manually.
No equivalent-circuit fitting, extrapolation, smoothing, or PDF generation.
"""
import argparse
import cmath
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'Data/static/eis/buchicchio-2022'
OUT = ROOT / 'Projects/eis-example-analysis'
SOCS = (20, 50, 80)
MEASURE_ID = '02_4'
BATTERY_ID = '02'
EXPECTED_FREQUENCIES = (0.05, 0.1, 0.2, 0.4, 1, 2, 4, 10, 20, 40, 100, 200, 400, 1000)


def rc_impedance(frequency_hz, rs_ohm, rp_ohm, capacitance_f):
    """Illustrative circuit only; not a fit to the published battery data."""
    return rs_ohm + rp_ohm / (1 + 1j * 2 * math.pi * frequency_hz * rp_ohm * capacitance_f)


def load_data():
    manifest = json.loads((INPUT / 'source-manifest.json').read_text(encoding='utf-8'))
    for file in manifest['files']:
        assert hashlib.sha256((INPUT / file['filename']).read_bytes()).hexdigest() == file['sha256']
    with (INPUT / 'frequencies.csv').open(encoding='utf-8-sig', newline='') as stream:
        frequencies = {row['FREQUENCY_ID']: float(row['FREQUENCY_VALUE']) for row in csv.DictReader(stream)}
    assert sorted(frequencies.values()) == list(EXPECTED_FREQUENCIES)
    points = []
    with (INPUT / 'impedance.csv').open(encoding='utf-8-sig', newline='') as stream:
        for line, row in enumerate(csv.DictReader(stream), 2):
            z = complex(row['IMPEDANCE_VALUE'])
            assert math.isfinite(z.real) and math.isfinite(z.imag)
            points.append({'source_line': line, 'measure_id': row['MEASURE_ID'],
                           'battery_id': row['BATTERY_ID'], 'soc_pct': int(row['SOC']),
                           'frequency_id': row['FREQUENCY_ID'], 'frequency_hz': frequencies[row['FREQUENCY_ID']],
                           'real_ohm': z.real, 'imag_ohm': z.imag,
                           'real_mohm': z.real * 1000, 'minus_imag_mohm': -z.imag * 1000,
                           'magnitude_mohm': abs(z) * 1000,
                           'phase_deg': math.degrees(cmath.phase(z)), 'raw_impedance': row['IMPEDANCE_VALUE']})
    groups = defaultdict(list)
    for point in points:
        groups[(point['battery_id'], point['measure_id'], point['soc_pct'])].append(point)
    assert len(points) == 3360 and len(groups) == 240
    batteries = sorted({point['battery_id'] for point in points})
    assert batteries == ['02', '03', '05', '06']
    for battery in batteries:
        measures = {point['measure_id'] for point in points if point['battery_id'] == battery}
        assert len(measures) == 6
        for measure in measures:
            assert {key[2] for key in groups if key[:2] == (battery, measure)} == set(range(10, 101, 10))
    for group in groups.values():
        assert len(group) == 14
        assert sorted(point['frequency_hz'] for point in group) == list(EXPECTED_FREQUENCIES)
    selected = {soc: sorted(groups[(BATTERY_ID, MEASURE_ID, soc)], key=lambda p: -p['frequency_hz']) for soc in SOCS}
    return manifest, points, groups, selected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--validate-only', action='store_true', help='Validate and record calculations without redrawing figures')
    args = parser.parse_args()
    manifest, points, groups, selected = load_data()
    OUT.mkdir(parents=True, exist_ok=True)
    focus = next(point for point in selected[50] if point['frequency_hz'] == 1)
    summaries = []
    for soc in SOCS:
        group = selected[soc]
        at1 = next(point for point in group if point['frequency_hz'] == 1)
        endpoint = group[0]
        repeats = [next(point for point in group if point['frequency_hz'] == 1)
                   for key, group in groups.items() if key[0] == BATTERY_ID and key[2] == soc]
        summaries.append({'soc_pct': soc, 'measure_id': MEASURE_ID, 'battery_id': BATTERY_ID,
                          'real_1000hz_mohm': endpoint['real_mohm'], 'real_1hz_mohm': at1['real_mohm'],
                          'minus_imag_1hz_mohm': at1['minus_imag_mohm'], 'magnitude_1hz_mohm': at1['magnitude_mohm'],
                          'phase_1hz_deg': at1['phase_deg'],
                          'repeat_1hz_real_min_mohm': min(point['real_mohm'] for point in repeats),
                          'repeat_1hz_real_max_mohm': max(point['real_mohm'] for point in repeats),
                          'repeat_count': len(repeats)})
    for name, rows in [('derived_points.csv', [point for soc in SOCS for point in selected[soc]]), ('summary.csv', summaries)]:
        with (OUT / name).open('w', encoding='utf-8-sig', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    record = {'schema_version': '2.0', 'id': 'eis-buchicchio-soc-20261004',
              'primary_category_id': 'method.eis', 'dataset_doi': manifest['doi'],
              'source_url': manifest['source_url'], 'paper_url': manifest['paper_url'],
              'license': 'CC BY 4.0', 'analyzed_at': '2026-10-04', 'review_status': 'pending_user_review',
              'question': 'How do measured EIS curves differ at SOC 20, 50 and 80 percent for the same battery and measurement ID?',
              'raw_files': manifest['files'], 'validation': {'raw_points': len(points), 'groups': len(groups),
               'points_per_spectrum': 14, 'selected_points': 42, 'duplicate_frequencies': 0,
               'missing_or_nonfinite': 0, 'provider_hashes_match': True},
              'selection': {'battery_id': BATTERY_ID, 'measure_id': MEASURE_ID, 'soc_pct': SOCS,
               'rule': 'First sorted source measurement ID for battery 02; do not interpret the suffix as a proven cycle number.'},
              'reported_conditions': {'cell': 'Samsung ICR18650-26J', 'nominal_capacity_mah': 2600,
               'nominal_voltage_v': 3.7, 'temperature_c': '25 +/- 1 (reported chamber condition)',
               'excitation': 'random-phase multisine, 50 mA per frequency component; not total multisine RMS',
               'instrument': 'custom four-wire system with Keysight U2351A DAQ',
               'soc_steps': '1 A discharge for 936 s removes 10% of nominal capacity; 1800 s relaxation',
               'measurement_time_s': 40},
              'unconfirmed': ['per-measurement actual temperature trace', 'amplitude peak/RMS convention',
               'measurement-ID suffix to experimental cycle mapping', 'individual cell actual capacity SOC correction'],
              'processing': ['join FREQUENCY_ID to lookup', 'parse complex impedance in ohms',
               'convert ohm to milliohm', 'sort high to low frequency for Nyquist',
               'calculate magnitude and atan2 phase', 'retain all original rows and keep selected source line IDs'],
              'focus_point': focus, 'summary': summaries,
              'teaching_model': {'purpose': 'Illustration only, not experimental data or battery fitting',
               'formula': 'Rs + Rp/(1+j*2*pi*f*Rp*C)', 'rs_ohm': [0.014, 0.019],
               'rp_ohm': [0.010, 0.020], 'capacitance_f': 0.05},
              'limits': ['No real-axis crossing inside the selected measured domain; 1000 Hz real value is not Rs.',
               '14 frequency points do not identify detailed electrode contributions.',
               'SOC differences do not prove aging or electrode-specific Rct.',
               'Observed ranges across six discharge runs are not confidence intervals or instrument uncertainty.'],
              'result_files': ['Projects/eis-example-analysis/1.4.1.3 EIS.md',
               'Projects/eis-example-analysis/1.4.1.3 EIS분석예시.md',
               'Projects/eis-example-analysis/derived_points.csv', 'Projects/eis-example-analysis/summary.csv'],
              'code_file': 'Tools/analyze_eis_soc.py'}
    record['figure_files'] = ['soc_learning_nyquist.png', 'soc_learning_magnitude.png',
                             'soc_learning_phase.png', 'soc_compare_nyquist.png',
                             'soc_compare_magnitude.png', 'soc_compare_phase.png',
                             'soc_repeat_check.png', 'walkthrough_model_rs.png', 'walkthrough_model_rp.png']
    assert all(point['imag_ohm'] < 0 for group in selected.values() for point in group)
    (OUT / 'analysis-record.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if not args.validate_only:
        draw_figures(selected, groups)
    print(json.dumps({'raw_points': len(points), 'selected': 42, 'focus': focus, 'summary': summaries}, ensure_ascii=True))


def draw_figures(selected, groups):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from matplotlib.ticker import FixedLocator, FuncFormatter
    font = Path('C:/Windows/Fonts/malgun.ttf')
    if font.exists():
        font_manager.fontManager.addfont(str(font))
        plt.rcParams['font.family'] = font_manager.FontProperties(fname=str(font)).get_name()
    plt.rcParams.update({'axes.unicode_minus': False, 'font.size': 12})
    colors = {20: '#bd4b28', 50: '#087f82', 80: '#3456a6'}
    markers = {20: 's', 50: 'o', 80: '^'}

    def canvas(title, xlabel, ylabel):
        fig, ax = plt.subplots(figsize=(9.2, 6.1), layout='constrained')
        ax.set_title(title, pad=16, fontsize=16)
        ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
        ax.grid(alpha=.22); ax.spines[['top', 'right']].set_visible(False)
        return fig, ax

    def save(fig, name):
        if fig.axes[0].get_xscale() == 'log':
            fig.axes[0].xaxis.set_major_locator(FixedLocator([.1, 1, 10, 100, 1000]))
            fig.axes[0].xaxis.set_major_formatter(FuncFormatter(lambda value, _: f'{value:g}'))
        fig.savefig(OUT / name, dpi=160, facecolor='white')
        plt.close(fig)

    group = selected[50]
    focus = next(point for point in group if point['frequency_hz'] == 1)
    fig, ax = canvas('한 곡선부터: 배터리 02 · 측정 02_4 · SOC 50%', '실수부 Z′ (mΩ)', '부호를 뒤집은 허수부 -Z″ (mΩ)')
    ax.plot([p['real_mohm'] for p in group], [p['minus_imag_mohm'] for p in group], 'o-', color=colors[50], linewidth=1.6)
    ax.axhline(0, color='#777', linewidth=.8)
    for freq, tag, shift in [(1000, 'A: 1000 Hz', (-6, 35)), (100, 'B: 100 Hz', (-25, 38)),
                             (1, 'C: 1 Hz', (-42, -24)), (.05, 'D: 0.05 Hz', (-85, 18))]:
        point = next(p for p in group if p['frequency_hz'] == freq)
        ax.annotate(tag, (point['real_mohm'], point['minus_imag_mohm']), xytext=shift,
                    textcoords='offset points', arrowprops={'arrowstyle': '->', 'color': '#666'})
    ax.set_aspect('equal', adjustable='datalim'); ax.margins(x=.15, y=.55)
    save(fig, 'soc_learning_nyquist.png')
    for field, title, ylabel, name in [
        ('magnitude_mohm', '같은 14개 점의 크기', '|Z| (mΩ)', 'soc_learning_magnitude.png'),
        ('phase_deg', '같은 14개 점의 위상', '위상 φ (°)', 'soc_learning_phase.png')]:
        title = '같은 14개 점의 크기: SOC 50%' if field == 'magnitude_mohm' else '같은 14개 점의 위상: SOC 50%'
        fig, ax = canvas(title, '주파수 f (Hz, 로그 축)', ylabel)
        ascending = sorted(group, key=lambda p: p['frequency_hz'])
        ax.semilogx([p['frequency_hz'] for p in ascending], [p[field] for p in ascending], 'o-', color=colors[50])
        ax.axvline(1, color='#c87519', linestyle='--', linewidth=1)
        ax.scatter([1], [focus[field]], color='#c87519', zorder=5)
        ax.annotate(f"1 Hz: {focus[field]:.3f}", (1, focus[field]), xytext=(22, 25), textcoords='offset points', arrowprops={'arrowstyle': '->'})
        if field == 'phase_deg':ax.axhline(0, color='#777', linewidth=.8)
        save(fig, name)
    for kind, title, xlabel, ylabel, name in [
        ('nyquist', 'SOC를 바꿔 비교: 같은 배터리 02 · 측정 02_4', '실수부 Z′ (mΩ)', '-Z″ (mΩ)', 'soc_compare_nyquist.png'),
        ('magnitude_mohm', 'SOC별 크기 비교: 같은 주파수에서 읽기', '주파수 f (Hz, 로그 축)', '|Z| (mΩ)', 'soc_compare_magnitude.png'),
        ('phase_deg', 'SOC별 위상 비교: 크기와 다른 정보', '주파수 f (Hz, 로그 축)', '위상 φ (°)', 'soc_compare_phase.png')]:
        fig, ax = canvas(title, xlabel, ylabel)
        for soc in SOCS:
            group = selected[soc]
            xs = [p['real_mohm'] if kind == 'nyquist' else p['frequency_hz'] for p in group]
            ys = [p['minus_imag_mohm'] if kind == 'nyquist' else p[kind] for p in group]
            ax.plot(xs, ys, marker=markers[soc], color=colors[soc], label=f'SOC {soc}%', linewidth=1.5)
        if kind == 'nyquist':ax.set_aspect('equal', adjustable='datalim'); ax.margins(y=.4)
        else:ax.set_xscale('log'); ax.axvline(1, color='#888', linestyle='--', linewidth=.8)
        ax.legend(frameon=False)
        save(fig, name)
    fig, ax = canvas('같은 배터리의 6개 측정: 1 Hz 실수부의 범위', 'SOC (%)', '1 Hz 실수부 Z′ (mΩ)')
    for soc in SOCS:
        repeats = sorted([(key[1], next(p for p in group if p['frequency_hz'] == 1))
                         for key, group in groups.items() if key[0] == BATTERY_ID and key[2] == soc])
        xs = [soc + (i - 2.5) * .65 for i in range(6)]
        ax.scatter(xs, [p['real_mohm'] for _, p in repeats], marker=markers[soc], color=colors[soc])
        selected_point = next(p for p in selected[soc] if p['frequency_hz'] == 1)
        ax.scatter([soc], [selected_point['real_mohm']], marker='*', s=230, color='#222', zorder=5)
    ax.set_xticks(SOCS);ax.text(.02,.97,'색 점: 6개 측정 ID · 검은 별: 본문에서 선택한 02_4\n가로로 살짝 벌린 것은 겹침 방지이며 SOC 차이가 아님',transform=ax.transAxes,va='top',fontsize=10)
    ax.margins(y=.25)
    save(fig, 'soc_repeat_check.png')

    frequencies = [10 ** (-2 + i * 7 / 600) for i in range(601)]
    for parameter, name, changed, color in [
        ('Rs', 'walkthrough_model_rs.png', (0.019, 0.010), '#bd4b28'),
        ('Rp', 'walkthrough_model_rp.png', (0.014, 0.020), '#7950a6')]:
        fig, ax = canvas(f'교육용 가상 회로: {parameter}만 바꾼다 (실측·피팅 아님)',
                         '실수부 Z′ (mΩ)', '-Z″ (mΩ)')
        for rs, rp, label, curve_color in [
            (0.014, 0.010, '기준: Rs 14 · Rp 10 mΩ', '#087f82'),
            (*changed, f'변경: Rs {changed[0]*1000:.0f} · Rp {changed[1]*1000:.0f} mΩ', color)]:
            values = [rc_impedance(f, rs, rp, 0.05) for f in frequencies]
            ax.plot([z.real * 1000 for z in values], [-z.imag * 1000 for z in values],
                    label=label, color=curve_color, linewidth=2)
        ax.legend(frameon=False); ax.set_aspect('equal', adjustable='datalim')
        ax.set_xticks([14, 19, 24, 29] if parameter == 'Rs' else [14, 19, 24, 29, 34])
        ax.margins(x=.08, y=.3)
        save(fig, name)


if __name__ == '__main__':
    main()
