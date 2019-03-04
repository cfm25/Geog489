# Filename: mapping.py
# Author: Charles Moser
# Date: 2/27/2019
# Input 1: Output folder
# Input 2:  List of shapefiles in output folder
# Use: Adds all shapefiles in a folder to an open project map

import arcpy.mp

def add_layers(outFolder, layer_list):

    try:

        aprx = arcpy.mp.ArcGISProject("CURRENT")
        aprxMap = aprx.listMaps()[0]
        #layout = aprx.listLayouts()[0]
        #mapframe = layout.listElements("MAPFRAME_ELEMENT")[0]

        #ext = mapframe.camera.getExtent()
    

        for l in layer_list:
            aprxMap.addDataFromPath(l)
    

        #mapframe.zoomToAllLayers()

    except Exception as err:
        arcpy.AddMessage("Error Aprx. %s" % str(err))
