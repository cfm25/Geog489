# Geog489
Advanced Python Exercises

This repository is for storing code written in fullfillment of requirements for the Penn State GIS course,
GEOG 489, Advanced Python Programming for GIS.

Source code: scripttool.py, scripttool_.py, multicode.py, multicode_.py, mapping.py

The "scripttool.py" script demonstrates multiprocessing. It calls the “multicode.py” script which clips a single target feature class and outputs the results to a user-defined folder. The "scripttool_.py" also demonstrates multi-processing but permits the user to clip a list of feature classes with a single clip feature. Also, this file imports the mapping.py script which will add the clipped features to an open project map. The Geog489_Lesson1A.tbx file is an ArcGIS Pro toolbox. The toolbox has two tools. The first tool, "Clipper", uses the scriptool.py and multicode.py files to demonstrate multiprocessing by clipping a single user-selected feature class, while the second tool, "Clipper Multi-input", demonstrates multiprocessing by clipping a list of user-designated feature classes and imports the mapping module to add the clipped features to an open project map.
