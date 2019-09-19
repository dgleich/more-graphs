Where's Waldo
-------------
These's graphs were generated from SIFT keypoints, using the default parameters of the OpenCV implementation. 

Data Download
-------------
The original files are subject to copywrite, however the imgur album where the original files were collected from can be found at
 - https://imgur.com/gallery/8exqx

Data
----
Each file from the imgur album is stored associated with a file name WaldoMapi, where i is the ith file in the list of the imgur album. All files are post fixed with with .smat for the graph, and .xy for the actual pixel locations of each keypoint. The ith row of the _keypoint_coordinates.xy file links the ith keypoint to a pixel (original floating point locations were floored), these are consistent with the indices in the graphs too. 

Graph Structure
---------------
The graphs are simply a mesh network which links the keypoints together if they're within a 25 pixel radius of one another. This produces an unweighted, undirected graph. 


Dependencies
------------
The only dependencies for these networks are Numpy and OpenCV. To install Numpy, please see their installation page. However to get access to OpenCV's sift implemenation, it's recommended to install through anaconda (which will also install numpy). 

The file "BuildWheresWaldoGraphs.py" can be used to rebuild the graphs using python3, and will run once the map_files_location variable is set in the boiler_plate template section.  



  