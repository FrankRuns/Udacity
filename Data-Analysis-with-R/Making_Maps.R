x <- c("ggmap", "rgdal", "rgeos", "maptools", "dplyr", "tidyr", "tmap")
# install.packages(x)
lapply(x, remove.packages)
# install.packages("rgdal")
# library(rgdal)

## export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin"

## export PATH=$PATH:/Library/Frameworks/GDAL.framework/Programs

## Download GDAL complete
## http://www.kyngchaos.com/software:frameworks

## add to path
## export PATH=$PATH:/Library/Frameworks/GDAL.framework/Programs

## Download project
## http://www.kyngchaos.com/software:frameworks

## download package source
## https://cran.r-project.org/web/packages/rgdal/index.html

## instll via
## sudo R CMD INSTALL –configure-args=’–with-proj-include=/usr/local/lib’ rgdal_1.0-7.tar.gz

## rgeos is easier install.packages("rgeos")
## 

## require rgdal.

## http://stackoverflow.com/questions/32132437/rgdal-not-available-for-r-version-3-2-2
## http://www.compmath.com/blog/2010/07/installing-package-on-mac-os-x/

## file:///Users/frankCorrigan/Downloads/intro-spatial-rl.pdf

library(ggplot2); library(rgdal); library(ggmap); library(dplyr); library(RColorBrewer)
setwd("/Users/frankCorrigan/Desktop")
area <- readOGR(dsn = "tl_2012_12_cousub", layer = "tl_2012_12_cousub")
colors <- brewer.pal(9, "BuGn")

names <- levels(area@data$NAME)
area <- area[area$NAME %in% names[-c(81, 86, 96)],]
area.points <- fortify(area, region="NAME")
setwd("/Users/frankCorrigan/Udacity/Data-Analysis-with-R")
counties <- read.csv("florida_counties.csv")
counties$zip <- as.character(counties$zip)

don_data <- left_join(data, counties, by="zip")
don_data <- select(don_data, party, contb_receipt_amt, county)

don_data_pct <- filter(don_data, party %in% c("democrat", "republican")) %>%
  group_by(county, party) %>%
  summarize(sub_total=n()) 
don_data_pct <- filter(don_data_pct, county != "")
don_data_dem <- filter(don_data_pct, party == "democrat")

don_data_totals <- filter(don_data, party %in% c("democrat", "republican")) %>%
  group_by(county) %>%
  summarize(total=n()) 
don_data_totals <- filter(don_data_totals, county != "")

dem <- left_join(don_data_totals, don_data_dem, by="county")
dem_last <- dem %>% mutate(prop = sub_total/total) %>%
  select(county, prop)

# Make dem_last county names look like area county names
test <- "Alachua County"
dem_last$county <- gsub(" County", "", dem_last$county)
colnames(dem_last)[1] <- "id"

# Merge dem_last data with area data
dem_map <- left_join(area.points, dem_last, by='id')

mapage <- get_map(location = c(lon = -83.5, lat = 27.77),
                    color = "color",
                    zoom = 7)

ggmap(mapage) +
      geom_polygon(aes(x = long,
                       y = lat,
                       group = group,
                       fill = prop),
                   data = subset(dem_map, !is.na(prop)),
                   color = "black",
                   alpha = 0.5) +
      labs(x = "Longitude",
           y = "Latitude")


library(ggplot2); library(rgdal); library(rgeos); library(maptools);
library(gpclib); library(ggmap); library(dplyr); library(RColorBrewer)

# Need ggmap, ggplot2, maptools, rgdal, rgeos

setwd("/Users/frankCorrigan/Downloads/cenzcta2010_feb12/")

mapage <- get_map(location = c(lon = -83.5, lat = 27.77), color = "color", zoom = 6)
ggmap(mapage)

flo = readOGR(".","cenzcta2010_feb12") %>% spTransform(CRS("+proj=longlat +datum=WGS84"))
ggplot(data = flo, aes(x = long, y = lat, group = group)) + geom_path()

flo.f <- fortify(flo, region="ZCTA5CE10")

data_small <- select(data, zip, cand_nm, party)

data_small <- filter(data_small, cand_nm %in% c("Obama, Barack", "Romney, Mitt"))

don_data_pct <- filter(data_small, party %in% c("democrat", "republican")) %>%
      group_by(zip, party) %>%
      summarize(sub_total=n()) 
don_data_dem <- filter(don_data_pct, party == "democrat")

don_data_totals <- filter(data_small, party %in% c("democrat", "republican")) %>%
      group_by(zip) %>%
      summarize(total=n()) 

dem <- left_join(don_data_totals, don_data_dem, by="zip")
dem_last <- dem %>% mutate(prop = round(sub_total/total)) %>%
      select(zip, prop) # 0 = rep, 1 = dem

colnames(dem_last)[1] <- "id"

# Merge dem_last data with area datas
dem_map <- left_join(flo.f, dem_last, by='id')

mapage <- get_map(location = c(lon = -83.5, lat = 27.77),
                  color = "color",
                  zoom = 6)

ggplot(dem_map, aes(long, lat, group = group)) + 
      geom_polygon(aes(fill = prop))

ggmap(mapage) + 
      geom_polygon(aes(fill = prop, x = long, y = lat, group = group), 
                   data = dem_map,
                   alpha = 0.6) +
      scale_fill_gradient(low = "red", high = "blue") +
      ggtitle("Majority Party by Zipcode")


# sf example
library(ggmap); library(maptools); library(rgeos); library(dplyr)
setwd("/Users/frankCorrigan/Downloads/sfzipcodes/")

sfMap = map = get_map(location = 'San Francisco', zoom = 12)
sfn = readOGR(".","sfzipcodes") %>% spTransform(CRS("+proj=longlat +datum=WGS84"))

ggplot(data = sfn, aes(x = long, y = lat, group = group)) + geom_path()

slot(sfn, "polygons") <- lapply(slot(sfn, "polygons"), checkPolygonsHoles)
sfn.t <- unionSpatialPolygons(sfn, as.character(sfn$ID))

sfn.f = sfn %>% fortify(region = 'ZIP_CODE')
SFNeighbourhoods  = merge(sfn.f, sfn@data, by.x = 'id', by.y = 'ZIP_CODE')
postcodes = SFNeighbourhoods %>% select(id) %>% distinct()
values = data.frame(id = c(postcodes),
                    value = c(runif(postcodes %>% count() %>% unlist(),5.0, 25.0)))
sf = merge(SFNeighbourhoods, values, by.x='id')
sf %>% group_by(id) %>% do(head(., 1)) %>% head(10)
ggplot(sf, aes(long, lat, group = group)) + 
      geom_polygon(aes(fill = value))
ggmap(sfMap) + 
      geom_polygon(aes(fill = value, x = long, y = lat, group = group), 
                   data = sf,
                   alpha = 0.8, 
                   color = "black",
                   size = 0.2)
