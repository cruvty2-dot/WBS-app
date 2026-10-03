"""Validate local example EIS CSVs and generate descriptive plots and metrics.

Run from any directory. Install matplotlib or use the local .analysis-deps folder.
No equivalent-circuit parameters or health classifications are fitted.
"""
import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
if (ROOT / '.analysis-deps').is_dir():
    sys.path.insert(0, str(ROOT / '.analysis-deps'))
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.mpl-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT = ROOT / 'Projects/eis-example-analysis'
COLORS = ['#147D92', '#D27C2C', '#7863A8']


def load(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames
        rows = list(reader)
    cell = {'Frequency_Hz', 'Real_Ohm', 'Imag_Ohm'}.issubset(headers)
    cathode = {'f', 'abs', 'phase', 'Zreal', '-Zimag'}.issubset(headers)
    if not (cell or cathode):
        raise ValueError(f'Unsupported headers: {path.name}')
    if not rows:
        raise ValueError(f'Empty input: {path.name}')
    keys = ['Frequency_Hz', 'Real_Ohm', 'Imag_Ohm'] if cell else ['f', 'Zreal', '-Zimag']
    raw = np.array([[float(row[key]) for key in keys] for row in rows])
    if not np.isfinite(raw).all() or (raw[:, 0] <= 0).any():
        raise ValueError(f'Nonfinite values or nonpositive frequency: {path.name}')
    if len(np.unique(raw[:, 0])) != len(raw):
        raise ValueError(f'Duplicate frequencies: {path.name}')
    order = np.argsort(raw[:, 0])[::-1]
    values = raw[order]
    f, real, imag = values.T
    if cathode:
        imag = -imag  # Source stores -Zimag; restore signed imaginary part.
    z = real + 1j * imag
    quality = {'finite': True, 'positive_frequency': True, 'duplicate_frequency_count': 0,
               'negative_real_count': int((real < 0).sum()), 'rows': len(rows)}
    if cathode:
        supplied_abs = np.array([float(rows[i]['abs']) for i in order])
        supplied_phase = np.array([float(rows[i]['phase']) for i in order])
        # Confirm source phase is in radians, not degrees.
        quality['supplied_magnitude_max_abs_error'] = float(np.max(np.abs(supplied_abs - np.abs(z))))
        quality['supplied_phase_radian_max_abs_error'] = float(np.max(np.abs(supplied_phase - np.angle(z))))
        if not np.allclose(supplied_abs, np.abs(z), rtol=1e-8, atol=1e-10):
            raise ValueError('Magnitude columns disagree')
        if not np.allclose(supplied_phase, np.angle(z), rtol=1e-8, atol=1e-10):
            raise ValueError('Phase column is inconsistent with radian phase')
    return {'name': path.stem, 'path': path, 'f': f, 'real': real, 'imag': imag,
            'z': z, 'cell': cell, 'quality': quality}


def metrics(d):
    f, r, im = d['f'], d['real'], d['imag']
    crossings = []
    for i in range(len(f) - 1):
        if im[i] * im[i + 1] < 0:
            weight = -im[i] / (im[i + 1] - im[i])
            crossings.append({'frequency_hz': float(10 ** (np.log10(f[i]) + weight * (np.log10(f[i + 1]) - np.log10(f[i])))),
                              'real': float(r[i] + weight * (r[i + 1] - r[i])),
                              'imag_transition': 'positive_to_negative' if im[i] > 0 else 'negative_to_positive'})
    high_crossings = [x for x in crossings if x['imag_transition'] == 'positive_to_negative']
    first = high_crossings[0] if high_crossings else None
    return {'dataset': d['name'], 'rows': len(f), 'unit': 'ohm' if d['cell'] else 'source_unit_unconfirmed',
            'f_min_hz': float(f[-1]), 'f_max_hz': float(f[0]),
            'min_real': float(r.min()), 'min_real_frequency_hz': float(f[r.argmin()]),
            'real_at_highest_f': float(r[0]), 'imag_at_highest_f': float(im[0]),
            'real_at_lowest_f': float(r[-1]), 'imag_at_lowest_f': float(im[-1]),
            'magnitude_at_lowest_f': float(abs(d['z'][-1])),
            'phase_at_lowest_f_deg': float(np.angle(d['z'][-1], deg=True)),
            'hf_crossing_real_proxy': first['real'] if first else None,
            'hf_crossing_frequency_hz': first['frequency_hz'] if first else None,
            'zero_crossings': crossings}


def decorate(ax):
    ax.grid(True, alpha=.22, linewidth=.7)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(labelsize=9)


def save(fig, name):
    fig.savefig(OUT / f'{name}.png', dpi=170, facecolor='white')
    plt.close(fig)


def cell_plots(cells):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.3), layout='constrained')
    fig.suptitle('NMC811 21700 examples | SOC 30% (filename label)', fontsize=17, weight='bold')
    for d, color in zip(cells, COLORS):
        label = d['name'].split('-')[-1].upper()
        r, y = d['real'] * 1000, -d['imag'] * 1000
        axes[0].plot(r, y, '.-', color=color, lw=1.3, ms=4, label=label)
        axes[0].scatter(r[0], y[0], marker='s', color=color, s=35)
        axes[0].scatter(r[-1], y[-1], marker='^', color=color, s=45)
        axes[1].loglog(d['f'], np.abs(d['z']) * 1000, '.-', color=color, ms=4, label=label)
        axes[2].semilogx(d['f'], np.angle(d['z'], deg=True), '.-', color=color, ms=4, label=label)
    axes[0].set(title='Nyquist', xlabel="Z real [mOhm]", ylabel="-Z imag [mOhm]")
    axes[0].set_aspect('equal', adjustable='box')
    axes[0].axhline(0, color='#555', lw=.8)
    axes[0].legend(title='Square: highest f / triangle: lowest f', fontsize=8, title_fontsize=8)
    axes[1].set(title='Bode |Z|', xlabel='Frequency [Hz]', ylabel='|Z| [mOhm]')
    axes[1].legend(fontsize=9)
    axes[2].set(title='Bode phase', xlabel='Frequency [Hz]', ylabel='Phase [degrees]')
    axes[2].axhline(0, color='#555', lw=.8)
    for ax in axes:
        decorate(ax)
    fig.supxlabel('Raw data retained; no circuit fit. ID01-03 are file IDs, not confirmed repeat measurements.', fontsize=10)
    save(fig, 'nmc811_nyquist_bode')


def cathode_plots(d):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), layout='constrained')
    fig.suptitle('MJ1 cathode example | discharge SOC 50% (filename label)', fontsize=16, weight='bold')
    r, y = d['real'], -d['imag']
    for ax, mask, title in [(axes[0, 0], np.ones(len(r), dtype=bool), 'Nyquist | all 72 points'),
                            (axes[0, 1], d['f'] <= 1e4, 'Nyquist | zoom: f <= 10 kHz')]:
        ax.plot(r[mask], y[mask], '.-', color=COLORS[0], ms=5, lw=1)
        indices = np.flatnonzero(mask)
        for idx, marker in [(indices[0], 's'), (indices[-1], '^')]:
            ax.scatter(r[idx], y[idx], marker=marker, color=COLORS[1], s=45)
            ax.annotate(f"{d['f'][idx]:.3g} Hz", (r[idx], y[idx]), xytext=(6, 8), textcoords='offset points', fontsize=8)
        ax.set(title=title, xlabel='Z real [source unit]', ylabel='-Z imag [source unit]')
        ax.axhline(0, color='#555', lw=.8)
        ax.set_aspect('equal', adjustable='box')
    axes[1, 0].loglog(d['f'], abs(d['z']), '.-', color=COLORS[0], ms=4)
    axes[1, 0].set(title='Bode |Z|', xlabel='Frequency [Hz]', ylabel='|Z| [source unit]')
    axes[1, 1].semilogx(d['f'], np.angle(d['z'], deg=True), '.-', color=COLORS[0], ms=4)
    axes[1, 1].set(title='Bode phase', xlabel='Frequency [Hz]', ylabel='Phase [degrees]')
    for ax in axes.flat:
        decorate(ax)
    fig.supxlabel('Impedance unit and measurement setup unconfirmed. Zoom is a display subset; all data remain in full plots.', fontsize=10)
    save(fig, 'mj1_nyquist_bode')


def main():
    report_path = OUT / '1.4.1.3 EIS분석예시.md'
    previous_report = report_path.read_text(encoding='utf-8')
    form_start = '<!-- analysis-request-form:start -->'
    form_end = '<!-- analysis-request-form:end -->'
    if previous_report.count(form_start) != 1 or previous_report.count(form_end) != 1:
        raise ValueError('Restore the reviewed analysis request form before regenerating this example.')
    start = previous_report.index(form_start)
    end = previous_report.index(form_end)
    if start >= end:
        raise ValueError('Analysis request form markers are out of order.')
    request_form = previous_report[start:end + len(form_end)]
    datasets = [load(p) for p in sorted((ROOT / 'Data/static/eis').glob('*.csv'))]
    cells = [d for d in datasets if d['cell']]
    cathodes = [d for d in datasets if not d['cell']]
    if len(cells) != 3 or len(cathodes) != 1:
        raise ValueError('This example report expects three NMC811 files and one MJ1 file')
    if not all(np.array_equal(d['f'], cells[0]['f']) for d in cells):
        raise ValueError('NMC811 frequency grids differ; direct point comparison requires alignment')
    OUT.mkdir(parents=True, exist_ok=True)
    summaries = [metrics(d) for d in datasets]
    cell_summaries = [s for s in summaries if s['unit'] == 'ohm']
    with (OUT / 'summary.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        fields = [k for k in summaries[0] if k != 'zero_crossings']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows({k: s[k] for k in fields} for s in summaries)
    with (OUT / 'derived_points.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['dataset', 'frequency_hz', 'real', 'imag', 'minus_imag', 'magnitude', 'phase_deg', 'unit'])
        for d in datasets:
            for f, r, im, z in zip(d['f'], d['real'], d['imag'], d['z']):
                writer.writerow([d['name'], f, r, im, -im, abs(z), np.angle(z, deg=True), 'ohm' if d['cell'] else 'source_unit_unconfirmed'])
    record = {
        'schema_version': '1.0', 'id': 'eis-example-analysis-20261003',
        'request_id': 'eis-example-analysis-20261003', 'title': 'EIS 예시 데이터 기초 분석',
        'primary_category_id': 'method.eis', 'related_category_ids': ['d.eval.degradation'], 'wbs_task_ids': [],
        'input_files': [{'path': d['path'].relative_to(ROOT).as_posix(),
                         'sha256': hashlib.sha256(d['path'].read_bytes()).hexdigest(),
                         'source_url': None, 'source_status': 'unconfirmed'} for d in datasets],
        'code_files': ['Tools/analyze_eis_examples.py'],
        'result_files': [f'Projects/eis-example-analysis/{name}' for name in
                         ['1.4.1.3 EIS분석예시.md', 'summary.csv', 'derived_points.csv', 'nmc811_nyquist_bode.png', 'mj1_nyquist_bode.png']],
        'created_at': datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds'),
        'author': 'Codex', 'review_status': 'pending_review',
        'data_role': 'external_example_unverified',
        'user_data_statement': 'User confirmed these are example data, not their own measured data.',
        'publication_authorization': {'scope': 'four input CSVs and derived analysis artifacts on public GitHub',
                                      'authorized_by': 'user', 'authorized_on': '2026-10-03'},
        'measurements': summaries,
        'checks': {d['name']: d['quality'] for d in datasets},
        'assumptions': ['Frequency_Hz and Real_Ohm/Imag_Ohm follow their headers.',
                        'MJ1 f is treated as Hz provisionally; impedance unit remains unconfirmed.',
                        'MJ1 -Zimag is negated to recover Zimag; phase radians confirmed numerically.',
                        'SOC and cell/cathode descriptions come only from filenames.'],
        'limitations': ['Original source, license, temperature, AC amplitude, equipment, cell history and geometry unavailable.',
                        'File IDs do not establish experimental replication.', 'No circuit fitting or Kramers-Kronig validation performed.',
                        'Real-axis crossing is an interpolated descriptive proxy, not a validated R_s.',
                        'Cell and cathode spectra are not ranked against one another.'],
        'standard_refs': [],
        'environment': {'python_version': platform.python_version(), 'packages': {'numpy': np.__version__, 'matplotlib': matplotlib.__version__}},
    }
    (OUT / 'analysis-record.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    cell_plots(cells)
    cathode_plots(cathodes[0])
    proxy = [s['hf_crossing_real_proxy'] * 1000 for s in cell_summaries]
    low = [s['real_at_lowest_f'] * 1000 for s in cell_summaries]
    lines = ['# 1.4.1.3 EIS분석예시', '',
             '> 학습 상태: 학습중 (사용자가 읽고 수정하기 시작함)', '',
             '> 2026-10-03 | 분류: 1.4.1.3 EIS (`method.eis`) | 검토 상태: pending_review', '',
             '[전체 구조](../../index.md) · [작업 계획](../../study-plan.md)', '',
             '처음 한 파일로 축 설정과 곡선 읽기를 공부하려면 [1.4.1.3 EIS](1.4.1.3%20EIS.md)를 먼저 읽는다. 원본 한 행의 계산, 주석 그림, 측정조건 비교 절차와 교육용 모형을 연결한다.', '',
             '## 이 예시를 사용하는 목적', '',
             '이 문서는 앞으로 사용자가 제공하는 데이터를 어떤 순서로 분석하고 설명할지 함께 학습하고 수정하는 예시다. 그래프의 배치·설명의 깊이·중점 지표·비교 기준·결론과 한계를 검토하면서 결과 작성 방식을 다듬는다. 새 데이터의 결과는 그 데이터의 원본·측정조건·분석 목적을 기준으로 작성하고, 이 예시의 수치나 조건을 그대로 적용하지 않는다.', '',
             '기초는 [1.4.1.3 EIS](1.4.1.3%20EIS.md)에서 그래프 하나씩 익힌다. 결과 설명은 **분석 목적·조건 → 그림별 중점 관찰 → 비교 수치 → 종합 해석 → 추가 확인** 순서로 함께 다듬는다. 설명 방식의 수정은 저장소 작업 기준과 문서에 반영한다.', '',
             request_form, '',
             '## 예시 자료의 범위', '',
             '이 자료는 EIS 분석·그래프 작성 방법을 보여주는 외부 예시다. 사용자는 본인의 실제 측정 데이터가 아니며, CSV 4개와 분석 결과의 공개 GitHub 업로드를 승인했다고 확인했다(2026-10-03). 합성 데이터인지 실제 외부 측정값인지는 확인되지 않았다. 원본 출처·이용 조건·일부 단위·측정조건은 미확인으로 유지한다. 공개 승인은 데이터나 해석의 검증 완료를 의미하지 않는다.', '',
             '## 결과 요약', '',
             'NMC811 세 파일은 같은 44개 주파수 지점에서 비슷한 곡선 형태를 보인다. ID02의 실수 임피던스가 ID01·ID03보다 높다. 파일 ID만으로 동일 시료의 반복 측정인지 서로 다른 셀인지 알 수 없어 반복성이나 열화 정도로 단정하지 않는다.', '',
             f'고주파 측 실축 교차값은 {min(proxy):.3f}–{max(proxy):.3f} mΩ, 최저 주파수 0.05 Hz에서 실수 임피던스는 {min(low):.3f}–{max(low):.3f} mΩ이다. 교차값은 인접 두 점의 선형 보간값이며 확정된 옴 저항 R_s가 아니다.', '',
             'MJ1 파일은 양극 데이터라는 파일명과 다른 주파수 범위·임피던스 스케일을 갖는다. 단위와 측정 구성이 불명확하므로 NMC811 셀과 수치 크기로 성능을 비교하지 않는다.', '',
             '## NMC811 셀 예시: Nyquist와 Bode', '', '![NMC811 Nyquist 및 Bode](nmc811_nyquist_bode.png)', '',
             '| 파일 ID | 점 수 | 주파수 범위 (Hz) | 고주파 측 실축 교차값 (mΩ) | 교차 주파수 (Hz) | 0.05 Hz 실수값 (mΩ) | 0.05 Hz 위상 (°) |',
             '| --- | --- | --- | --- | --- | --- | --- |']
    for s in cell_summaries:
        lines.append(f"| {s['dataset'].split('-')[-1].upper()} | {s['rows']} | {s['f_min_hz']:.3g}–{s['f_max_hz']:.3g} | {s['hf_crossing_real_proxy'] * 1000:.3f} | {s['hf_crossing_frequency_hz']:.1f} | {s['real_at_lowest_f'] * 1000:.3f} | {s['phase_at_lowest_f_deg']:.2f} |")
    lines += ['', '고주파에서 양의 허수값, 중간·낮은 주파수에서 음의 허수값이 나타난다. 유도성 응답은 연결선·측정 배치 등의 영향일 수 있지만 이 데이터만으로 원인을 특정하지 않는다. 저주파 쪽 곡선의 증가는 느린 응답과 양립하며, 확산계수·전하전달저항·열화 원인은 별도 모델과 검증 없이는 결정하지 않는다.', '',
              '## MJ1 양극 예시: 전체 범위와 확대', '', '![MJ1 Nyquist 및 Bode](mj1_nyquist_bode.png)', '',
              '전체 72개 지점(가정: 0.01 Hz–2 MHz)을 표시한다. 오른쪽 위 Nyquist는 10 kHz 이하만 확대한다. 확대를 위한 표시 범위이며 이상치 제거가 아니다. 전체 데이터와 Bode에는 모든 지점이 남아 있다.', '',
              '고주파에서 굴곡이 보이고 전체 데이터에서 허수부 부호 전환은 1회 확인된다. 장비·배선·보정·데이터 출처를 확인해야 하며, 임의로 한 개 반원에 피팅하지 않았다.', '',
              '## 계산·단위·검증', '',
              '- 복소 임피던스: `Z = Zreal + j Zimag`.',
              '- Nyquist: 가로 `Zreal`, 세로 `-Zimag`. NMC811만 Ω→mΩ로 변환함.',
              '- Bode 크기: `|Z| = sqrt(Zreal² + Zimag²)`; 위상: `atan2(Zimag, Zreal) × 180/π`.',
              '- MJ1은 원본 `-Zimag`의 부호를 복원함. `abs`와 재계산 크기, `phase`와 라디안 위상의 일치를 검증함.',
              '- 네 파일 모두 유한한 수치·양의 주파수·주파수 중복 없음 확인. NMC811 세 파일의 주파수 배열이 정확히 일치함.',
              '- 모든 입력 행을 유지하고 주파수 내림차순으로 정렬함. 평활화·이상치 제거·회로 피팅을 수행하지 않음.',
              '- 고주파 측 교차값은 주파수 내림차순으로 처음 나타나는 허수부 양→음 부호 전환의 실수값을 선형 보간함. 교차 주파수는 log10(f)에서 보간함.', '',
              '## 파일과 재현', '',
              '| 산출물 | 용도 |', '| --- | --- |',
              '| [summary.csv](summary.csv) | 파일별 지표; 원본 단위 유지 |',
              '| [derived_points.csv](derived_points.csv) | 모든 204개 점의 크기·위상 계산 |',
              '| [analysis-record.json](analysis-record.json) | 입력 해시·검증·단위·가정·한계 |',
              '| [분석 코드](../../Tools/analyze_eis_examples.py) | 결과와 그래프 재생성 |', '',
              '입력 파일:', '']
    for d in datasets:
        lines.append(f"- [{d['path'].name}](../../{d['path'].relative_to(ROOT).as_posix()})")
    lines += ['', '일반 Python 환경은 `pip install matplotlib numpy` 후 `python Tools/analyze_eis_examples.py`로 실행한다. 현재 환경은 [작업 계획](../../study-plan.md)의 앱 포함 Python 경로를 사용하며 `.analysis-deps`에 그래프 의존성을 설치했다.', '',
              '## 해석 근거 및 다음 확인', '',
              '- [Gamry: Basics of EIS](https://www.gamry.com/application-notes/EIS/basics-of-electrochemical-impedance-spectroscopy): Nyquist·Bode 표현과 등가회로 해석의 기본. 데이터 원본 출처를 뜻하지 않음.',
              '- [Gamry: Four-terminal EIS of batteries](https://www.gamry.com/application-notes/battery-research/four-terminal-eis-of-batteries/): 배선·접촉·측정 구성의 영향.',
              '- 확인일: 2026-10-03. 원본 데이터 출처·이용 조건, MJ1의 단위·주파수 단위, 온도·진폭·휴지 시간·전극 면적·시료 관계를 확인해야 함.',
              '- 위 조건을 확보하면 적절한 등가회로 선정, 적합도·잔차·파라미터 식별성 및 Kramers–Kronig 검증을 검토할 수 있음.', '']
    (OUT / '1.4.1.3 EIS분석예시.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'datasets': summaries, 'output': str(OUT)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
