"""Reproduce six educational Li/Mn figures; curves are models, not measurements."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, fontManager
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TEAL = '#087F82'
NAVY = '#203949'
ORANGE = '#D28239'
PURPLE = '#7960A3'
GRAY = '#647985'
PALE = '#EFF5F7'


def arrow(ax, start, end, color=TEAL, lw=2.3, **kw):
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=lw, **kw))


def panel(ax, title, limits=(0, 10, 0, 6)):
    ax.set_xlim(limits[:2]); ax.set_ylim(limits[2:]); ax.axis('off')
    ax.set_title(title, loc='left', color=NAVY, fontsize=13, pad=13)


def box(ax, x, y, w, h, label, color, fill=PALE, size=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                boxstyle='round,pad=0.08,rounding_size=0.12',
                linewidth=1.3, edgecolor=color, facecolor=fill))
    ax.text(x+w/2, y+h/2, label, ha='center', va='center', color=color, fontsize=size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--font-dir', type=Path, required=True)
    args = ap.parse_args()
    fp = FontProperties(fname=str(args.font_dir/'NotoSansKR-400.ttf'))
    fontManager.addfont(fp.get_file())
    plt.rcParams.update({'font.family': fp.get_name(), 'font.size': 11,
                         'svg.fonttype': 'path', 'axes.unicode_minus': False})
    data = json.loads((ROOT/'Data/wbs-learning.json').read_text())
    items = {i['id']: i for i in data['items']}
    out = ROOT/'Knowledge/items'

    def save(fig, name):
        for ext in ['svg', 'png']:
            fig.savefig(out/(name+'.'+ext), bbox_inches='tight',
                        facecolor='white', dpi=220)
        plt.close(fig)

    # Li: both charged species travel in the same electrode-to-electrode
    # direction, along separate external and internal paths.
    fig, axs = plt.subplots(1, 2, figsize=(10.0, 4.1))
    for discharge, ax in enumerate(axs):
        panel(ax, '방전: 음극에서 양극으로' if discharge else '충전: 양극에서 음극으로')
        box(ax, .35, .9, 2.1, 2.0, '양극 (+)\n고체 호스트', NAVY, size=11)
        box(ax, 7.5, .9, 2.1, 2.0, '음극 (-)\n고체 호스트', NAVY, size=11)
        ax.add_patch(Rectangle((2.8, .9), 4.3, 2.0, color='#E6F3F2', ec='none'))
        ax.add_patch(Rectangle((4.8, .9), .3, 2.0, color='#D7E2E6', ec=GRAY, ls='--'))
        ax.text(4.95, .47, '전해질 · 분리막', color=TEAL, ha='center', fontsize=10.5)
        x0, x1 = (7.4, 2.6) if discharge else (2.6, 7.4)
        arrow(ax, (x0, 2.15), (x1, 2.15), TEAL)
        ax.text(4.95, 2.5, r'$\mathrm{Li}^{+}$'+' 내부 이온 경로', ha='center', color=TEAL)
        # external circuit: wires rise from both electrode boxes
        ax.plot([1.4, 1.4, 3.55], [2.95, 4.45, 4.45], color=PURPLE, lw=1.8)
        ax.plot([6.35, 8.55, 8.55], [4.45, 4.45, 2.95], color=PURPLE, lw=1.8)
        box(ax, 3.6, 4.05, 2.7, .8, '외부 부하' if discharge else '충전기', PURPLE,
            fill='#F2EEF7')
        start, end = ((8.2, 5.35), (1.8, 5.35)) if discharge else ((1.8, 5.35), (8.2, 5.35))
        arrow(ax, start, end, PURPLE)
        ax.text(4.95, 5.6, r'$e^{-}$'+' 외부 전자 경로', ha='center', color=PURPLE)
        ax.text(4.95, -.02, '두 경로는 전극 표면의 반응으로 연결된다.', ha='center', color=GRAY, fontsize=10)
    fig.tight_layout(w_pad=2.3)
    save(fig, '1.1.1.1.1_Li_transport')

    c = items['element.li']['calculation']; m = c['atomic_masses']
    masses = [m['Li'], 6*m['C'], m['Li']+m['Fe']+m['P']+4*m['O']]
    q = [c['F']/(3.6*mass) for mass in masses]
    fig, ax = plt.subplots(figsize=(9.8, 3.8))
    labels = ['Li 금속\nLi 질량 기준', '흑연: C'+r'$_6$'+'\n삽입 전 흑연 질량 기준',
              'LFP: LiFePO'+r'$_4$'+'\nLFP 질량 기준']
    ax.barh(np.arange(3), q, height=.52, color=[TEAL, NAVY, ORANGE])
    for i, val in enumerate(q): ax.text(val+65, i, f'{val:,.1f}', va='center', color=NAVY, fontsize=12)
    ax.set_yticks(np.arange(3), labels); ax.invert_yaxis()
    ax.set(xlim=(0, 4400), xlabel='이상화한 비용량 (mAh/g), 각각 다른 물질 질량 기준')
    ax.set_title('같은 전자 1개라도 분모의 몰질량이 다르다: q = F / (3.6M)',
                 loc='left', color=NAVY, pad=17, fontsize=13)
    ax.spines[['top', 'right', 'left']].set_visible(False)
    ax.set_axisbelow(True); ax.grid(axis='x', alpha=.18)
    ax.tick_params(axis='y', length=0, pad=12)
    fig.tight_layout()
    save(fig, '1.1.1.1.1_Li_capacity')

    fig, axs = plt.subplots(1, 2, figsize=(10.0, 3.7))
    for isolated, ax in enumerate(axs):
        panel(ax, '전자 연결이 끊긴 금속 Li' if isolated else '연결된 금속과 계면의 Li 화합물', (0, 10, 0, 5.3))
        ax.add_patch(Rectangle((.55, .55), 8.9, .38, facecolor=NAVY, edgecolor='none'))
        ax.text(5, .05, '전자 경로 · 집전체', ha='center', color=NAVY, fontsize=10.5)
        if isolated:
            ax.add_patch(Circle((5, 2.85), 1.4, facecolor='#EEE8F3', edgecolor=PURPLE, lw=1.6))
            ax.add_patch(Circle((5, 2.85), .95, facecolor=TEAL, edgecolor='white', lw=2))
            ax.text(5, 2.85, r'$\mathrm{Li}^{0}$'+'\n고립 금속', ha='center', va='center', color='white')
            ax.plot([5, 5], [.95, 1.3], color=GRAY, ls='--', lw=1.5)
            ax.text(7.3, 1.2, '연결 끊김', ha='center', color=GRAY, fontsize=10)
            ax.text(5, 4.55, '원소는 남지만 회수에 참여하기 어렵다.', ha='center', color=NAVY, fontsize=10.5)
        else:
            ax.add_patch(Rectangle((2.3, 1), 5.4, 2.1, facecolor=TEAL, edgecolor='none'))
            ax.add_patch(Rectangle((2.1, 3.1), 5.8, .65, facecolor='#EEE8F3', edgecolor=PURPLE))
            ax.text(5, 2.02, r'$\mathrm{Li}^{0}$'+'\n연결된 금속', color='white', ha='center', va='center')
            ax.text(5, 3.42, 'SEI: Li'+r'$^{+}$'+' 화합물', color=PURPLE, ha='center', va='center', fontsize=10.5)
            ax.text(5, 4.55, '계면 화합물 속 Li는 금속과 상태가 다르다.', ha='center', color=NAVY, fontsize=10.5)
    fig.tight_layout(w_pad=2.0)
    save(fig, '1.1.1.1.1_Li_inventory')

    c = items['element.mn']['calculation']; m = c['atomic_masses']; x = c['lmfp_fraction']
    molar_mass = m['Li']+x*m['Mn']+(1-x)*m['Fe']+m['P']+4*m['O']
    qmax = c['F']/(3.6*molar_mass); volts = c['lmfp_model_voltages']; boundary = (1-x)*qmax
    fig, ax = plt.subplots(figsize=(9.4, 3.7))
    ax.axvspan(0, boundary, color='#E8F2F2'); ax.axvspan(boundary, qmax, color='#FCF0E5')
    ax.plot([0, boundary, boundary, qmax], [volts['Fe'], volts['Fe'], volts['Mn'], volts['Mn']], color=NAVY, lw=2.7)
    ax.text(boundary/2, 3.56, r'$\mathrm{Fe}^{2+}/\mathrm{Fe}^{3+}$'+'\n약 3.4 V · 용량의 절반', ha='center', color=TEAL, fontsize=11)
    ax.text((boundary+qmax)/2, 3.73, r'$\mathrm{Mn}^{2+}/\mathrm{Mn}^{3+}$'+'\n약 4.1 V · 용량의 절반', ha='center', color=ORANGE, fontsize=11)
    ax.set(xlim=(0, qmax+4), ylim=(3.1, 4.4), xlabel='LiMn'+r'$_{0.5}$'+'Fe'+r'$_{0.5}$'+'PO'+r'$_4$'+' 질량 기준 계산 용량 (mAh/g)',
           ylabel='모형 전위 (V vs. Li/Li'+r'$^{+}$'+')')
    ax.set_xticks([0, boundary, qmax], ['0', f'{boundary:.1f}', f'{qmax:.1f}'])
    ax.set_yticks([3.2, 3.4, 3.8, 4.1, 4.4])
    ax.set_title('교육용 이상화: Fe와 Mn 반응의 용량 합은 전자 1개', loc='left', color=NAVY, fontsize=13, pad=15)
    ax.grid(axis='y', alpha=.2); ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    save(fig, '1.1.1.1.4_Mn_lmfp_model')

    fig, axs = plt.subplots(1, 2, figsize=(9.9, 3.8))
    equatorial = [(-1.5, -.55), (-.75, .6), (.75, -.6), (1.5, .55)]
    for elongated, ax in enumerate(axs):
        panel(ax, '한 축 방향 결합이 길어진 모형' if elongated else '대칭적인 팔면체의 투영 모형', (-2.65, 2.65, -2.8, 2.8))
        axial = 2.1 if elongated else 1.5
        points = equatorial+[(0, axial), (0, -axial)]
        if elongated:
            for y in [1.5, -1.5]:
                ax.add_patch(Circle((0, y), .18, fill=False, edgecolor=GRAY, ls='--'))
            ax.text(1.9, 1.9, '축 결합\n늘어남', ha='center', color=TEAL, fontsize=10.5)
            arrow(ax, (1.65, 1.52), (.35, 2.05), TEAL, lw=1.5)
        for px, py in points:
            ax.plot([0, px], [0, py], color=GRAY, lw=1.5)
            ax.add_patch(Circle((px, py), .21, facecolor=ORANGE, edgecolor='white', lw=1.5))
            ax.text(px, py, 'O', ha='center', va='center', color='white', fontsize=10)
        ax.add_patch(Circle((0, 0), .38, facecolor=NAVY, edgecolor='white', lw=1.5))
        ax.text(0, 0, r'$\mathrm{Mn}^{3+}$', ha='center', va='center', color='white', fontsize=11)
        ax.text(0, -2.68, '고스핀 d'+r'$^4$'+' · 산소 6개와 배위', ha='center', color=NAVY, fontsize=11)
        ax.set_aspect('equal')
    fig.tight_layout(w_pad=2)
    save(fig, '1.1.1.1.4_Mn_jahn_teller')

    fig, ax = plt.subplots(figsize=(10.1, 3.2))
    panel(ax, '양극의 손실과 음극의 계면 영향을 함께 본다', (0, 15, 0, 4.5))
    box(ax, .25, 1.1, 3.45, 2.1, 'Mn 함유 양극\n표면 반응 · 용출', NAVY)
    box(ax, 5.3, 1.1, 4.2, 2.1, '전해질 경로\nMn 함유 종 이동', TEAL, fill='#E8F3F2')
    box(ax, 11.1, 1.1, 3.55, 2.1, '음극 계면 · SEI\nMn 성분 축적 · 상호작용', PURPLE, fill='#F2EEF7', size=10.5)
    arrow(ax, (3.85, 2.15), (5.15, 2.15), ORANGE)
    arrow(ax, (9.65, 2.15), (10.95, 2.15), ORANGE)
    ax.text(1.98, .4, '조성 · 구조 변화', ha='center', color=NAVY, fontsize=11)
    ax.text(7.4, .4, '이동종의 상태는 환경에 따라 다름', ha='center', color=TEAL, fontsize=10.5)
    ax.text(12.88, .4, '계면 반응 · 저항 변화', ha='center', color=PURPLE, fontsize=11)
    ax.text(7.5, 3.8, '음극에서 Mn를 검출해도 금속 Mn로 바로 판정하지 않는다.', ha='center', color=NAVY, fontsize=11)
    fig.tight_layout()
    save(fig, '1.1.1.1.4_Mn_crosstalk')
    print('Saved six Li/Mn figures as PNG and vector SVG')


if __name__ == '__main__':
    main()
