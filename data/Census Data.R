rm(list=ls())

library(cancensus)
library(sf)
library(ggplot2)

vectors_16 = list_census_vectors('CA16')
regions = list_census_regions('CA16')


# Vectors:
  # Total Household Income ($)
  # Unemployment Rate
  # Total Population

vectors = c('v_CA16_4985', 'v_CA16_5618', 'v_CA16_401')

census_16 = get_census(dataset='CA16', regions=list(CSD='3520005'),
                       vectors = vectors, level='DA', geo_format = 'sf')

st_write(census_16, 'C:/ENVSOCTY 4GA3 Group Project/CensusData.shp')
