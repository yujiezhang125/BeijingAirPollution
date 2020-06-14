1 Code: 

 -- airpollution_dataprocessing.py [ !! Python 3.7 !! ]

 -- arc_interpolation.py [ !! Python 2.7 !! ]

2 Description:

- Preprocess and clean seven climate factors(temperature, dew temperature, sea level pressure, wind direction, wind speed, sky cloud coverage, precipitation) from 2000 to 2019.
- In order to create raster data within Beijing boundary range, interpolate(Inverse Distance Weight) the climate data from several meteorological stations around Beijing area.
- Extract climate value from raster data to Beijing grid data with PM2.5 value.
- Export and combine data sets from 2000 to 2019 according to key column as "year".

3 Input Data: 

| Data                                            | Type      | Source                    |
| ----------------------------------------------- | --------- | ------------------------- |
| Climate data from Chine meteorological stations | txt       | https://quotsoft.net/air/ |
| Beijing grid data with PM2.5 value              | excel     |                           |
| Beijing boundary data                           | shapefile |                           |

