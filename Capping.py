import bpy
import math 
import parameters
print("Welcome to Local Flattening Module")
dp = 2 * parameters.particle_radius
tol_p=0.02
tol_w = 0.04
d_bridge = dp/5
l_bridge = 0.2
R_tube = parameters.cyl_radius - 0.02
bpy.ops.object.select_by_type( type = 'MESH')
bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY')
obj = bpy.context.selected_objects
size = len(bpy.context.selected_objects)
x = list()
y = list()
z = list()
progress = list()
x_bridge = list()
y_bridge= list()
z_bridge= list()
orientation_bridge_x= list()
orientation_bridge_y= list()
orientation_bridge_z= list()
for ob in obj:

    x.append(ob.matrix_world.translation[0])
    y.append(ob.matrix_world.translation[1])
    z.append(ob.matrix_world.translation[2])

n_spheres = len(y)
p_p = 0
p_w = 0
for i in range(n_spheres):
    #Particle-Particle Contact Points
    for j in range(i+1,n_spheres):
        
        x_dis = (x[i]-x[j])
        y_dis = (y[i]-y[j])
        z_dis = (z[i]-z[j])
        
        distance = math.sqrt((x_dis**2)+(y_dis**2)+(z_dis**2))
        phi = math.atan2(y_dis, x_dis)
        theta = math.acos((z_dis)/distance)
        
        if distance < dp+tol_p:
            p_p = p_p + 1
            x_bridge.append((x[i]+x[j])/2)
            y_bridge.append((y[i]+y[j])/2)
            z_bridge.append((z[i]+z[j])/2)
            orientation_bridge_x.append(theta)
            orientation_bridge_y.append(phi)
    #Particle-Wall Contact Points        
    x_dis = x[i]
    y_dis = y[i]
    z_dis = z[i]
    
    distance = ((R_tube) - math.sqrt((x_dis**2)+(y_dis**2)))
    phi = math.atan2(y_dis, x_dis)
    theta = math.acos(0)
    if distance < (dp/2)+tol_w:
        p_w = p_w +1
        b = y_dis/x_dis
        c = 1/(math.sqrt(1 + b**2))
        if x_dis < 0.0:
            x_bridge.append(-R_tube*c)
            y_bridge.append(b * -R_tube * c)
        else:
            x_bridge.append(R_tube*c)
            y_bridge.append(b * R_tube * c)
        z_bridge.append(z[i])
        orientation_bridge_x.append(theta)
        orientation_bridge_y.append(phi)


caps_number = len(x_bridge)
print('Number of Contact Points is',caps_number)
print('Number of Particle-Wall Contact Points is', p_w)
print('Number of Particle-Particle Contact Points is', p_p)
bpy.ops.object.join()
bpy.context.object.name = 'Sphere.028'
for k in range(caps_number):
    bpy.ops.mesh.primitive_cylinder_add(vertices = 50,
                                                end_fill_type = 'TRIFAN',
                                                radius = parameters.particle_radius/4.5,
                                                depth = parameters.particle_radius/25,
                                                location = (x_bridge[k], y_bridge[k],z_bridge[k]),
                                                rotation = (0,orientation_bridge_x[k], orientation_bridge_y[k]))
    bpy.context.object.name = 'cap'
    bpy.context.scene.objects.active = bpy.data.objects["Sphere.028"]
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["cap"]
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
    bpy.context.scene.objects.active = bpy.data.objects["cap"]
    bpy.ops.object.delete()
    progress.append(int((k*100)/caps_number))
    if progress[k]%10 == 0.0 and k !=0:
        if progress[k] != progress[k-1]:
            print(progress[k],'% of the caps are made...')
print("100% of the caps are made...xporting the capped geometry as a STL file...")

bpy.ops.export_mesh.stl(filepath=parameters.file_path_capped, check_existing=True, axis_forward='Y', axis_up='Z', filter_glob= ".STL", global_scale=1, ascii=False, use_mesh_modifiers=True)

print('Capping procedure is finnished, and the STL file is saved in the selected directory! Have a nice day! :)')
