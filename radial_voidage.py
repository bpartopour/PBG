import bpy, math, bmesh, mesh_helpers
import numpy as np
import parameters

def radial_voidage():
    bpy.ops.object.delete()
    bpy.ops.import_mesh.stl(filepath= parameters.file_path, axis_forward='Y', axis_up='Z', filter_glob="*.stl",  global_scale=1.0, use_scene_unit=True, use_facet_normal=False)
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH':
            ob.select = True
            bpy.context.scene.objects.active = ob
#   bpy.ops.object.join()
    for obj in bpy.data.objects:
        obj.name = 'bed'



    obj = bpy.data.objects["bed"]
#    bpy.ops.object.editmode_toggle()
#    bpy.ops.mesh.dissolve_limited()
#    bpy.ops.object.editmode_toggle()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.context.object.location = 0,0,0
    p_l = obj.matrix_world.translation
    u = bpy.context.object.dimensions
    print("bed dimensions (X,Y,Z) are:", u[0], u[1], u[2])
    Rad = (max(u[0],u[1]))/2.0
    d = u[2] - 4*parameters.particle_radius
    r_p = [0]*99
    w_d = [0]*99
    tube_volume = 0.0
    j=1

    for i in range(0,99):
        R=j*Rad
        bpy.ops.mesh.primitive_cylinder_add(location = p_l, radius = R, depth = d, vertices = 150)
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].operation = 'INTERSECT'
        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["bed"]
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
        obj = bpy.context.active_object
        bm = mesh_helpers.bmesh_copy_from_object(obj, apply_modifiers = True)
        intersect_volume = bm.calc_volume()


        slice_volume = math.pi*pow(R,2)*d
        if i == 0:
            packing_volume = intersect_volume
        r_p[i] = 1-(packing_volume-intersect_volume)/(tube_volume-slice_volume)
        tube_volume = slice_volume
        packing_volume = intersect_volume
        bpy.ops.object.delete()
        w_d[i] = j+0.005
        j = j-0.01
        
        
    w_d[0] = 1.0
    Distance = [(Rad*(1-x))/(2*parameters.particle_radius) for x in w_d]
    file_name ='/Users/Benancio/Documents/blender/module_packed_bed/radial_p.txt'
    f=open(file_name,'w')
    for k in range(99):
        d = Distance[k]
        z = r_p[k]
        f.write("Distance %.2f Voidage %.2f \n"%(d, z))  
    f.close()
#    print(Distance)
#    print(r_p)
