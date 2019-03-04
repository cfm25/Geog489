# Filename: multicode.py
# Author: Charles Moser
# Source: Adapted from Lesson 1, Geography 489, Penn State
# Date: 2/27/2019
# Parameter 1: clipper - feature class for clipping other features
# Parameter 2:  tobeclipped - target features to be clipped
# Parameter 3: field - field of clip feature that stores object id's
# Parameter 4: oid - object id's from clip feature
# Parameter 5: outFolder - output folder for clipped features
# Use: This script clips one or more feature classes and writes
#      the clipped features as shapefiles to a user-selected folder

import os, sys
import arcpy
 
def worker(clipper, tobeclipped, field, oid, outFolder): 
    """  
       This is the function that gets called and does the work of clipping the input feature class to one of the polygons from the clipper feature class. 
       Note that this function does not try to write to arcpy.AddMessage() as nothing is ever displayed.  If the clip succeeds then it returns TRUE else FALSE.  
    """
    try:
        desc = arcpy.Describe(tobeclipped)
        name = desc.baseName
        # Create a layer with only the polygon with ID oid. Each clipper layer needs a unique name, so we include oid in the layer name.
        query = '"' + field +'" = ' + str(oid)
        arcpy.AddMessage("current id: " + str(oid))
        arcpy.MakeFeatureLayer_management(clipper, name + "_" + str(oid), query) 
        
        # Do the clip. We include the oid in the name of the output feature class. 
        outFC = outFolder + "\\" + name + str(oid) + ".shp"

        arcpy.Clip_analysis(tobeclipped, name + "_" + str(oid), outFC) 
         
        arcpy.AddMessage("finished clipping:", str(oid)) 
        return True # everything went well so we return True

    except Exception as err:
        arcpy.AddMessage("Error in Worker. %s" % str(err))
        return False
