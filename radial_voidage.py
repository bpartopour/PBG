import bpy  
from mathutils import Vector  
from mathutils.bvhtree import BVHTree  
import numpy as np
import math
import os
import parameters 

###### function q_inside checks if a point is inside the "solid" packing based on ray-casting algorithm ###
###### ray casting algorithm can be mathematically proved by Jordan curve theorm #########
def q_inside(obj, point_in_object_space):  
 
 direction = Vector((1,0,0))  
 epsilon = direction * 1e-6  
 count = 0  
 result, point_in_object_space, normal, index = obj.ray_cast(point_in_object_space, direction)  
 while result:  
  count += 1  
  result, point_in_object_space, normal, index = obj.ray_cast(point_in_object_space + epsilon, direction)  
 return (count % 2) == 1  




def radial_voidage():
    bpy.ops.object.delete()
    bpy.ops.import_mesh.stl(filepath= parameters.file_path, axis_forward='Y', axis_up='Z', filter_glob="*.stl",  global_scale=1.0, use_scene_unit=True, use_facet_normal=False)
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH':
            ob.select = True
            bpy.context.scene.objects.active = ob

    for obj in bpy.data.objects:
        obj.name = 'bed'


    # renaming the stl file
    obj = bpy.data.objects["bed"]
    # changing to edit mode to make all the face normals consistant and facing outwards
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.normals_make_consistent(inside = False)
    bpy.ops.object.editmode_toggle()
    #setting the origin to the geometry and to the space origin
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.context.object.location = 0,0,0
    p_l = obj.matrix_world.translation
    u = bpy.context.object.dimensions

    print("The bed dimensions (X,Y,Z) are:", u[0], u[1], u[2])
    R_tube = (max(u[0],u[1]))/2.0
    d = u[2] - 8*parameters.particle_radius
    if d <= (2*parameters.particle_radius):
        decision = ''
        while decision != 'Yes' and decision != 'No':
            decision = input('WARNING: The bed is not long enough for accurate radial voidage calculation, do you want to continue? Yes, No?')
            if decision != 'Yes' and decision != 'No':
                print("your answer is not acceptable, please enter Yes or No")
        if decision == 'Yes':
            d = u[2]
            r_p = [0]*99
            w_d = [0]*99

            j=1
            dp= 2*parameters.particle_radius
            # setting max and min height of the radial surface
            Lmin = -d/2
            Lmax = d/2
            # generating a cylindrical surface mesh 
            w = 2*math.pi
            r_p = [0]*99
            w_d = [0]*99
            for i in range(0,99):
                #print('loop number is', i)
                R = j*R_tube
                step = 2*math.asin(dp/20/2/R)
                list_t = [t for t in np.arange(0,w,step)] 
                L_face = dp/20
                #print(L_face)
                Area_face = pow(L_face,2)
                list_x_y = [(R*math.cos(x_y),R*math.sin(x_y)) for x_y  in list_t]
                list_z = [z for z in np.arange(Lmin,Lmax,L_face)]
                point_co =[(x,y,z) for (x,y) in list_x_y for z in list_z]
                point_nu = len(point_co)
                count = 0
                #print('number of points',point_nu)
                d = False
                for p in range(0,point_nu):
                    point_in_object_space = Vector((point_co[p]))
                    d = q_inside(obj, point_in_object_space)
                    if d:
                        count += 1

                ring_area = Area_face * point_nu 
                packed_area = Area_face * count
                r_p[i] = 1-(count/point_nu)   
                #print('eps', r_p[i])
                w_d[i] = j
                j = j - 0.01
                if i%10 == 0:
                 print((i),'% progress...')
                
            print('100% progress...Radial voidage calculation is finished!')
            print('writing the data...')
            w_d[0] = 1.0
            Distance = [(R_tube*(1-x))/(2*parameters.particle_radius) for x in w_d]
            file_name = filepath=parameters.file_path_2
            f=open(file_name,'w')
            for k in range(99):
                d = Distance[k]
                z = r_p[k]
                f.write("Distance %.2f Voidage %.2f \n"%(d, z))  
            f.close()
        #    print('Done! :)')
        else:
            print('Radial voidage calculation has stopped, goodbye!')
    elif d > (2*parameters.particle_radius):        
        r_p = [0]*99
        w_d = [0]*99

        j=1
        dp= 2*parameters.particle_radius
        # setting max and min height of the radial surface
        Lmin = -d/2
        Lmax = d/2
        # generating a cylindrical surface mesh 
        w = 2*math.pi
        r_p = [0]*99
        w_d = [0]*99
        for i in range(0,99):
            #print('loop number is', i)
            R = j*R_tube
            step = 2*math.asin(dp/20/2/R)
            list_t = [t for t in np.arange(0,w,step)] 
            L_face = dp/20
            #print(L_face)
            Area_face = pow(L_face,2)
            list_x_y = [(R*math.cos(x_y),R*math.sin(x_y)) for x_y  in list_t]
            list_z = [z for z in np.arange(Lmin,Lmax,L_face)]
            point_co =[(x,y,z) for (x,y) in list_x_y for z in list_z]
            point_nu = len(point_co)
            count = 0
            #print('number of points',point_nu)
            d = False
            for p in range(0,point_nu):
                point_in_object_space = Vector((point_co[p]))
                d = q_inside(obj, point_in_object_space)
                if d:
                    count += 1

            ring_area = Area_face * point_nu 
            packed_area = Area_face * count
            r_p[i] = 1-(count/point_nu)   
            #print('eps', r_p[i])
            w_d[i] = j
            j = j - 0.01
            if i%10 == 0:
             print((i),'% progress...')
            
        print('100% progress...Radial voidage calculation is finished!')
        print('writing the data...')
        w_d[0] = 1.0
        Distance = [(R_tube*(1-x))/(2*parameters.particle_radius) for x in w_d]
        file_name = filepath=parameters.file_path_2
        f=open(file_name,'w')
        for k in range(99):
            d = Distance[k]
            z = r_p[k]
            f.write("Distance %.2f Voidage %.2f \n"%(d, z))  
        f.close()
    #    print('Done! :)')
