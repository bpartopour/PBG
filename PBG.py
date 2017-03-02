##Packed-Bed generation module (Version-Beta)
##BPartopour, AG Dixon†
##Heat and Mass Transfer Lab
##Worcester Polytechnic Institute

#Main Program
import bpy 
import parameters
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
print("Initializing the parameter ...")
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
last_particle_drop_frame = int((number_of_particle / 5) * 10)

#generating the particles and filling up the tube
print("Filling up the bed....")
simulation_current_frame = rigidbody_simulation(Particle_type, last_particle_drop_frame)

bpy.ops.object.select_by_type( type = 'MESH')
#continueing the simulation till steady-state (condition: max particle velocity < 0.01)
print("Reaching the steady_state condition")
distance=steady_state(simulation_current_frame)
bpy.ops.object.select_all(action = 'TOGGLE')#removing the container
if parameters.remove_the_tube == True:
    bpy.data.objects['Cylinder'].select = True
    bpy.ops.object.delete(use_global = False)

#Do we want to get the angle distribution? if so, in parameters.py set the angle_dist to True

if parameters.angle_dist == True:
    print("Calculating the particles angle distributiions in the bed...")
    bpy.ops.object.select_by_type( type = 'MESH')
    file_name = parameters.file_name
    angle_distribution(file_name)
    
    
    
#to export the bed uncomment the next 2 lines: 
#bpy.ops.object.select_all(action = 'TOGGLE')
print("Exporting the geometry as a STL file...")
bpy.ops.export_mesh.stl(filepath=parameters.file_path, check_existing=True, axis_forward='Y', axis_up='Z', filter_glob= ".STL", use_selection=False, global_scale=1, use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OFF')

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
