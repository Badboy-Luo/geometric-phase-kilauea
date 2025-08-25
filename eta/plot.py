from obspy import read
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from datetime import datetime,timedelta
import math,os
from tqdm import tqdm
from fnmatch import fnmatch
import netCDF4 as nc


def dateRange(beginDate,endDate):
    dates=[]
    dt = datetime.strptime(beginDate,'%Y-%m-%d')
    date = beginDate[:]
    while date<=endDate:
        dates.append(dt)
        dt = dt + timedelta(1)
        date = dt.strftime('%Y-%m-%d')
    return dates

def extract_eta(freq,ref_st,stack,sr):
    etas = np.load(os.path.join('output','%sd_%s.npy'%(stack,ref_st)))
    with open(os.path.join('output','%sd_%s.txt'%(stack,ref_st))) as f:
        cat = f.readlines()
    f.close()
    dates = dateRange(cat[0].split()[0],cat[-1].split()[0])
    freq_len = etas.shape[1]
    eta = np.mean(etas[:,int(freq*(freq_len/(sr/2))):
            int((freq+0.4)*(freq_len/(sr/2)))], axis=-1)
    return dates,eta



stack = '05'
sr = 100
dates = dateRange('2018-01-01','2018-12-31')

xloc,xlabel = [],[]
xloc.append(datetime(2018,1,1))
xlabel.append('2018-01')
xloc.append(datetime(2018,4,1))
xlabel.append('2018-04')
xloc.append(datetime(2018,7,1))
xlabel.append('2018-07')
xloc.append(datetime(2018,10,1))
xlabel.append('2018-10')
xloc.append(datetime(2019,1,1))
xlabel.append('2019-01')


# Plot time-frequency function of \Delta\eta for the reference station of "AHUD"
ref_st = 'AHUD'
etas = np.load(os.path.join('output','%sd_%s.npy'%(stack,ref_st)))
with open(os.path.join('output','%sd_%s.txt'%(stack,ref_st))) as f:
    cat = f.readlines()
f.close()
dates = dateRange(cat[0].split()[0],cat[-1].split()[0])
plt.figure(figsize=[9,4])
plt.rcParams['xtick.direction'] = 'out'
plt.rcParams['ytick.direction'] = 'out'
data_len = etas.shape[1]*2
freqs = np.linspace(0,sr/2,int(data_len/2))
plt.pcolormesh(freqs,dates,etas, shading='auto')
plt.yticks(xloc,xlabel,fontsize=10,rotation=30)
plt.ylim(datetime(2018,1,1),datetime(2019,1,1))
plt.xlim(0.1,50)
plt.xscale('log')
plt.xticks(fontsize=12)
plt.xlabel('Frequency (Hz)',fontsize=16)
cb = plt.colorbar(extend='both')
cb.set_label('$\Delta \eta$ ($rad$)',size=16)
cb.ax.tick_params(labelsize=14)
plt.title('$\Delta \eta (\omega, T)$, ref_sta=%s'%ref_st,weight='bold',fontsize=18)
plt.grid(linestyle='dotted')
plt.savefig('tf_eta.jpg',bbox_inches='tight',dpi=400)



# Plot the averaged \Delta\eta time series over all stations at frequency of 0.6-1.0 Hz
ref_sts = ['SBL','BYL','KKO','OBL','UWE','RIMD','SDH','WRM','HAT','UWB','OTLD',
            'AHUD','CPKD','PUHI','RSDD']
freq = 0.6
plt.figure(figsize=[6,3])
plt.subplots_adjust(hspace=0.3)
plt.tight_layout()
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
eta_all = np.zeros((len(ref_sts),365))
for i in tqdm(range(len(ref_sts))):
    dates,eta = extract_eta(freq,ref_sts[i],stack,sr)
    if i == 0:
        plt.plot(dates,eta,c='gray',alpha=0.6,lw=1,ls='--',zorder=2,label = '$\Delta\eta$ of each reference station')
    else:
        plt.plot(dates,eta,c='gray',alpha=0.6,lw=1,ls='--',zorder=2)
    eta_all[i,:] = eta
    eta_mean = np.mean(eta_all,axis=0)
plt.plot(dates,eta_mean,lw=2,c='k',zorder=3,label='mean $\Delta\eta$')
plt.axvline(datetime(2018,4,26),c='peru',lw=2,alpha=0.6,ls='--',zorder=1,label='pre-eruptive inflation peak')
plt.axvline(datetime(2018,5,4),lw=2,c='peru',alpha=0.7,zorder=1,label='LERZ eruption and Mw6.9 EQ')
plt.axvspan(datetime(2018,5,28),datetime(2018,8,4),color='peru',alpha=0.4,ec='none')
plt.text(datetime(2018,6,1),1.3,'Broad-scale\ncollapses',fontsize=9,weight='bold',color='peru')
plt.axvspan(datetime(2018,1,1),datetime(2018,1,31),color='k',alpha=0.2,ec='none')
plt.text(datetime(2018,1,5),1.5,'Ref',weight='bold',fontsize=12,color='gray')
plt.grid(ls=':',alpha=0.4)
plt.yticks([1.3,1.4,1.5,1.6],fontsize=10)
plt.ylabel('$rad$',fontsize=13)
plt.xticks(xloc,xlabel,fontsize=11)
plt.title('$\Delta \eta(T)$, %s-%s Hz'%(freq,round(freq+0.4,2)),fontsize=14,weight='bold')
plt.legend(loc='lower right',fontsize=8,edgecolor='none')
plt.xlim(datetime(2018,1,1),datetime(2019,1,1))
plt.tight_layout()
plt.savefig('eta_%sHz.pdf'%freq,bbox_inches='tight')
plt.close()




