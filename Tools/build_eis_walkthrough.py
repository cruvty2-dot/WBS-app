"""Build annotated ID01 plots and an explicitly synthetic parameter illustration.

The walkthrough Markdown is maintained manually. This script only writes figures,
point tables and a provenance/validation record; no WBS content is generated.
"""
import csv
import hashlib
import json
from pathlib import Path

from analyze_eis_examples import ROOT, load, metrics, np, plt, matplotlib
from matplotlib import font_manager

OUT = ROOT / 'Projects/eis-example-analysis'
INPUT = ROOT / 'Data/static/eis/nmc811-21700-soc30-id01.csv'
FONT = Path('C:/Windows/Fonts/malgun.ttf')
if FONT.is_file():
    font_manager.fontManager.addfont(str(FONT))
    plt.rcParams['font.family'] = font_manager.FontProperties(fname=str(FONT)).get_name()
plt.rcParams['axes.unicode_minus'] = False


def style(ax):
    ax.grid(alpha=.2)
    ax.spines[['top', 'right']].set_visible(False)


def save(fig, name):
    fig.savefig(OUT / name, dpi=160, facecolor='white')
    plt.close(fig)


def save_panels(fig, axes, names):
    """Export each plotted axis with its own title, labels and annotations."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    engine = fig.get_layout_engine()
    axis_visibility = [ax.get_visible() for ax in axes]
    text_visibility = [artist.get_visible() for artist in fig.texts]
    # Freeze layout and hide other panels/figure text, which otherwise appear
    # as clipped fragments inside a panel's padded export bounds.
    fig.set_layout_engine(None)
    try:
        for artist in fig.texts:
            artist.set_visible(False)
        for ax, name in zip(axes, names, strict=True):
            for other in axes:
                other.set_visible(other is ax)
            fig.canvas.draw()
            renderer = fig.canvas.get_renderer()
            bounds = ax.get_tightbbox(renderer).transformed(fig.dpi_scale_trans.inverted()).padded(.15)
            fig.savefig(OUT / name, dpi=160, facecolor='white', bbox_inches=bounds)
    finally:
        for ax, visible in zip(axes, axis_visibility, strict=True):
            ax.set_visible(visible)
        for artist, visible in zip(fig.texts, text_visibility, strict=True):
            artist.set_visible(visible)
        fig.set_layout_engine(engine)


def model(f, rs, rp, capacitance):
    return rs + rp / (1 + 1j * 2 * np.pi * f * rp * capacitance)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    d = load(INPUT)
    m = metrics(d)
    f, r, im = d['f'], d['real'], d['imag']
    x, y = 1000 * r, -1000 * im
    worked = int(np.argmin(np.abs(f - 1190)))
    arc = np.flatnonzero((f >= 50) & (f <= 800))
    crest = int(arc[np.argmax(y[arc])])
    point_indices = [0, worked, crest, len(f) - 1]
    with (OUT / 'walkthrough_points.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['data_row_1based', 'frequency_hz', 'real_ohm', 'imag_ohm',
                         'nyquist_x_mohm', 'nyquist_y_mohm', 'bode_magnitude_mohm', 'bode_phase_deg'])
        for i in point_indices:
            writer.writerow([i + 1, f[i], r[i], im[i], x[i], y[i], abs(d['z'][i]) * 1000,
                             np.angle(d['z'][i], deg=True)])

    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2), layout='constrained')
    fig.suptitle('예시 1 · ID01: 한 행을 점으로 바꾸고, 주파수 순서로 읽기', fontsize=17, weight='bold')
    for ax in axes:
        ax.plot(x, y, '.-', color='#117A88', ms=5, lw=1.5)
        ax.axhline(0, color='#888', lw=.8)
        ax.set(xlabel="실수부 Z′ [mΩ]", ylabel="-허수부 -Z″ [mΩ]")
        ax.set_aspect('equal', adjustable='box')
        style(ax)
    axes[0].set_title('전체 44개 점 · 주파수는 축이 아니라 각 점의 표지')
    axes[0].annotate('A · 10,000 Hz\n축 아래: 양의 허수부', (x[0], y[0]), xytext=(15.0, -4.5),
                     arrowprops={'arrowstyle': '->'}, fontsize=10)
    axes[0].annotate('D · 0.05 Hz\n측정 범위의 끝', (x[-1], y[-1]), xytext=(17.0, -2.4),
                     arrowprops={'arrowstyle': '->'}, fontsize=10)
    # Zoom preserves the same polyline; limits only change the displayed view.
    axes[1].set(xlim=(13.3, 20.8), ylim=(-.45, 2.55), title='축 근처 확대 · 선은 원본과 동일')
    bx = m['hf_crossing_real_proxy'] * 1000
    axes[1].scatter([bx], [0], color='#C04C3E', marker='*', s=150, zorder=5)
    axes[1].annotate(f"B · 보간 교차점 {bx:.3f} mΩ\n약 {m['hf_crossing_frequency_hz']:.0f} Hz (측정점 아님)",
                     (bx, 0), xytext=(13.5, 2.12), arrowprops={'arrowstyle': '->'}, fontsize=9)
    axes[1].scatter([x[worked]], [y[worked]], color='#D18425', s=70, zorder=5)
    axes[1].annotate(f"계산 예 · {f[worked]:.0f} Hz\n({x[worked]:.3f}, {y[worked]:.3f})",
                     (x[worked], y[worked]), xytext=(14.6, -.25), arrowprops={'arrowstyle': '->'}, fontsize=9)
    axes[1].annotate(f"C · 호의 꼭대기 부근\n{f[crest]:.1f} Hz", (x[crest], y[crest]), xytext=(16.7, 1.96),
                     arrowprops={'arrowstyle': '->'}, fontsize=10)
    axes[1].annotate('D · 낮은 주파수 꼬리\n관찰 → 원인 후보 → 추가 검증', (x[-1], y[-1]), xytext=(17.4, .7),
                     arrowprops={'arrowstyle': '->'}, fontsize=9)
    for ax in axes:
        ax.scatter([x[0], x[-1]], [y[0], y[-1]], color='#117A88', s=45, zorder=4)
    fig.supxlabel('X와 Y 모두 선형·같은 비율. 44개 점 유지, 평활화·피팅 없음. 확대는 데이터 삭제가 아님.', fontsize=10)
    save_panels(fig, axes, ['walkthrough_nyquist_full.png', 'walkthrough_nyquist_zoom.png'])
    save(fig, 'walkthrough_nyquist.png')

    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, layout='constrained')
    fig.suptitle('ID01 Bode · 같은 행을 주파수 축에서 다시 보기', fontsize=17, weight='bold')
    axes[0].semilogx(f, np.abs(d['z']) * 1000, '.-', color='#117A88')
    axes[0].set(xlabel='주파수 f [Hz] · 로그 축', ylabel='|Z| [mΩ] · 선형 축', title='크기: 해당 주파수에서 전압/전류 응답 비율')
    axes[0].tick_params(axis='x', labelbottom=True)
    axes[1].semilogx(f, np.angle(d['z'], deg=True), '.-', color='#7964A8')
    axes[1].set(xlabel='주파수 f [Hz] · 로그 축', ylabel='위상 φ [°] · 선형 축', title='위상: 전압과 전류의 상대 위상')
    axes[1].axhline(0, color='#888', lw=.8)
    axes[1].set_xticks([.1, 1, 10, 100, 1000, 10000], labels=['0.1', '1', '10', '100', '1000', '10000'])
    for ax, ordinate in [(axes[0], abs(d['z']) * 1000), (axes[1], np.angle(d['z'], deg=True))]:
        ax.axvline(f[worked], color='#D18425', ls='--', lw=1)
        ax.scatter(f[worked], ordinate[worked], color='#D18425', s=55, zorder=5)
        ax.annotate(f"1190 Hz → {ordinate[worked]:.3f}", (f[worked], ordinate[worked]),
                    xytext=(20, 15), textcoords='offset points', fontsize=10,
                    arrowprops={'arrowstyle': '->'})
        style(ax)
    fig.supxlabel('로그 간격: 0.1 → 1 → 10 → 100 → 1000 Hz가 같은 폭. 시간 경과나 충방전 순서가 아님.', fontsize=10)
    save_panels(fig, axes, ['walkthrough_bode_magnitude.png', 'walkthrough_bode_phase.png'])
    save(fig, 'walkthrough_bode.png')

    frequencies = np.logspace(-3, 7, 1000)
    base = model(frequencies, .014, .010, .05)
    rs_up = model(frequencies, .019, .010, .05)
    rp_up = model(frequencies, .014, .020, .05)
    # Analytical checks prove the intended examples, not a fit to measured data.
    assert np.allclose(rs_up - base, .005 + 0j)
    for rp in [.010, .020]:
        peak_f = 1 / (2 * np.pi * rp * .05)
        peak_z = model(peak_f, .014, rp, .05)
        assert np.isclose(peak_z.real, .014 + rp / 2)
        assert np.isclose(-peak_z.imag, rp / 2)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), layout='constrained')
    fig.suptitle('교육용 계산 모형 · 측정 데이터·온도별 실험 결과·피팅값이 아님', fontsize=16, weight='bold')
    for ax in axes:
        ax.plot(base.real * 1000, -base.imag * 1000, color='#117A88', lw=2, label='기준: Rs 14, Rp 10 mΩ')
        ax.set(xlabel='Z′ [mΩ]', ylabel='-Z″ [mΩ]', ylim=(-.3, 12.8))
        ax.set_aspect('equal', adjustable='box')
        style(ax)
    axes[0].plot(rs_up.real * 1000, -rs_up.imag * 1000, color='#D18425', lw=2, label='Rs만 +5 mΩ')
    axes[0].set_title('교육용 모형 · Rs 증가 → 같은 모양을 오른쪽으로 이동', fontsize=12)
    axes[0].annotate('+5 mΩ', (24, 5), xytext=(19, 5), arrowprops={'arrowstyle': '<->'}, fontsize=10)
    axes[1].plot(rp_up.real * 1000, -rp_up.imag * 1000, color='#7964A8', lw=2, label='Rp만 10 → 20 mΩ')
    axes[1].set_title('교육용 모형 · Rp 증가 → 반원 폭·높이 증가, 꼭대기 주파수 감소', fontsize=12)
    axes[1].annotate('318.3 Hz', (19, 5), xytext=(17, 6.5), arrowprops={'arrowstyle': '->'}, fontsize=10)
    axes[1].annotate('159.2 Hz', (24, 10), xytext=(27, 11), arrowprops={'arrowstyle': '->'}, fontsize=10)
    for ax in axes:
        ax.legend(fontsize=9, loc='lower right')
    fig.supxlabel('Z = Rs + Rp/(1 + j·2πf·Rp·C), C = 0.05 F 고정. 파라미터 효과를 분리한 계산 예시.', fontsize=10)
    save_panels(fig, axes, ['walkthrough_model_rs.png', 'walkthrough_model_rp.png'])
    save(fig, 'walkthrough_model_effects.png')
    record = {'role': 'learning_walkthrough', 'input_file': INPUT.relative_to(ROOT).as_posix(),
              'input_sha256': hashlib.sha256(INPUT.read_bytes()).hexdigest(), 'rows': len(f),
              'worked_example_data_row': worked + 1,
              'worked_example': {'frequency_hz': float(f[worked]), 'nyquist_x_mohm': float(x[worked]),
                                 'nyquist_y_mohm': float(y[worked]),
                                 'magnitude_mohm': float(abs(d['z'][worked]) * 1000),
                                 'phase_deg': float(np.angle(d['z'][worked], deg=True))},
              'hf_crossing_proxy': m['hf_crossing_real_proxy'],
              'data_validation': d['quality'],
              'teaching_figures': ['walkthrough_nyquist_full.png', 'walkthrough_nyquist_zoom.png',
                                   'walkthrough_bode_magnitude.png', 'walkthrough_bode_phase.png'],
              'model': {'data_type': 'synthetic_educational', 'fit_performed': False,
                        'rs_ohm': [.014, .019], 'rp_ohm': [.010, .020], 'c_f': .05,
                        'checks': ['Rs shift exactly 0.005 ohm with zero imaginary change',
                                   'Analytical RC crest real=Rs+Rp/2, minus-imag=Rp/2']},
              'packages': {'matplotlib': matplotlib.__version__, 'numpy': np.__version__}}
    (OUT / 'walkthrough-record.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(record['worked_example'], ensure_ascii=False))
    print('Saved four individual data figures, two individual model figures, combined views, point CSV and validation record.')


if __name__ == '__main__':
    main()
