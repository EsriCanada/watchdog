from geotrigger import GeotriggerClient
import datetime
import arcpy
import urllib
import os
import sys
import shapefile
import json
import urllib2

def createGeotriggerPolys(scratchWorkspace):

    # Overwrite pre-existing files
    arcpy.env.overwriteOutput = True

    snoUrl = "http://geo.weather.gc.ca/geomet/?SERVICE=WMS&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=FALSE&STYLES=&VERSION=1.1.1&LAYERS=RADAR_RSNO&WIDTH=2048&HEIGHT=2048&SRS=EPSG:3857&BBOX=-16784277.92698697,5022834.091988032,-3810773.9902040344,17996338.028770965"
    raiUrl = "http://geo.weather.gc.ca/geomet/?SERVICE=WMS&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=FALSE&STYLES=&VERSION=1.1.1&LAYERS=RADAR_RRAI&WIDTH=2048&HEIGHT=2048&SRS=EPSG:3857&BBOX=-16784277.92698697,5022834.091988032,-3810773.9902040344,17996338.028770965"

    snoFile = os.path.join(scratchWorkspace,'SNO.png')
    raiFile = os.path.join(scratchWorkspace,'RAI.png')

    snoShp = os.path.join(scratchWorkspace,'SNO.shp')
    raiShp = os.path.join(scratchWorkspace,'SNO.shp')

    if (os.path.exists(snoFile)):
        os.remove(snoFile)

    if (os.path.exists(raiFile)):
        os.remove(raiFile)


    urllib.urlretrieve(snoUrl, snoFile)
    urllib.urlretrieve(raiUrl, raiFile)

    if (arcpy.Exists(snoShp)):
        arcpy.Delete_management(snoShp)

    if (arcpy.Exists(raiShp)):
        arcpy.Delete_management(raiShp)

    arcpy.RasterToPolygon_conversion(os.path.join(snoFile,'Band_1'),os.path.join('in_memory','snob1'),"NO_SIMPLIFY","Value")
    arcpy.RasterToPolygon_conversion(os.path.join(snoFile,'Band_2'),os.path.join('in_memory','snob2'),"NO_SIMPLIFY","Value")
    arcpy.RasterToPolygon_conversion(os.path.join(snoFile,'Band_3'),os.path.join('in_memory','snob3'),"NO_SIMPLIFY","Value")

    arcpy.Intersect_analysis(os.path.join('in_memory','snob1 #;in_memory','snob2 #;in_memory','snob3 #'),os.path.join('in_memory','sno_all'),"ALL","#","INPUT")
    arcpy.MakeFeatureLayer_management(os.path.join('in_memory','sno_all'),os.path.join('in_memory','sno_allfl'))

    arcpy.RasterToPolygon_conversion(os.path.join(raiFile,'Band_1'),os.path.join('in_memory','raib1'),"NO_SIMPLIFY","Value")
    arcpy.RasterToPolygon_conversion(os.path.join(raiFile,'Band_2'),os.path.join('in_memory','raib2'),"NO_SIMPLIFY","Value")
    arcpy.RasterToPolygon_conversion(os.path.join(raiFile,'Band_3'),os.path.join('in_memory','raib3'),"NO_SIMPLIFY","Value")

    arcpy.Intersect_analysis(os.path.join('in_memory','raib1 #;in_memory','raib2 #;in_memory','raib3 #'),os.path.join('in_memory','rai_all'),"ALL","#","INPUT")
    arcpy.MakeFeatureLayer_management(os.path.join('in_memory','rai_all'),os.path.join('in_memory','rai_allfl'))

    arcpy.AddField_management(os.path.join('in_memory','sno_allfl'),"severity","SHORT")
    arcpy.AddField_management(os.path.join('in_memory','rai_allfl'),"severity","SHORT")

    arcpy.CopyFeatures_management(os.path.join('in_memory','sno_allfl'),os.path.join(scratchWorkspace,'sno_allfl.shp'))
    arcpy.CopyFeatures_management(os.path.join('in_memory','rai_allfl'),os.path.join(scratchWorkspace,'rai_allfl.shp'))

    arcpy.CalculateField_management(os.path.join(scratchWorkspace,'sno_allfl.shp'),"severity","sev( !gridcode!, !gridcode_1!, !gridcode_2!)","PYTHON_9.3","def sev(r,g,b):\n    if (r==154 and g == 0 and b == 154):\n        return 100\n    elif (r==153 and g == 0 and b == 153):\n        return 100\n    elif  (r==154 and g == 48 and b == 203):\n        return 64\n    elif  (r==154 and g == 48 and b == 204):\n        return 64\n    elif  (r==255 and g == 1 and b == 154):\n        return 50\n    elif  (r==255 and g == 0 and b == 0):\n        return 32\n    elif  (r==255 and g == 98 and b == 0):\n        return 24\n    elif  (r==255 and g == 154 and b == 0):\n        return 16\n    elif  (r==255 and g == 204 and b == 0):\n        return 12\n    elif  (r==255 and g == 255 and b == 52):\n        return 8\n    elif  (r==0 and g == 98 and b == 0):\n        return 4\n    elif  (r==0 and g == 102 and b == 0):\n        return 4\n    elif  (r==0 and g == 154 and b == 0):\n        return 2\n    elif  (r==0 and g == 153 and b == 0):\n        return 2\n    elif  (r==0 and g == 204 and b == 0):\n        return 1\n    elif  (r==0 and g == 255 and b == 101):\n        return 0\n    elif  (r==0 and g == 255 and b == 102):\n        return 0\n    else:\n        return -1\n")

    arcpy.CalculateField_management(os.path.join(scratchWorkspace,'rai_allfl.shp'),"severity","sev( !gridcode!, !gridcode_1!, !gridcode_2!)","PYTHON_9.3","def sev(r,g,b):\n    if (r==154 and g == 0 and b == 154):\n        return 100\n    elif (r==153 and g == 0 and b == 153):\n        return 100\n    elif  (r==154 and g == 48 and b == 203):\n        return 64\n    elif  (r==154 and g == 48 and b == 204):\n        return 64\n    elif  (r==255 and g == 1 and b == 154):\n        return 50\n    elif  (r==255 and g == 0 and b == 0):\n        return 32\n    elif  (r==255 and g == 98 and b == 0):\n        return 24\n    elif  (r==255 and g == 154 and b == 0):\n        return 16\n    elif  (r==255 and g == 204 and b == 0):\n        return 12\n    elif  (r==255 and g == 255 and b == 52):\n        return 8\n    elif  (r==0 and g == 98 and b == 0):\n        return 4\n    elif  (r==0 and g == 102 and b == 0):\n        return 4\n    elif  (r==0 and g == 154 and b == 0):\n        return 2\n    elif  (r==0 and g == 153 and b == 0):\n        return 2\n    elif  (r==0 and g == 204 and b == 0):\n        return 1\n    elif  (r==0 and g == 255 and b == 101):\n        return 0\n    elif  (r==0 and g == 255 and b == 102):\n        return 0\n    else:\n        return -1\n")

    arcpy.DefineProjection_management(os.path.join(scratchWorkspace,'sno_allfl.shp'), "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]")

    arcpy.Project_management(os.path.join(scratchWorkspace,'sno_allfl.shp'),os.path.join(scratchWorkspace,'sno_projected.shp'),"GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]","#","PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]")

    arcpy.DefineProjection_management(os.path.join(scratchWorkspace,'rai_allfl.shp'), "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]")

    arcpy.Project_management(os.path.join(scratchWorkspace,'rai_allfl.shp'),os.path.join(scratchWorkspace,'rai_projected.shp'),"GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]","#","PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]")


    return

def createWeatherTriggers(workspace, gt):
    # Create snow geoJSON
    snoLoc = os.path.join(workspace, 'sno_projected.shp')

    # read the shapefile
    reader = shapefile.Reader(snoLoc)
    fields = reader.fields[1:]
    fieldNames = [field[0] for field in fields]
    snoShapes = []
    st = datetime.datetime.now().isoformat()
    # set for 1 minute
    et =  (datetime.datetime.now() + datetime.timedelta(minutes = 1)).isoformat()

    for sr in reader.shapeRecords():
        atr = dict(zip(fieldNames, sr.record))
        # set a severity level
        if atr['severity'] >= 1:
            geom = sr.shape.__geo_interface__

            shape = json.dumps(dict(geojson=geom), indent=4)
            # buffer.append(dict(type="Feature", geojson=geom, properties=atr))
            temp = {
                'condition': {
                    'geo': shape,
                    'direction': 'enter',
                    'fromTimestamp': st,
                    'toTimestamp': et
                },
                'action': {
                    'notification': {
                        'text': 'Warning: Severe snow ahead.'
                    }
                },
                "times": 1,
                'setTags': ['snow']
            }
            snoShapes.append(temp)


    # Create snow geoJSON
    raiLoc = os.path.join(workspace, 'rai_projected.shp')

    # read the shapefile
    reader = shapefile.Reader(raiLoc)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    raiShapes = []
    st = datetime.datetime.now().isoformat()
    # set for 1 minute
    et =  (datetime.datetime.now() + datetime.timedelta(minutes = 1)).isoformat()
    for sr in reader.shapeRecords():
        atr = dict(zip(fieldNames, sr.record))
        # Set a severity level
        if atr['severity'] >= 2:
            geom = sr.shape.__geo_interface__
            shape = json.dumps(dict(geojson=geom), indent=4)
            temp = {
                'condition': {
                    'geo': shape,
                    'direction': 'enter',
                    'fromTimestamp': st,
                    'toTimestamp': et
                },
                'action': {
                    'notification': {
                        'text': 'Warning: Severe rain ahead.'
                    }
                },
                "times": 1,
                'setTags': ['rain']
            }
            raiShapes.append(temp)

    for trigger in snoShapes:
        snoTrigger = gt.request('trigger/create', trigger)
    for trigger in raiShapes:
        raiTrigger = gt.request('trigger/create', trigger)

    return

def createMASASTriggers(workspace, gt):

    maxAgeDays = 90

    codes = {
        # "56":"incident.aviation.aircraftCrash",
        "16":"incident.fire",
        "84":"incident.fire.forestFire",
        "85":"incident.fire.hotSpot",
        "86":"incident.fire.industryFire",
        "87":"incident.fire.smoke",
        "88":"incident.fire.urbanFire",
        "89":"incident.fire.wildFire",
        "17":"incident.flood",
        # "23":"incident.meteorological.fog",
        # "123":"incident.meteorological.hail",
        # "131":"incident.meteorological.thunderstorm",
        # "135":"incident.meteorological.snowSquall",
        # "139":"incident.meteorological.tornado",
        # "27":"incident.railway",
        # "152":"incident.railway.railwayAccident",
        "29":"incident.roadway",
        "154":"incident.roadway.bridgeClosure",
        "155":"incident.roadway.hazardousRoadConditions",
        "156":"incident.roadway.roadwayAccident",
        "157":"incident.roadway.roadwayClosure"
    }

    codelist = []
    for code in codes:
        codelist.append(code)

    pointsUrl = "http://74.216.225.117/arcgis/rest/services/MASAS/Points/MapServer/0/query?where=type%20in%20("+",".join(codelist)+")&outFields=*&outSR=4326&orderByFields=UPDATED+DESC&f=json"


    response = urllib2.urlopen(pointsUrl)
    jsonResponse = response.read()
    features = json.loads(jsonResponse)['features']
    geotriggers = []


    for f in features:
        tDate = datetime.datetime.utcfromtimestamp(f['attributes']['UPDATED']/1000)
        tNow = datetime.datetime.now()
        tDelta = tNow - tDate
        if tDelta.days < maxAgeDays:
            tagType = str(f['attributes']['TYPE'])
            if (codes[tagType].split('.')[1] == 'fire'):
                tag = 'fire'
                text = "Warning: Fire ahead."
            elif (codes[tagType].split('.')[1] == 'flood'):
                tag = 'flood'
                text = "Warning: Flood ahead."
            else:
                tag = 'roads'
                text = "Warning: Road obstruction ahead."
            trigger = {
                'condition': {
                    'geo': {
                        'longitude': f['geometry']['x'],
                        'latitude': f['geometry']['y'],
                        'distance': 2000
                    },
                    'direction': 'enter'
                },
                'action': {
                    'notification': {
                        'text': text
                    }
                },
                "times": 1,
                'setTags': [tag]

                # 'masas_id':f['attributes']['ID'],
                # 'type':codes[str(f['attributes']['TYPE'])]
            }
            geotriggers.append(trigger)

    for trigger in geotriggers:
        masasTrigger = gt.request('trigger/create', trigger)

    return

def deleteOldTriggers(triggerArray, gt):
    # get a list of all pre-existing triggers
    oldTriggers = gt.request('trigger/list', {
                             'tags': triggerArray
    })

    # delete all old records
    triggersDeleted = gt.request('trigger/delete', {
               'triggerIds': [t['triggerId'] for t in oldTriggers['triggers']]
    })
# Set Workspace
workspace = "C:\\WatchDog\\Python\\Data"

# Create a GeotriggerClient as an Application
gt = GeotriggerClient("rv74pSMm7KXpsbwk", "baa9d0ce222f479f843ea0051b2cf5f8")

createGeotriggerPolys(workspace)

# All tags to be deleted every 10 minutes
triggerArray = ['rain', 'snow', 'fire', 'roads', 'flood']

deleteOldTriggers(triggerArray, gt)
createWeatherTriggers(workspace, gt)
createMASASTriggers(workspace, gt)
