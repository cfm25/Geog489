# Filename: scripttool.py
# Author: Charles Moser
# Source: Adapted from Lesson 1, Geography 489, Penn State
# Date: 2/27/2019
# Input 1: Environment (geodatabase)
# Input 2:  polygon feature class for clipping
# Input 3: feature class(s) to be clipped
# Output: path to output folder
# Use: Input polygon feature class to clip multiple feature classes
#   This file imports the "worker" function from the "muticode.py"
#   Python script which calls the Clip tool (data management).
#   Finally, the clipped features are added to an open project map.

import os, sys
import arcpy
import multiprocessing 
from multicode_ import worker
from mapping import add_layers
import glob
import time
start_time = time.time()

# Input parameters
arcpy.env.workspace = arcpy.GetParameterAsText(0)
Path = arcpy.env.workspace

# Feature Class that will serve as clip feature
clipper = arcpy.GetParameterAsText(1)
# Target feature class(s) that will be clipped
tobeclipped = arcpy.GetParameterAsText(2)
# Folder for saving clipped shapefiles
outFolder = arcpy.GetParameterAsText(3)
# List of target feature classes
clipList = tobeclipped.split(';')


def get_install_path():
    ''' Return 64bit python install path from registry (if installed and registered),
        otherwise fall back to current 32bit process install path.
    '''
    if sys.maxsize > 2**32: return sys.exec_prefix #We're running in a 64bit process
  
    #We're 32 bit so see if there's a 64bit install
    path = r'SOFTWARE\Python\PythonCore\2.7'
  
    from _winreg import OpenKey, QueryValue
    from _winreg import HKEY_LOCAL_MACHINE, KEY_READ, KEY_WOW64_64KEY
  
    try:
        with OpenKey(HKEY_LOCAL_MACHINE, path, 0, KEY_READ | KEY_WOW64_64KEY) as key:
            return QueryValue(key, "InstallPath").strip(os.sep) #We have a 64bit install, so return that.
    except: return sys.exec_prefix #No 64bit, so return 32bit path 
    
def mp_handler():

    for item in clipList:
        print("here is the list: " + item)
 
    try: 
        # Create a list of object IDs for clipper polygons 
         
        arcpy.AddMessage("Creating Polygon OID list...") 
        print("Creating Polygon OID list...") 
        clipperDescObj = arcpy.Describe(clipper) 
        field = clipperDescObj.OIDFieldName 
      
        idList = [] 
        with arcpy.da.SearchCursor(clipper, [field]) as cursor: 
            for row in cursor: 
                id = row[0] 
                idList.append(id)
 
        arcpy.AddMessage("There are " + str(len(idList)) + " object IDs (polygons) to process.") 
        print("There are " + str(len(idList)) + " object IDs (polygons) to process.") 
 
        # Create a task list with parameter tuples for each call of the worker function. Tuples consist of the clippper, tobeclipped, field, and oid values.
        
        jobs = []
        for item in clipList:
            tobeclipped = Path + "\\" + item
            for id in idList:
                jobs.append((clipper,tobeclipped,field,id, outFolder)) # adds tuples of the parameters that need to be given to the worker function to the jobs list

        arcpy.AddMessage("Job list has " + str(len(jobs)) + " elements.") 
        print("Job list has " + str(len(jobs)) + " elements.") 
 
        # Create and run multiprocessing pool.

        multiprocessing.set_executable(os.path.join(get_install_path(), 'pythonw.exe')) # make sure Python environment is used for running processes, even when this is run as a script tool
 
        arcpy.AddMessage("Sending to pool") 
        print("Sending to pool") 
 
        cpuNum = multiprocessing.cpu_count()  # determine number of cores to use
        print("there are: " + str(cpuNum) + " cpu cores on this machine") 
  
        with multiprocessing.Pool(processes=cpuNum) as pool: # Create the pool object 
            res = pool.starmap(worker, jobs)  # run jobs in job list; res is a list with return values of the worker function
 
        # If an error has occurred report it 
         
        failed = res.count(False) # count how many times False appears in the list with the return values
        if failed > 0:
            arcpy.AddError("{} workers failed!".format(failed)) 
            print("{} workers failed!".format(failed)) 
         
        arcpy.AddMessage("Finished multiprocessing!") 

 
    except arcpy.ExecuteError:
        # Geoprocessor threw an error 
        arcpy.AddError(arcpy.GetMessages(2)) 
        print("Execute Error:", arcpy.ExecuteError) 
    except Exception as e: 
        # Capture all other errors 
        arcpy.AddError(str(e)) 
        print("Exception:", e)

    # Get list of shapefiles in the output folder
    list_layers = glob.glob(outFolder + "\\" + "*.shp")

    # Call the function to add clipped shapefiles to open project
    add_layers(outFolder, list_layers)

    # Print out total processing time
    arcpy.AddMessage("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':   
    mp_handler()
    











