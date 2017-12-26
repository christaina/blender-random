"""
From https://blenderartists.org/forum/showthread.php?433738-How-in-python-select-top-faces
"""

import bpy, math, bmesh
from mathutils import Vector

def bmesh_copy_from_object(obj, transform=True, triangulate=True, apply_modifiers=False):
    assert(obj.type == 'MESH')


    if apply_modifiers and obj.modifiers:
        import bpy
        me = obj.to_mesh(bpy.context.scene, True, 'PREVIEW', calc_tessface=False)
        bm = bmesh.new(); bm.from_mesh(me); bpy.data.meshes.remove(me)
        del bpy
    else:
        me = obj.data
        if obj.mode == 'EDIT': bm_orig = bmesh.from_edit_mesh(me); bm = bm_orig.copy()
        else: bm = bmesh.new(); bm.from_mesh(me)


    if transform: bm.transform(obj.matrix_world)
    if triangulate: bmesh.ops.triangulate(bm, faces=bm.faces)
    return bm


def sel_top(obj):
    bm = bmesh_copy_from_object(obj, transform=True, triangulate=False); bm.normal_update()


    fo = [ele.index for ele in bm.faces if 
    Vector((0, 0, -1.0)).angle(ele.normal, 4.0) > (math.pi)]

    bpy.ops.mesh.select_all(action='DESELECT')
    for i in fo:
        obj = bpy.context.edit_object
        bm = bmesh.from_edit_mesh(obj.data).faces[i].select = True
        bmesh.update_edit_mesh(obj.data, True)
