# PBG
PBG is working based on [Blender](https://www.blender.org/foundation)  therefore, Blender 2.77 or a later version is required.


Input parameters should be adjusted in [parameters.py](https://github.com/bpartopour/PBG/blob/master/parameters.py). 
Make sure the file paths are set to desired directory. 
In online version only a few particle shapes are available. To access other shapes please contact me. 

Download all the files and place all except [empty.blend](https://github.com/bpartopour/PBG/blob/master/empty.blend) and [PBG.py](https://github.com/bpartopour/PBG/blob/master/empty.blend) in:  
  Blender/Contents/Resources/2.78/scripts/modules.  
  
Place [empty.blend](https://github.com/bpartopour/PBG/blob/master/empty.blend) and [PBG.py](https://github.com/bpartopour/PBG/blob/master/empty.blend) in your working directory.   

To run the simulation in Console/Terminal (Win or Mac):   
  Make sure you are in the right directory  
  Type: blender -b empty.blend -P PBG.py   

To run the simulation interactively in Blender:  
  Run Blender.exe   
  Remove all the objects in the scene, icluding Camera and Light  
  Change to scripting mode  
  Open PBG.py   
  Run the script     
  
If you are using this package for research or work make sure you refer to our [paper](https://doi.org/10.1016/j.powtec.2017.09.009)
