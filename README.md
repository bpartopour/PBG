# PBG V.2



PBG works based on [Blender](https://www.blender.org/foundation)  therefore, Blender 2.77 or a later version is required.


Input parameters should be adjusted in [parameters.py](https://github.com/bpartopour/PBG/blob/master/parameters.py). 
Make sure the file paths are set to desired directory. 
In online version only a few particle shapes are available. To access other shapes please contact me. 

All files must be kept in the same directory as [pbg.py](https://github.com/bpartopour/PBG/blob/master/pbg.py). However, this multiple instances of [pbg.py](https://github.com/bpartopour/PBG/blob/master/pbg.py). can be run by copying the whole directory.
  
Place [empty.blend](https://github.com/bpartopour/PBG/blob/master/empty.blend) and [PBG.py](https://github.com/bpartopour/PBG/blob/master/pbg.py) and [Capping.py](https://github.com/bpartopour/PBG/blob/master/Capping.py) in your working directory.   

To run the simulation in Console/Terminal (Win or Mac):   
  Make sure you are in the right directory  
  Type: blender -b empty.blend -P PBG.py 
  

To run the simulation interactively in Blender:  
  Run Blender.exe   
  Remove all the objects in the scene, including Camera and Light  
  Change to scripting mode  
  Open PBG.py   
  Run the script     
  
To run the capping.py from Console/Terminal:

  Make sure you are in the right directory  
  Type: blender -b \\working_bed_X.blend -P Capping.py 
  
  
If you are using this package for research or work make sure you refer to our [paper](https://doi.org/10.1016/j.powtec.2017.09.009)

