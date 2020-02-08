import os
import conda

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib

import numpy as np
from datetime import datetime
import matplotlib
import matplotlib.figure
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时'-'显示为方块的问题
def plot_distribution(data, plotname = "2019-nCoV疫情地图"):

    font = FontProperties(fname='res/simhei.ttf', size=14)
    lat_min = 0
    lat_max = 60
    lon_min = 70
    lon_max = 140

    handles = [
            matplotlib.patches.Patch(color='#ffaa85', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#ff7b69', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#bf2121', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#7f1818', alpha=1, linewidth=0),
]
    labels = [ '1-9人', '10-99人', '100-999人', '>1000人']

    fig = matplotlib.figure.Figure()
    fig.set_size_inches(10, 8) # 设置绘图板尺寸
    axes = fig.add_axes((0.1, 0.12, 0.8, 0.8)) # rect = l,b,w,h
    #m = Basemap(llcrnrlon=lon_min, urcrnrlon=lon_max, llcrnrlat=lat_min, urcrnrlat=lat_max, resolution='l', ax=axes)
    m = Basemap(projection='ortho', lat_0=30, lon_0=105, resolution='l', ax=axes)
    
    m.readshapefile('res/china-shapefiles-master/china', 'province', drawbounds=True)
    m.readshapefile('res/china-shapefiles-master/china_nine_dotted_line', 'section', drawbounds=True)
    m.drawcoastlines(color='black') # 洲际线
    m.drawcountries(color='black')  # 国界线
    m.drawparallels(np.arange(lat_min,lat_max,10), labels=[1,0,0,0]) #画经度线
    m.drawmeridians(np.arange(lon_min,lon_max,10), labels=[0,0,0,1]) #画纬度线

    for info, shape in zip(m.province_info, m.province):
        pname = info['OWNER'].strip('\x00')
        fcname = info['FCNAME'].strip('\x00')
        #if pname != fcname: # 不绘制海岛
        #    continue

        for key in data.keys():
            if key in pname:
                if data[key] == 0:
                    color = '#f0f0f0'
                elif data[key] < 10:
                    color = '#ffaa85'
                elif data[key] <100:
                    color = '#ff7b69'
                elif  data[key] < 1000:
                    color = '#bf2121'
                else:
                    color = '#7f1818'
                break

        poly = Polygon(shape, facecolor=color, edgecolor=color)
        axes.add_patch(poly)

    axes.legend(handles, labels, bbox_to_anchor=(0.5, -0.11), loc='lower center', ncol=4, prop=font)
    axes.set_title(plotname, fontproperties=font)
    FigureCanvasAgg(fig)
    fig.savefig(plotname + '.png')

def plot_distribution2(data):
    """绘制行政区域确诊分布数据"""
    
    
    
    font_14 = FontProperties(fname='res/simhei.ttf', size=14)
    font_11 = FontProperties(fname='res/simhei.ttf', size=11)
    
    width = 1600
    height = 800
    rect = [0.1, 0.12, 0.8, 0.8]
    lat_min = 0
    lat_max = 60
    lon_min = 77
    lon_max = 140
    
    '''全球等经纬投影模式使用以下设置，否则使用上面的对应设置
    width = 3000
    height = 1500
    rect = [0, 0, 1, 1]
    lat_min = -90
    lat_max = 90
    lon_min = 0
    lon_max = 360
    '''
    
    handles = [
            matplotlib.patches.Patch(color='#ffaa85', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#ff7b69', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#bf2121', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#7f1818', alpha=1, linewidth=0),
]
    labels = [ '1-9人', '10-99人', '100-999人', '>1000人']
    
    provincePos = {
        "辽宁省":[121.7,40.9],
        "吉林省":[124.5,43.5],
        "黑龙江省":[125.6,46.5],
        "北京市":[116.0,39.9],
        "天津市":[117.0,38.7],
        "内蒙古自治区":[110.0,41.5],
        "宁夏回族自治区":[105.2,37.0],
        "山西省":[111.0,37.0],
        "河北省":[114.0,37.8],
        "山东省":[116.5,36.0],
        "河南省":[111.8,33.5],
        "陕西省":[107.5,33.5],
        "湖北省":[111.0,30.5],
        "江苏省":[119.2,32.5],
        "安徽省":[115.5,31.8],
        "上海市":[121.0,31.0],
        "湖南省":[110.3,27.0],
        "江西省":[114.0,27.0],
        "浙江省":[118.8,28.5],
        "福建省":[116.2,25.5],
        "广东省":[113.2,23.1],
        "台湾省":[120.5,23.5],
        "海南省":[108.0,19.0],
        "广西壮族自治区":[107.3,23.0],
        "重庆市":[106.5,29.5],
        "云南省":[101.0,24.0],
        "贵州省":[106.0,26.5],
        "四川省":[102.0,30.5],
        "甘肃省":[103.0,35.0],
        "青海省":[95.0,35.0],
        "新疆维吾尔自治区":[85.5,42.5],
        "西藏自治区":[85.0,31.5],
        "香港特别行政区":[115.1,21.2],
        "澳门特别行政区":[112.5,21.2]
    }
    
    fig = matplotlib.figure.Figure()
    fig.set_size_inches(width/100, height/100) # 设置绘图板尺寸
    axes = fig.add_axes(rect)
    
    # 兰博托投影模式，局部
    m = Basemap(projection='lcc', llcrnrlon=77, llcrnrlat=14, urcrnrlon=140, urcrnrlat=51, lat_1=33, lat_2=45, lon_0=100, ax=axes)
    
    # 兰博托投影模式，全图
    #m = Basemap(projection='lcc', llcrnrlon=80, llcrnrlat=0, urcrnrlon=140, urcrnrlat=51, lat_1=33, lat_2=45, lon_0=100, ax=axes)
    
    # 圆柱投影模式，局部
    #m = Basemap(llcrnrlon=lon_min, urcrnrlon=lon_max, llcrnrlat=lat_min, urcrnrlat=lat_max, resolution='l', ax=axes)
    
    # 正射投影模式
    #m = Basemap(projection='ortho', lat_0=36, lon_0=102, resolution='l', ax=axes)
	
	# 全球等经纬投影模式，
    #m = Basemap(llcrnrlon=lon_min, urcrnrlon=lon_max, llcrnrlat=lat_min, urcrnrlat=lat_max, resolution='l', ax=axes)
    #m.etopo()
    
    m.readshapefile('res/china-shapefiles-master/china', 'province', drawbounds=True)
    m.readshapefile('res/china-shapefiles-master/china_nine_dotted_line', 'section', drawbounds=True)
    m.drawcoastlines(color='black') # 洲际线
    m.drawcountries(color='black')  # 国界线
    m.drawparallels(np.arange(lat_min,lat_max,10), labels=[1,0,0,0]) #画经度线
    m.drawmeridians(np.arange(lon_min,lon_max,10), labels=[0,0,0,1]) #画纬度线
    
    pset = set()
    for info, shape in zip(m.province_info, m.province):
        pname = info['OWNER'].strip('\x00')
        fcname = info['FCNAME'].strip('\x00')
        if pname != fcname: # 不绘制海岛
            continue
        
        for key in data.keys():
            if key in pname:
                if data[key] == 0:
                    color = '#f0f0f0'
                elif data[key] < 10:
                    color = '#ffaa85'
                elif data[key] <100:
                    color = '#ff7b69'
                elif  data[key] < 1000:
                    color = '#bf2121'
                else:
                    color = '#7f1818'
                break
        
        poly = Polygon(shape, facecolor=color, edgecolor=color)
        axes.add_patch(poly)
        
        pos = provincePos[pname]
        text = pname.replace("自治区", "").replace("特别行政区", "").replace("壮族", "").replace("维吾尔", "").replace("回族", "").replace("省", "").replace("市", "")
        if text not in pset:
            x,  y = m(pos[0], pos[1])
            axes.text(x,  y, text, fontproperties=font_11, color='#00FFFF')
            pset.add(text)
    
    axes.legend(handles, labels, bbox_to_anchor=(0.5, -0.11), loc='lower center', ncol=4, prop=font_14)
    axes.set_title("2019-nCoV疫情地图", fontproperties=font_14)
    FigureCanvasAgg(fig)
    fig.savefig('2019-nCoV疫情地图.png')


def plot_daily(d, title = 'DailyTotal'):

    date_list, confirm_list, suspect_list, dead_list, heal_list = d
    plt.figure('2019-nCoV疫情统计图表', facecolor='#f4f4f4', figsize=(10, 8))
    plt.title('2019-nCoV '+ title, fontsize=20)

    plt.plot(date_list, confirm_list, label='Confirm')
    plt.plot(date_list, suspect_list, label='Suspected')
    plt.plot(date_list, dead_list, label='Dead')
    plt.plot(date_list, heal_list, label='Heal')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d')) # 格式化时间轴标注
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    plt.grid(linestyle=':') # 显示网格
    plt.legend(loc='best') # 显示图例
    plt.savefig('2019-nCoV_'+title+'.png') # 保存为文件

    plt.show()
    return