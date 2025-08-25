from obspy import read
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from scipy.stats import pearsonr
from datetime import datetime,timedelta
import math,os
from tqdm import tqdm
from fnmatch import fnmatch
import pandas as pd

def dateRange(beginDate,endDate):
    dates=[]
    dt = datetime.strptime(beginDate,'%Y-%m-%d')
    date = beginDate[:]
    while date<=endDate:
        dates.append(dt)
        dt = dt + timedelta(1)
        date = dt.strftime('%Y-%m-%d')
    return dates

# Loop over all reference stations
ref_sts = ['SBL','BYL','KKO','OBL','UWE','RIMD','SDH','WRM','HAT','UWB','OTLD',
            'AHUD','CPKD','PUHI','RSDD']
stack = '05'
sr = 100

# Set the total time range for \Delta\eta calculation
dates = dateRange('2018-01-01','2018-12-31')

plt.figure(figsize=[5.3,9.5])
plt.subplots_adjust(hspace=0.3)
plt.tight_layout()
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

for n in tqdm(range(len(ref_sts))):
    # Set the path to folder that includes cross-correlations for all station pairs
    path = 'STACKS/01/0%s_DAYS/ZZ'%stack
    pairs = [file for file in os.listdir(path) if fnmatch(file,'*%s*'%ref_sts[n])]

    # Build the reference vector
    ref_mag = 0
    ref_allday = []
    
    # Set the reference time period as January 2018
    for ref_d in dateRange('2018-01-01','2018-01-31'):
        ref_daily_vectors = []
        num = 0
        for i in range(len(pairs)):
            try:
                st = read(os.path.join(path,pairs[i],str(ref_d).split()[0]+'.MSEED'))
            except FileNotFoundError:
                num = 0
                break
            num += 1
            data = st[0].data
            f = fft(data)[:int(len(data)/2)]
            ref_daily_vectors.append(f)
            ref_mag += abs(f)**2
        if num == 0:
            continue
        else:
            ref_allday.append(np.array(ref_daily_vectors)/np.sqrt(ref_mag))
    ref_vectors = np.mean(np.array(ref_allday),axis=0)


    # Calculate daily \Delta\eta relative to the reference time period 
    etas = []
    for d in tqdm(range(len(dates))):
        sum_mag = 0
        vectors = []
        for i in range(len(pairs)):
            num = len(pairs)
            try:
                st = read(os.path.join(path,pairs[i],str(dates[d]).split()[0]+'.MSEED'))
                data = st[0].data
                f = fft(data)[:int(len(data)/2)]
                vectors.append(f)
                sum_mag += abs(f)**2
            except FileNotFoundError:
                num = 0
                break
        if num == len(pairs):
            vectors = np.array(vectors)/np.sqrt(sum_mag)
            eta = []
            for f in range(vectors.shape[1]):
                cdot = np.dot( np.conj([ref_vectors[:,f]]), vectors[:,f] )
                try:
                    eta.append(math.acos(cdot.real))
                except ValueError:
                    print('---Value Limit Warning---')
                    eta.append(math.acos(1))
            etas.append(np.array(eta))
        else:
            etas.append(np.zeros_like(eta) * np.nan)
    etas = np.array(etas)
    

    # save eta as .npy format into "output"
    if not os.path.exists('output'):
        os.makedirs('output')
    np.save(os.path.join('output','%sd_%s.npy'%(stack,ref_sts[n])), etas)
    with open(os.path.join('output','%sd_%s.txt'%(stack,ref_sts[n])), 'a+') as f:
        for d in dates:
            f.write(str(d).split()[0] + '\n')
    f.close()
