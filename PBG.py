##

print('*******************************************',"\n"
      "Packed bed generator module (v-1.1)","\n"
      "by B Partopour & AG Dixon†", "\n"
      "Heat and Mass Transfer Lab","\n"
      "Worcester Polytechnic Institute","\n"
      "Reference : https://doi.org/10.1016/j.powtec.2017.09.009","\n"
      '*********************************************'
)
#Main Program

import sys
import os
CurrentDir = os.getcwd()	#get directory in which PBG.py is stored
sys.path.append(CurrentDir) #Add filepath to system path
print(CurrentDir, "added to system path.") #Report to user

import parameters

import bpy 
import importlib
from radial_voidage import radial_voidage
from Rigidbody_generator import tube_generation
from Rigidbody_generator import part_generation
from Simulator import steady_state
from Simulator import rigidbody_simulation
from bed_properties import angle_distribution

# Reloading parameters in case of re-runs
if "parameters" in locals():
    importlib.reload(parameters)
if "radial_porosity" in locals():
    importlib.reload(radial_porosity)

print("Welcome to the generator")   
print("Initializing the parameters ...")
#Geometry input parameters

Particle_type = str()
Particle_type = parameters.Particle_type
cyl_radius = parameters.cyl_radius
cyl_depth = parameters.cyl_depth
number_of_particle = parameters.number_of_particle
#..................................................

#Generating the Tube
tube_generation(cyl_radius, cyl_depth)
#..................................................

bpy.context.scene.frame_end = 50000
bpy.context.scene.rigidbody_world.point_cache.frame_end = 50000
if cyl_radius < 5:
    last_particle_drop_frame = int((number_of_particle)*10)
else: 
    last_particle_drop_frame = int((number_of_particle / 5) * 10)

#generating the particles and filling up the tube
print("Filling up the bed....")
print("Solver iterations per step: ",bpy.context.scene.rigidbody_world.solver_iterations) 
simulation_current_frame = rigidbody_simulation(Particle_type, last_particle_drop_frame)

bpy.ops.object.select_by_type( type = 'MESH')
#continuing the simulation till steady-state (condition: max particle velocity < 0.01)
print("Reaching the steady_state condition")
distance=steady_state(simulation_current_frame)
bpy.ops.object.select_all(action = 'TOGGLE')#removing the container
if parameters.remove_the_tube == True:
    bpy.data.objects['Cylinder'].select = True
    bpy.ops.object.delete(use_global = False)

#Do we want to get the angle distribution? if so, in parameters.py set the angle_dist to True

if parameters.angle_dist == True:
    print("Calculating the particles angle distributions in the bed...")
    bpy.ops.object.select_by_type( type = 'MESH')
    file_name = parameters.file_name
    angle_distribution(file_name)
    
    
#Saving the blender file to have the packing with separated particles
print("Saving a copy of the packing...")
bpy.ops.wm.save_as_mainfile(filepath = parameters.blender_file_path)
    
#to export the bed uncomment the next 2 lines: 
#bpy.ops.object.select_all(action = 'TOGGLE')
print("Exporting the geometry as a STL file...")
bpy.ops.export_mesh.stl(filepath=parameters.file_path, check_existing=True, axis_forward='Y', axis_up='Z', filter_glob= ".STL", global_scale=1, ascii=False, use_mesh_modifiers=True)

#radial porosity measurment
decision = ''
while decision != 'Yes' and decision != 'No':
    decision = input('Do you want to calculate the radial voidage of the bed (this might take more than an hour)? Yes, No?')
    if decision != 'Yes' and decision != 'No':
        print("your answer is not acceptable, please enter Yes or No")

if decision == 'Yes':
    print("calculating radial porosity ...")
    radial_voidage()



print("Done!")
print("Goodbye!")
