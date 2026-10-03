"""Original educational figures; all numbers are stated toy models, not data."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle,Rectangle
ROOT=Path(__file__).resolve().parents[1]
import argparse
ap=argparse.ArgumentParser()
ap.add_argument('--font-dir',type=Path,required=True)
args=ap.parse_args()
FONT=FontProperties(fname=str(args.font_dir/'NotoSansKR-400.ttf'))
plt.rcParams.update({'font.family':FONT.get_name(),'axes.unicode_minus':False,'font.size':12})
from matplotlib import font_manager
font_manager.fontManager.addfont(FONT.get_file())
OUT=ROOT/'Knowledge/items'
def save(name,fig):
 fig.tight_layout();fig.savefig(OUT/(name+'.png'),dpi=155)
 svg=OUT/(name+'.svg');fig.savefig(svg)
 svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
 plt.close(fig)
def axes():return plt.subplots(figsize=(8,3.3))
f,a=axes();r=np.linspace(.5,5,100);a.plot(r,r*r,color='#087f82',lw=3);a.set(xlabel='확산 길이 / 기준 길이',ylabel='확산 시간 / 기준 시간',title='같은 D에서 시간 척도는 길이의 제곱에 비례');a.grid(alpha=.2);save('study_diffusion',f)
f,a=axes();d=np.linspace(1,20,100);a.plot(d,6/(4*d),color='#087f82',lw=3);a.set(xlabel='구형 입자 지름 (마이크로미터)',ylabel='이상적 외부 면적 (m²/g)',title='S = 6 / (밀도 × 지름), 밀도 4 g/cm³');a.grid(alpha=.2);save('study_area',f)
f,a=axes();eps=np.linspace(.2,.7,100);a.plot(eps,eps**1.5,label='교육용: 유효 전도도 / 액체 전도도');a.set(xlabel='전극 공극률',ylabel='상대 유효 전도도',title='공극률과 경로 연결은 전달 성능에 함께 영향을 준다');a.legend();a.grid(alpha=.2);save('study_porosity',f)
f,a=axes();x=np.linspace(0,.2,150);a.plot(x,np.maximum(x-.04,0)**2/.16**2,color='#087f82',lw=3);a.axvline(.04,ls='--',color='#999');a.set(xlabel='도전재 체적분율 (모형)',ylabel='정규화 전도도',title='연속 전자 경로가 만들어지는 퍼콜레이션 개념');a.grid(alpha=.2);save('study_percolation',f)
f,a=axes();a.axis('off')
for j,(title,sub) in enumerate([('층상','Li층을 따라 이동'),('올리빈','주요 1차원 통로'),('스피넬','3차원 연결 통로')]):
 cx=j*2.7+.8;a.add_patch(Rectangle((cx-.7,.4),1.7,1.6,facecolor='#eef5f5',edgecolor='#087f82'));a.text(cx+.15,2.25,title,ha='center',fontsize=15);a.text(cx+.15,.03,sub,ha='center',fontsize=11)
 if j==0:
  for y in [.7,1.2,1.7]:a.plot([cx-.5,cx+.8],[y,y],color='#466f81',lw=4)
  a.annotate('',xy=(cx+.8,.94),xytext=(cx-.5,.94),arrowprops=dict(arrowstyle='->',color='#d27040',lw=2))
 if j==1:
  for xx in [cx-.3,cx+.3]:a.annotate('',xy=(xx,1.8),xytext=(xx,.6),arrowprops=dict(arrowstyle='->',color='#d27040',lw=2))
 if j==2:
  for dx,dy in [(1,0),(0,1),(.7,.7)]:a.annotate('',xy=(cx-.3+dx,.6+dy),xytext=(cx-.3,.6),arrowprops=dict(arrowstyle='->',color='#d27040',lw=2))
a.set(xlim=(-.3,8.1),ylim=(-.25,2.7));save('study_structures',f)
f,a=axes();a.axis('off');a.set(xlim=(0,8),ylim=(0,3))
for x,y in [(1,.8),(2.5,2),(4,.8),(5.7,1.8)]:a.add_patch(Circle((x,y),.42,color='#638da0'));a.text(x,y,'활물질',ha='center',va='center',color='white',fontsize=10)
a.plot([.7,1.7,2.5,3.5,4,5,5.7,7],[.7,1.3,2,1.4,.8,1,1.8,1.3],color='#087f82',lw=4,label='도전 경로');a.plot([.5,1,2.5,4,5.7,6.5],[.4,.8,2,.8,1.8,2.4],color='#d27040',lw=2,ls='--',label='바인더 연결');a.legend(loc='upper right');a.set_title('전자 연결과 기계적 연결을 각각 유지해야 한다');save('study_network',f)
f,a=axes();a.axis('off');a.set(xlim=(0,8),ylim=(0,3))
for xx,rad,label in [(1.8,.6,'삽입 전'),(5.1,.6*4**(1/3),'부피 4배 모형')]:a.add_patch(Circle((xx,1.3),rad,facecolor='#638da0',edgecolor='#203949'));a.text(xx,2.5,label,ha='center')
a.text(3.4,.1,'반지름은 약 1.59배; 실제 팽창은 조성·상태에 따라 달라짐',ha='center',fontsize=12);save('study_expansion',f)
f,a=axes();a.axis('off');a.set(xlim=(0,8),ylim=(0,3))
for xx,label,color in [(1.6,'벌크 전해질','#638da0'),(4,'계면층','#d27040'),(6.5,'전극 내부','#087f82')]:a.add_patch(Rectangle((xx-.8,.6),1.6,1.6,facecolor=color,alpha=.2));a.text(xx,2.35,label,ha='center')
for x in [1.2,2.3,3.4,4.5,5.6,6.7]:a.add_patch(Circle((x,1.4),.11,color='#087f82'))
a.annotate('',xy=(7.3,1),xytext=(.5,1),arrowprops=dict(arrowstyle='->',lw=2));a.text(4,.15,'각 구간의 저항·반응·접촉을 구별한다',ha='center');save('study_interface',f)
f,a=axes();a.bar(['LiC6\nC6 기준','LiFePO4','LiMn0.5Fe0.5PO4','LiMn2O4','LiNi0.5Mn1.5O4'],[371.9,169.9,170.4,148.2,146.7],color=['#638da0','#087f82','#56aaa3','#d27040','#ba9357']);a.set(ylabel='이론 비용량 (mAh/g)',title='명시한 화학식에서 전자 1개를 사용하는 이상화한 계산');save('study_capacity',f)
f,a=axes();a.axis('off');a.set(xlim=(0,8),ylim=(0,3));a.add_patch(Rectangle((.5,1),7,.25,color='#638da0'));a.add_patch(Rectangle((.5,1.25),7,.65,color='#087f82',alpha=.2));a.add_patch(Rectangle((.5,1.9),7,.4,color='#d27040',alpha=.3));a.text(4,.55,'집전체: 전자를 모으는 경로',ha='center');a.text(4,1.56,'다공성 전극: 이온 + 전자 경로',ha='center');a.text(4,2.6,'분리막: 전자 차단 + 전해질을 통한 이온 이동',ha='center');save('study_separator',f)
print('10 original educational figures (PNG + SVG)')
