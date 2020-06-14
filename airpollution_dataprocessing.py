# -*- coding: utf-8 -*-
# @Time    : 2020/05/21
# @Author  : yujiezhang125
# @FileName: airpollution_dataprocessing.py
# @Description: Recalculate raw data to annual data from 2000 to 2019 (PM2.5 condensation and seven climate factors)
# @Description:  Extract climate data from raster data after 'arc_interpolation.py'
# @Description:  Concat 2000-2019 data by key as year and export.

import pandas as pd
import numpy as np
import xlwt
import os

os.chdir(r'D:\CityDNA\Data\airpollutiondata')
path = r'D:\CityDNA\Data\airpollutiondata'
stn = pd.read_excel(r"D:\CityDNA\Data\airpollutiondata\isdlite\isd_select.xlsx")['USAF'].tolist()[0:37]
years = range(2000, 2020)


# input raw climate data (isd)
for year in years:
    print(str(year) + " start...")
    xlswrite = pd.read_excel(r"D:\CityDNA\Data\airpollutiondata\isdstn\df.xlsx")
    for i in range(len(stn)):
        print("stn" + str(i) + "...")
        stnnum = stn[i]
        isdpath = r"D:\CityDNA\Data\airpollutiondata\isdlite\china_isd_lite_" + str(year) + "\\china_isd_lite_" + str(year)
        isdfile = str(stnnum) + "-99999-" + str(year)
        if isdfile in os.listdir(isdpath):
            table = pd.read_table(os.path.join(isdpath, isdfile), header=None, delim_whitespace=True)
            table[table == -9999] = 0
            table[table == -1] = 0
            sums = table.iloc[:, 11].sum()
            xlswrite['pre'][i] = sums/10

            table[table == 0] = np.nan
            means = np.nanmean(table, axis=0)
            xlswrite['stnid'][i] = stnnum
            xlswrite['tem'][i] = means[4] / 10
            xlswrite['dew'][i] = means[5] / 10
            xlswrite['SLP'][i] = means[6] / 10
            xlswrite['WD'][i] = means[7]
            xlswrite['WS'][i] = means[8] / 10
            xlswrite['skycov'][i] = means[9]

        else:
            print(str(year) + " year " + str(isdfile) + " doesn't exist...")

    xlswrite.to_excel(os.path.join(path, "isdstn") + '\\' + str(year) + 'stn.xls')


# deal with PM2.5 data. calculate annual mean value from month data
mon = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
mon = ['01', '02', '03', '04', '05', '06', '07', '09', '10', '11', '12']
pmpath = r'D:\CityDNA\Data\airpollutiondata\Beijing_monthly_PM-1km'
year = 2019  # 2005年少一月数据， 2000年少前三月数据， 2018缺少8月数据
for year in range(2019, 2020):
    print(str(year) + ' start...')
    base = pd.read_csv(r'D:\CityDNA\Data\airpollutiondata\Beijing_monthly_PM-1km\Beijing_PM_' + str(year) + '01.csv')
    base = base.iloc[:, [0, 1]]
    for i in range(1, len(mon)):
        pmname = 'Beijing_PM_' + str(year) + mon[i] + '.csv'
        tbadd = pd.read_csv(os.path.join(pmpath, pmname))
        tbadd = tbadd.iloc[:, [0, 1]]
        tb = pd.merge(base, tbadd, how='outer', on='ID', sort=False)
        base = tb

    print(str(year) + ' calculate mean value...')
    for j in range(len(tb)):
        tb.loc[j, 'annual'] = tb.iloc[j, 1:13].mean()

    print(str(year) + ' write in excel...')
    ann = tb.loc[:, ['ID', 'annual']]
    ann.to_excel(os.path.join(pmpath, "ba" + str(year) + '.xls'))
    print(str(year) + ' finished!!!')

# After run 'arc_interpolation.py' ====================================================================================
# merge climate data with PM2.5 data
tbpath = r'D:\CityDNA\Data\airpollutiondata\mergedtables'
for year in range(2000, 2020):
    print(str(year) + ' start...')
    base = pd.read_csv(r'D:\CityDNA\Data\airpollutiondata\tables\Bgridbj' + str(year) + '.csv')
    base[['ID']] = base[['ID']].round()
    tbadd = pd.read_excel(r'D:\CityDNA\Data\airpollutiondata\Beijing_monthly_PM-1km\ba' + str(year) + '.xls')

    tb = pd.merge(base, tbadd, how='inner', on='ID', sort=False)
    tb = tb.drop(columns=['OID', 'Unnamed: 0'])
    tb = tb.rename(columns={'annual': 'pm'})

    tb.to_excel(os.path.join(tbpath, "Btb" + str(year) + '.xls'))
    print(str(year) + ' finished!!!')

# check data row number
for year in range(2000, 2020):
    tb = pd.read_excel(r'D:\CityDNA\Data\airpollutiondata\mergedtables\Btb' + str(year) + '.xls')
    print(str(year) + ' uniqueID ' + str(len(tb['ID'].unique())))

# Concat and export
frames = []
for year in range(2000, 2020):
    frames.append(pd.read_excel(r'D:\CityDNA\Data\airpollutiondata\mergedtables\Btb' + str(year) + '.xls'))

keyvalue = []
for year in range(2000, 2020):
    keyvalue.append(str(year))

result = pd.concat(frames, keys=keyvalue)
result.to_csv(r'D:\CityDNA\Data\airpollutiondata\mergedtables\Bpmdata0609.csv')

