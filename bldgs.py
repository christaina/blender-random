import bpy, bmesh
import numpy as np

def get_cubes():
    cubes = []
    for obj in bpy.data.objects:
        if 'cube' in obj.name:
            cubes.append(obj)
    return cubes

def delete_cubes():
    bpy.ops.object.select_all(action='DESELECT')
    cubes = get_cubes()
    for obj in cubes:
            obj.select = True
    bpy.ops.object.delete()
    
def make_material(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    return mat
 
def set_material(ob, mat):
    me = ob.data
    me.materials.append(mat)
 
def color():
    # Create two materials
    pink = make_material('Pink', (0.8,0.1,0.7), (1,1,1), 1)
    for obj in get_cubes():
        set_material(obj, pink)

#Define vertices, faces, edges
verts = [(0,0,0),(0,5,0),(5,5,0),(5,0,0),(0,0,5),(0,5,5),(5,5,5),(5,0,5)]
faces = [(0,1,2,3), (4,5,6,7), (0,4,5,1), (1,5,6,2), (2,6,7,4), (3,7,4,0)]

nrow=15
ncol=5
space=6
delete_cubes()    
for k in range(nrow):  
    for j in range(ncol):
        n = 'cube_'+str(j)+str(k)

        #Define mesh and objectxx
        mesh = bpy.data.meshes.new(n)
        object = bpy.data.objects.new(n, mesh) 

        #Set location and scene of objects
        object.location = (j*space, k*space, 0)
        bpy.context.scene.objects.link(object)

        #Create mesh
        mesh.from_pydata(verts,[],faces)
        mesh.update(calc_edges=True)

        bpy.data.objects[n].select = True   
        bpy.context.scene.objects.active = bpy.context.scene.objects[n] # Select the default Blender Cube

        #Enter edit mode to extrude
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(number_cuts=3)
        bpy.ops.mesh.normals_make_consistent(inside=False)

        bm = bmesh.from_edit_mesh(mesh)
        for face in bm.faces:
            face.select = False
        
        r_v = np.random.randint(0, len(bm.verts),10)
        for i, vert in enumerate(bm.verts):
            if i in r_v:
                vert.select = True
            
        # Show the updates in the viewport
        bmesh.update_edit_mesh(mesh, True)

        bpy.ops.transform.translate(value=(0, 0, np.random.rand()*3))
        bpy.ops.object.mode_set(mode='OBJECT')
color()  

bpy.ops.mesh.primitive_plane_add(location=(0,0,0), radius=100)
