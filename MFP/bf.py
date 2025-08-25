import os
import numpy as np
from geopy import distance
from scipy import fftpack
from obspy.signal.filter import envelope
import matplotlib.pyplot as plt
from obspy import read,read_inventory
from tqdm import tqdm
import cmocean
import warnings
warnings.filterwarnings('ignore')


def moving_average(data, length):
    window = np.ones(int(length))/float(length)
    re = np.convolve(data, window, 'same')
    return re

def normalization(data):
    data = data/np.max(np.abs(data))
    return data



lat0 = 19.41
lon0 = -155.28
latrange = [-0.042,0.055]
lonrange = [-0.05,0.04]
ps = 70
qs = 70
uy = np.linspace(latrange[0]+lat0, latrange[1]+lat0, ps)
ux = np.linspace(lonrange[0]+lon0, latrange[1]+lon0, qs)
dt = 5
fz = 100
vel = 1000  # m/s     
maxlag = 40

yr = 2018
dates = ['2018-04-01']   # map the power map for a selected date 


# read lon./lat. for all stations from the .xml files in "station"
xmls = [file for file in os.listdir('station') if file.endswith('xml')]
lats,lons = [],[]
for xml in xmls:
    lat = read_inventory(os.path.join('station',xml))[0][0].latitude
    lon = read_inventory(os.path.join('station',xml))[0][0].longitude
    lats.append(lat)
    lons.append(lon)


# set the path to the folder that includes all daily CCFs for all station pairs 
path = 'ccf'
pairs = [file for file in os.listdir(path) if file.startswith('HV')]

for i in range(len(dates)):

    plt.figure(figsize=[5.2,4.8])
    plt.tick_params(direction='out')    
    bf_pair = np.ones((ps,qs))
    for pair in tqdm(pairs):
        line = pair.split('_')
        st1,st2 = line[1],line[3]
        lat1 = read_inventory(os.path.join('station','HV.'+st1+'.xml'))[0][0].latitude
        lon1 = read_inventory(os.path.join('station','HV.'+st1+'.xml'))[0][0].longitude
        lat2 = read_inventory(os.path.join('station','HV.'+st2+'.xml'))[0][0].latitude
        lon2 = read_inventory(os.path.join('station','HV.'+st2+'.xml'))[0][0].longitude
        dist = distance.distance((lat1,lon1), (lat2,lon2)).m
        try:
            st = read(os.path.join(path,pair,dates[i]+'.MSEED'))
        except FileNotFoundError:
            print('------Missing %s------'%pair)
            continue
        tr = st[0].normalize().data
        tr_en = envelope(tr)**2

        bf = np.zeros((ps,qs))
        for p in range(ps):
            for q in range(qs):
                d1 = distance.distance((lat1,lon1), (uy[p],ux[q])).m
                d2 = distance.distance((lat2,lon2), (uy[p],ux[q])).m
                deltat = (d2-d1)/vel
                tindex = int((deltat+maxlag)*fz)
                bf[p,q] = np.sum(tr_en[int(tindex-dt*fz) : int(tindex+dt*fz)])**1
                
        bf_pair *= bf
    bf_pair /= np.max(bf_pair)

    im = plt.pcolormesh(ux,uy,bf_pair,cmap='Blues',vmin=0,vmax=1)
    plt.scatter(lons,lats,marker='v',color='k',ec='k',lw=2,alpha=0.8,s=200)
    CS = plt.contour(ux,uy,bf_pair,levels=[0.6],colors=['white'])
    plt.clabel(CS,inline=True,fmt='%.1f',fontsize=11)
    if yr == 2018:
        plt.text(-155.307,19.395,'Lava lake\n(2008-2018)',color='r',fontsize=13,weight='bold',zorder=3)
        plt.plot([-155.279046248,-155.288],[19.4039734341,19.396],lw=0.5,c='r')
    elif yr == 2019:
        plt.text(-155.307,19.398,'No lava lake',color='gray',fontsize=13,weight='bold',zorder=3)
    else:
        plt.text(-155.307,19.394,'New lava lake\n(2020-)',color='r',fontsize=13,weight='bold',zorder=3)
        plt.plot([-155.279046248,-155.290],[19.4039734341,19.401],lw=0.5,c='r')
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.xlim(lon0+lonrange[0],lon0+lonrange[1])
    plt.ylim(lat0+latrange[0],lat0+latrange[1])
    plt.title(dates[i],fontsize=18,weight='bold')
    plt.text(-155.325,19.455,'Summit',fontsize=16,fontstyle='italic',weight='bold')

    # cbar = plt.colorbar(im,orientation='horizontal')
    # cbar.set_label('Normalized MFP power',fontsize=14)
    # cbar.ax.tick_params(labelsize=12)

    # plt.suptitle('Noise source energy localization',fontsize=18,weight='bold')
    plt.tight_layout()
    plt.savefig('%s.jpg'%dates[i],dpi=300,bbox_inches='tight')
    plt.close()



