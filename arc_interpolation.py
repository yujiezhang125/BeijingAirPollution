# -*- coding: utf-8 -*-
# @Time    : 2020/05/21
# @Author  : yujiezhang125
# @FileName: arc_interpolation.py
# @Description: Create raster data from climate stations data interpolation (IDW interpolation)
# @Description: Interpolation year from 2000 to 2019, seven climate factors for each year.


import arcpy
from arcpy.sa import *
import os
arcpy.CheckOutExtension("Spatial")

arcpy.env.workspace = r'D:\CityDNA\Data\airpollutiondata\airplt.gdb'
arcpy.env.overwriteOutput = True


for year in range(2000, 2020):
    print str(year) + ' start...'
    isdpath = r'D:\CityDNA\Data\airpollutiondata\isdstn'
    table = os.path.join(isdpath, str(year) + 'stn.xls\\Sheet1$')

    print str(year) + ' make layers and addjoin...'
    arcpy.MakeFeatureLayer_management('isd_select', 'pntlyr')
    arcpy.MakeTableView_management(table, 'tblyr' + str(year))
    arcpy.TableToGeodatabase_conversion('tblyr' + str(year), r'D:\CityDNA\Data\airpollutiondata\airplt.gdb')
    arcpy.AddJoin_management('pntlyr', 'USAF', 'tblyr' + str(year), 'stnid', 'KEEP_COMMON')
    arcpy.CopyFeatures_management('pntlyr', 'stn' + str(year))
    arcpy.Delete_management('pntlyr', str(year) + 'tblyr')

    print str(year) + ' finished!!!'


# make rasters
arcpy.CheckOutExtension("Spatial")
outIDW = Idw("isd_select.shp", "ELEV_M_")
outIDW.save(r"D:\CityDNA\Data\airpollutiondata\isdlite\idwout.tif")


# "tem", "dew", "SLP", 'WD', 'WS', 'skycov', 'pre'
attributes = ["tem", "dew", "SLP", 'WD', 'WS', 'skycov', 'pre']
for year in range(2000, 2020):
    stnfile = 'stn' + str(year) + '.shp'
    print stnfile + ' start...'
    for attr in attributes:
        print 'outIDW...'
        outIDW = Idw(stnfile, attr)
        rastername = attr + str(year)
        outIDW.save(r"D:\CityDNA\Data\airpollutiondata\isdraster\\" + rastername + ".tif")
        print rastername + ' finished!!!'

# extract values to point
arcpy.env.workspace = r'D:\CityDNA\Data\airpollutiondata\airplt.gdb'
arcpy.env.overwriteOutput = True

attributes = ["tem", "dew", "SLP", 'WD', 'WS', 'skycov', 'pre']
for year in range(2000, 2020):
    print str(year) + ' start...'
    arcpy.MakeFeatureLayer_management('Bgridbj', 'lyr')
    arcpy.CopyFeatures_management('lyr', 'Bgridbj' + str(year))
    arcpy.Delete_management('lyr')

    for i in range(len(attributes)):
        print str(year) + attributes[i] + ' extract value to point...'
        rasterpath = r"D:\CityDNA\Data\airpollutiondata\isdraster"  # \dew2000.tif
        raster = os.path.join(rasterpath, attributes[i] + str(year) + '.tif')
        ExtractValuesToPoints("Bgridbj" + str(year), raster, "gridtemp")
        arcpy.AlterField_management("gridtemp", 'RASTERVALU', attributes[i])

        print str(year) + attributes[i] + ' copy feature...'
        arcpy.MakeFeatureLayer_management("gridtemp", 'lyr')
        arcpy.CopyFeatures_management('lyr', 'Bgridbj' + str(year))
        arcpy.Delete_management('lyr')
        arcpy.Delete_management("gridtemp")
        print str(year) + attributes[i] + ' finished!!!'

    print str(year) + ' finished!!!'


# Export attribute table
inputname = r'D:\CityDNA\Data\airpollutiondata\airplt.gdb\gridbj2000'
outputPath = r'D:\CityDNA\Data\airpollutiondata\tables'
outputName = 'gridbj' + '.csv'
arcpy.TableToTable_conversion(inputname, outputPath, outputName)

for year in range(2000, 2020):
    print str(year) + ' start...'
    inputname = r'D:\CityDNA\Data\airpollutiondata\airplt.gdb\Bgridbj' + str(year)
    outputPath = r'D:\CityDNA\Data\airpollutiondata\tables'
    outputName = 'Bgridbj' + str(year) + '.csv'
    arcpy.TableToTable_conversion(inputname, outputPath, outputName)
    print str(year) + ' finished!!!'

