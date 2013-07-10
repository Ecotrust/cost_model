import main_model as m
import routing_main as r
import landing
from pprint import pprint
import ogr
import gis

def main():
    ### GIS Data
    slope_raster = 'G:\\Basedata\\PNW\\terrain\\slope'
    elevation_raster = 'G:\\Basedata\\PNW\\terrain\\dem_prjr6'
    #slope_raster = '/usr/local/apps/land_owner_tools/lot/fixtures/downloads/terrain/slope.tif'
    #elevation_raster = '/usr/local/apps/land_owner_tools/lot/fixtures/downloads/terrain/dem.tif'

    driver = ogr.GetDriverByName('ESRI Shapefile')
    #property_shp = driver.Open('Data//test_stands.shp', 0)
    property_shp = driver.Open('Data//testarea6.shp', 0)
    property_lyr = property_shp.GetLayer()
    stand_lyr = property_shp.GetLayer()
    feat = stand_lyr.GetFeature(0)
    geom = feat.GetGeometryRef()

    stand_wkt = geom.ExportToWkt()
    area = gis.area(stand_lyr)
    elevation = gis.zonal_stats(elevation_raster, stand_lyr)
    slope = gis.zonal_stats(slope_raster, stand_lyr)

    ### Tree Data ###
    # Harvest Type (clear cut = 0, partial cut = 1)
    PartialCut = 0

    # Hardwood Fraction
    HdwdFractionCT = 0.15
    HdwdFractionSLT = 0.0
    HdwdFractionLLT = 0.0

    # Chip Trees
    RemovalsCT = 200.0
    TreeVolCT = 5.0

    # Small Log Trees
    RemovalsSLT = 100.00
    TreeVolSLT = 70.0

    # Large Log Trees
    RemovalsLLT = 20.00
    TreeVolLLT = 200.00
    
    ### Mill information
    # Can use mill_lyr alone, mill_lyr AND millID, OR mill_Lat and mill_Lon
    mill_shp = driver.Open('Data//mills.shp', 0)
    mill_lyr = mill_shp.GetLayer()
    millID = None
    mill_Lat = None
    mill_Lon = None
    mill_lyr = None
    mill_Lat = 41.2564
    mill_Lon = -123.5677

    # Landing Coordinates 
    landing_coords = landing.landing(property_lyr)

    haulDist, haulTime, coord_mill = r.routing(
        landing_coords,
        millID,
        mill_Lat,
        mill_Lon,
        mill_lyr
    )

    cost = m.cost_func(
        # stand info
        area,
        elevation,
        slope,
        stand_wkt,
        # harvest info
        RemovalsCT,
        TreeVolCT,
        RemovalsSLT,
        TreeVolSLT,
        RemovalsLLT,
        TreeVolLLT,
        HdwdFractionCT,
        HdwdFractionSLT,
        HdwdFractionLLT,
        PartialCut,
        # routing info
        landing_coords,
        haulDist,
        haulTime,
        coord_mill
    )

    pprint(cost)

main()
