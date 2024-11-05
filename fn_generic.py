import bpy
import bmesh
from bpy.app.handlers import persistent
from mathutils import Vector
#data = bpy.data
context = bpy.context
#scene = bpy.context.scene
ops = bpy.ops

# =================================================
# ADD
# =================================================
def add_mesh(name):
    """-> types.Mesh: \nmeshes.new(name="m_"+name)"""
    return bpy.data.meshes.new(name="m_"+name)

def add_object(name):
    """-> types.Object: \nobjects.new(name=name, object_data=add_mesh(name))"""
    return bpy.data.objects.new(name=name, object_data=add_mesh(name))

@persistent
def add_collection(name):
    """-> Collection: data.collections.new(name)"""
    if name not in bpy.data.collections:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
        return col
    
    else:
        return bpy.data.collections[name]
    
def add_sub_collection(name, col):
    if name not in bpy.data.collections:
        sub_col = bpy.data.collections.new(name)
        col.children.link(sub_col)
    
def select_collection(name):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    return None

# =================================================
# LINKING
# =================================================
def unlink_from(obj):
    users_collection = obj.users_collection
    for col in users_collection:
        col.objects.unlink(obj)
    pass

def link_to(obj, collection):
    unlink_from(obj)
    collection.objects.link(obj)


# =================================================
# MATERIAL
# =================================================
def add_material(name):
    if name not in bpy.data.materials:
        return bpy.data.materials.new(name)
    else:
        return bpy.data.materials[name]

def set_material(obj, mat):
    select(obj)
    ops.object.material_slot_add()
    obj.material_slots[0].material = mat


# =================================================
# BMESH
# =================================================
def bm_from_mesh(me):
    """-> bmesh: from_mesh(me)"""
    bm = bmesh.new()
    bm.from_mesh(me)
    return bm

def bm_to_mesh(bm, me):
    # finish mesh
    bm.to_mesh(me)
    bm.free()
    me.update()


# =================================================
# CONVERT
# =================================================
def convert_to_curve(obj):
    select(obj)
    me = obj.data
    ops.object.convert(target='CURVE')
    bpy.data.meshes.remove(me)
    name = obj.name
    obj.data.name = "c_"+name
    mode = set_mode(obj, 'EDIT')
    ops.curve.spline_type_set(type='BEZIER')
    ops.curve.handle_type_set(type='ALIGNED')
    back_mode(mode)

def pivot_to_mesh(obj):
    select(obj)
    # convert to mesh
    cu_name = obj.data.name
    me_name = obj.name
    obj.data.resolution_u = 16
    obj.data.bevel_depth  = 0.0
    ops.object.convert(target='MESH')
    bpy.data.curves.remove(bpy.data.curves[cu_name])
    obj.data.name = "m_"+me_name

def convert_to_mesh(obj):
    select(obj)
    # convert to mesh
    cu_name = obj.data.name
    me_name = obj.name
    ops.object.convert(target='MESH')
    bpy.data.curves.remove(bpy.data.curves[cu_name])
    obj.data.name = "m_"+me_name
    ops.object.transform_apply(location=False, rotation=True, scale=False)


# =================================================
# CONVERT COORDINATES
# =================================================
def to_global(obj, co_local):
    return obj.matrix_world @ co_local

def to_local(obj, co_global):
    return obj.matrix_world.inverted() @ co_global

def edge_position(obj, factor):
    max = int(len(obj.data.vertices))-1
    if factor >= 1.0:
        index = max - 1
        x = 1.0
    else:
        value = max * factor
        x = value % 1
        index = int(value)
        
    pos_vec = obj.data.vertices[index].co
    dir_vec = obj.data.vertices[index+1].co - pos_vec

    co = pos_vec + x * dir_vec
    return to_global(obj, co)

def axis_vector(up_axis):
    # move object
    if up_axis == 'x':
        return Vector((1.0, 0.0, 0.0))
    elif up_axis == 'y':
        return Vector((0.0, 1.0, 0.0))
    elif up_axis == 'z':
        return Vector((0.0, 0.0, 1.0))
    elif up_axis == '-x':
        return Vector((-1.0, 0.0, 0.0))
    elif up_axis == '-y':
        return Vector((0.0, -1.0, 0.0))
    elif up_axis == '-z':
        return Vector((0.0, 0.0, -1.0))

# =================================================
# MOVING OBJECTS
# =================================================
def obj_to_edge(obj, edge_obj, factor):
    obj.location = edge_position(edge_obj, factor)

def obj_to_cursor(obj):
    obj.location = bpy.context.scene.cursor.location


# =================================================
# METHODS
# =================================================
def select(obj, one=True):
    if one:
        select_one(obj)
    else:
        obj.select_set(True)

def select_one(obj):
    deselect_all()
    obj.select_set(True)
    set_active(obj)

def select_all():
    ops.object.select_all(action='SELECT')

def deselect_all():
    ops.object.select_all(action='DESELECT')

def set_active(obj):
    bpy.context.view_layer.objects.active = obj

def is_curve(obj):
    return obj.type == 'CURVE'

def is_bezier(obj):
    return obj.data.splines[0].type == 'BEZIER'

def is_poly(obj):
    return obj.data.splines[0].type == 'POLY'

def is_mesh(obj):
    return obj.type == 'MESH'

def get_start_point(obj):
    if is_bezier(obj):
        return obj.data.splines[0].bezier_points[0].co
    elif is_poly(obj):
        return obj.data.splines[0].points[0].co

def origin_to_cursor():
    ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')


# =================================================
# GETTER
# =================================================
def name_obj(obj):
    """-> String: obj.name"""
    return obj.name

def name_data(obj):
    """-> String: obj.data.name"""
    return obj.data.name

def get_collection(name):
    """-> Collection: data.collections[name]"""
    return bpy.data.collections[name]

def cursor_co_copy():
    return bpy.context.scene.cursor.location.copy()

def cursor_to_co(co):
    bpy.context.scene.cursor.location = co

def origin_to_co(co):
    cursor_co = cursor_co_copy()
    bpy.context.scene.cursor.location = co
    origin_to_cursor()
    bpy.context.scene.cursor.location = cursor_co

def get_polygons(obj):
    ops.object.mode_set(mode='OBJECT')
    ops.object.mode_set(mode='EDIT')
    me = obj.data
    return [p for p in me.polygons if p.select and len(p.vertices) == 4]

# =================================================
# SETTER
# =================================================
def set_mode(obj, mode):
    """-> String: obj.mode"""
    old_mode = obj.mode
    ops.object.mode_set(mode=mode)
    return old_mode

def back_mode(mode):
    ops.object.mode_set(mode=mode)
