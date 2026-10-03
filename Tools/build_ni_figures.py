"""Reproducible educational figures for WBS 1.1.1.1.2, not measured data."""
import argparse,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties,fontManager
from matplotlib.patches import Circle,Rectangle
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
TEAL='#087F82';NAVY='#203949';ORANGE='#D28239';BLUE='#4286B3'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--font-dir',type=Path,required=True);a=ap.parse_args()
    fp=FontProperties(fname=str(a.font_dir/'NotoSansKR-400.ttf'));fontManager.addfont(fp.get_file())
    plt.rcParams.update({'font.family':fp.get_name(),'font.size':12,'svg.fonttype':'path','axes.unicode_minus':False})
    item=next(i for i in json.loads((ROOT/'Data/wbs-learning.json').read_text())['items'] if i['id']=='element.ni')
    out=ROOT/'Knowledge/items'
    def save(fig,name):
        fig.savefig(out/(name+'.svg'),bbox_inches='tight',facecolor='white')
        fig.savefig(out/(name+'.png'),bbox_inches='tight',dpi=220,facecolor='white');plt.close(fig)
    def atom(ax,x,y,s,color):
        ax.add_patch(Circle((x,y),.18,facecolor=color,edgecolor='white',linewidth=1.6))
        ax.text(x,y,s,ha='center',va='center',color='white',fontsize=11,fontweight='bold')
    fig,axs=plt.subplots(1,2,figsize=(10,4.1))
    for charged,ax in enumerate(axs):
        ax.set_xlim(-.55,4.5);ax.set_ylim(-.85,3.35);ax.axis('off')
        for y in [.4,1.4,2.4]:
            for x in [.2,1.2,2.2,3.2]:atom(ax,x,y,'O',ORANGE)
        for x in [.2,1.2,2.2,3.2]:atom(ax,x,.9,'Ni',NAVY)
        for j,x in enumerate([.2,1.2,2.2,3.2]):
            if charged and j%2:ax.add_patch(Circle((x,1.9),.17,fill=False,edgecolor=TEAL,linestyle='--',linewidth=1.6))
            else:atom(ax,x,1.9,'Li',TEAL)
        ax.text(3.7,.9,'Ni층',va='center',color=NAVY)
        ax.text(3.7,1.9,'Li층',va='center',color=TEAL)
        ax.set_title('충전 중: 일부 Li 자리 비움' if charged else '충전 전: Li가 차 있는 모델',color=NAVY,pad=12)
        if charged:
            ax.annotate('',xy=(4.2,2.8),xytext=(2.2,2.05),arrowprops={'arrowstyle':'->','color':TEAL,'lw':2})
            ax.text(1.5,2.9,r'$\mathrm{Li}^+$'+'는 전해질 쪽으로',color=TEAL,fontsize=11)
            ax.text(.1,-.35,'전자: 외부 회로로 빠지며 Ni-O 전자상태 변화',color=NAVY,fontsize=10.5)
        else:ax.text(.1,-.35,'Ni는 산소와 함께 전극의 골격을 이룬다.',color=NAVY,fontsize=11)
    fig.tight_layout(w_pad=2)
    save(fig,'1.1.1.1.2_Ni_layer_transport')

    fig,ax=plt.subplots(figsize=(9.4,4.0))
    c=item['calculation'];mass=sum(c['atomic_masses'][e]*n for e,n in {'Li':1,'Ni':1,'O':2}.items());q=c['F']/(3.6*mass)
    z=np.linspace(0,1,101);ax.plot(z,q*z,color=TEAL,lw=2.8)
    for x in [.2,.5,.7]:
        ax.scatter([x],[q*x],color=TEAL,zorder=3)
        ax.annotate(f'z={x:.1f}: {q*x:.1f}',(x,q*x),xytext=(8,-20),textcoords='offset points',fontsize=11,color=NAVY)
    ax.axvline(1,color='#8799A4',ls='--',lw=1.2);ax.text(.98,287,f'z=1 상한: {q:.1f}',ha='right',color=NAVY,fontsize=11)
    ax.set(xlim=(0,1.04),ylim=(0,310),xlabel='화학식 단위당 추출한 Li의 양 z',ylabel=r'$\mathrm{LiNiO}_2$'+' 질량 기준 계산 비용량 (mAh/g)')
    ax.set_title('교육용 계산: q = zF / (3.6M)',loc='left',color=NAVY,pad=16)
    ax.grid(alpha=.18);ax.spines[['top','right']].set_visible(False)
    fig.tight_layout();save(fig,'1.1.1.1.2_Ni_capacity_calculation')

    fig,axs=plt.subplots(1,2,figsize=(10,3.55))
    for defect,ax in enumerate(axs):
        ax.set_xlim(-.55,4.45);ax.set_ylim(-.8,2.3);ax.axis('off')
        for y in [.5,1.5]:ax.add_patch(Rectangle((-.25,y-.27),3.95,.54,facecolor='#F0F5F7',edgecolor='none'))
        for j,x in enumerate([.2,1.2,2.2,3.2]):
            if j==2:ax.add_patch(Circle((x,1.5),.17,fill=False,edgecolor=TEAL,ls='--',lw=1.5))
            else:atom(ax,x,1.5,'Ni' if defect and j==1 else 'Li',NAVY if defect and j==1 else TEAL)
            atom(ax,x,.5,'Li' if defect and j==1 else 'Ni',TEAL if defect and j==1 else NAVY)
        ax.text(3.85,1.5,'Li층',va='center',color=TEAL);ax.text(3.85,.5,'Ni층',va='center',color=NAVY)
        ax.annotate('',xy=(2.0,1.97),xytext=(.2,1.97),arrowprops={'arrowstyle':'->','color':TEAL,'lw':2})
        if defect:
            ax.annotate('자리 교환',xy=(1.2,.87),xytext=(2.0,-.12),fontsize=11,color=NAVY,arrowprops={'arrowstyle':'->','color':NAVY})
            ax.text(.1,-.5,'Li층의 Ni는 이동 경로와 국소 환경을 바꾼다.',fontsize=10.5,color=NAVY)
        else:ax.text(.1,-.5,'빈 Li 자리와 주변 경로를 따라 이동한다.',fontsize=10.5,color=NAVY)
        ax.set_title('Li/Ni 자리 혼입의 예' if defect else '층이 구분된 구조의 예',color=NAVY,pad=8)
    fig.tight_layout(w_pad=2);save(fig,'1.1.1.1.2_Ni_antisite')
    print('Saved three Ni figures as PNG and vector SVG')
if __name__=='__main__':main()
