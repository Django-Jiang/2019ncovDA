import os
import conda

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib

import time
import json
import requests
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.figure
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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