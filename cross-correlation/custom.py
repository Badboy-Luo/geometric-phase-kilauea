import os
from obspy import read_inventory

def populate(data_folder):
    datalist = sorted(os.listdir(data_folder))
    stationdict = {}
    for di in datalist:
        tmp = os.path.join(data_folder,di)
        net,sta = di.split('.')[0],di.split('.')[1]
        lat,lon = read_inventory(tmp)[0][0].latitude,read_inventory(tmp)[0][0].longitude
        ele = read_inventory(tmp)[0][0].elevation
        stationdict[net+"_"+sta]=[net,sta,lon,lat,ele,'DEG','N/A']
    return stationdict

