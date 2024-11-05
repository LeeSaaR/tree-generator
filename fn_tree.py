import bpy
import bmesh

from math import log as ln
from math import sqrt as sq
from math import pow
from math import radians
from math import sin
from math import cos
from random import uniform
from random import randint

data    = bpy.data
context = bpy.context
#scene   = bpy.context.scene
ops     = bpy.ops

# =================================================
# FUNCTIONS
# =================================================
# IMPORTS: DEV
# =================================================
"""
texts = bpy.data.texts
fn_generic   = texts['fn_generic.py'].as_module()

add_collection        = fn_generic.add_collection
add_material          = fn_generic.add_material
add_object            = fn_generic.add_object
add_sub_collection    = fn_generic.add_sub_collection
axis_vector           = fn_generic.axis_vector
back_mode             = fn_generic.back_mode
bm_from_mesh          = fn_generic.bm_from_mesh
bm_to_mesh            = fn_generic.bm_to_mesh
convert_to_curve      = fn_generic.convert_to_curve
convert_to_mesh       = fn_generic.convert_to_mesh
pivot_to_mesh         = fn_generic.pivot_to_mesh
cursor_co_copy        = fn_generic.cursor_co_copy
cursor_to_co          = fn_generic.cursor_to_co
deselect_all          = fn_generic.deselect_all
edge_position         = fn_generic.edge_position
get_polygons          = fn_generic.get_polygons
get_start_point       = fn_generic.get_start_point
link_to               = fn_generic.link_to
name_obj              = fn_generic.name_obj
name_data             = fn_generic.name_data
obj_to_cursor         = fn_generic.obj_to_cursor
obj_to_edge           = fn_generic.obj_to_edge
origin_to_co          = fn_generic.origin_to_co
origin_to_cursor      = fn_generic.origin_to_cursor
select                = fn_generic.select
select_all            = fn_generic.select_all
select_collection     = fn_generic.select_collection
select_one            = fn_generic.select_one
set_active            = fn_generic.set_active
set_material          = fn_generic.set_material
set_mode              = fn_generic.set_mode
to_global             = fn_generic.to_global
to_local              = fn_generic.to_local
"""

# =================================================
# IMPORTS: DEPLOY
# =================================================
#"""
from . fn_generic import bm_from_mesh
from . fn_generic import add_collection
from . fn_generic import add_material
from . fn_generic import add_object
from . fn_generic import add_sub_collection
from . fn_generic import axis_vector
from . fn_generic import back_mode
from . fn_generic import bm_from_mesh
from . fn_generic import bm_to_mesh
from . fn_generic import convert_to_curve
from . fn_generic import convert_to_mesh
from . fn_generic import pivot_to_mesh
from . fn_generic import cursor_co_copy
from . fn_generic import cursor_to_co
from . fn_generic import deselect_all
from . fn_generic import edge_position
from . fn_generic import get_polygons
from . fn_generic import get_start_point
from . fn_generic import link_to
from . fn_generic import name_obj
from . fn_generic import name_data
from . fn_generic import obj_to_cursor
from . fn_generic import obj_to_edge
from . fn_generic import origin_to_co
from . fn_generic import origin_to_cursor
from . fn_generic import select
from . fn_generic import select_all
from . fn_generic import select_collection
from . fn_generic import select_one
from . fn_generic import set_active
from . fn_generic import set_material
from . fn_generic import set_mode
from . fn_generic import to_global
from . fn_generic import to_local
#"""

# =================================================
# VALIDATION
# =================================================
def collections_exists():
    data = bpy.data
    if 'LSR_TREE_STEM' not in data.collections:
        return False
    if 'LSR_TREE_BRANCHES' not in data.collections:
        return False
    if 'LSR_TREE_TWIGS' not in data.collections:
        return False
    if 'LSR_TREE_OUT' not in data.collections:
        return False
    if 'LSR_TREE_META' not in data.collections:
        return False
    if 'LSR_TREE_META_STEM' not in data.collections:
        return False
    if 'LSR_TREE_META_BRANCH' not in data.collections:
        return False
    return True

def stem_exists(context):
    return bpy.context.scene.target_stem is not None


def branches_exists():
    col = select_collection('LSR_TREE_BRANCHES')
    return len(col.objects) > 0

def twigs_exists():
    col = select_collection('LSR_TREE_TWIGS')
    return len(col.objects) > 0

# =================================================
# SETUP
# =================================================
def start_tree(context):
    add_collection('LSR_TREE_STEM')
    add_collection('LSR_TREE_BRANCHES')
    add_collection('LSR_TREE_TWIGS')
    add_collection('LSR_TREE_OUT')
    col = add_collection('LSR_TREE_META')
    add_sub_collection('LSR_TREE_META_STEM', col)
    add_sub_collection('LSR_TREE_META_BRANCH', col)
    pass

# =================================================
# RMEOVE OBJECT
# =================================================
def remove_object(obj, only_object=False):
    data = bpy.data
    if only_object:
        data.objects.remove(obj)
    else:
        obj_data = obj.data
        obj_type = obj.type
        data.objects.remove(obj)
        if obj_type == 'CURVE':
            data.curves.remove(obj_data)
        else:
            data.meshes.remove(obj_data)
        


# =================================================
# STEM
# =================================================
def add_stem(context):
    scene = bpy.context.scene
    lsr_tree = scene.lsr_tree

    if bpy.context.active_object is not None:
        # switch to obejct mode
        set_mode(context.active_object, 'OBJECT')
    
    # create stem object
    col = select_collection('LSR_TREE_STEM')
    stem = add_object('Stem')
    link_to(stem, col)

    # create stem mesh
    add_stem_mesh(stem, lsr_tree)

    # convert stem mesh to curve
    convert_to_curve(stem)

    # set stem curve properties
    curve = stem.data
    curve.resolution_u = 3
    curve.bevel_resolution = 1
    curve.bevel_depth = 1.0
    set_stem_radius(curve, lsr_tree)
    
    # add material
    mat = add_material('Stem')

    # set material
    set_material(stem, mat)

    # set stem target
    bpy.context.scene.target_stem = stem

    # finish
    deselect_all()
    

def add_stem_mesh(stem, lsr_tree):
    height   = lsr_tree.stem_height
    offset   = (height * (lsr_tree.stem_random_pos_factor / 100)) / 20
    segments = lsr_tree.stem_segments
    vert_count  = segments+1
    step_height = height / segments

    bm = bm_from_mesh(stem.data)

    # add vert coordinates
    points = []
    points.append((0.0,0.0,-0.5)) # the root point
    x = 0.0
    y = 0.0
    z = 0.0
    rx = 0.0
    ry = 0.0
    for v in range(vert_count):
        if v != 0:
            rx = uniform(-offset, offset)
            ry = uniform(-offset, offset)
        points.append((x+rx, y+ry, z))
        z += step_height

    # add verts
    verts = [bm.verts.new(vert) for vert in points]

    # add edges
    for i in range(len(verts)):
        if i != 0:
            bm.edges.new((verts[i-1], verts[i]))

    # sort indecies
    bm.verts.sort(key=lambda v: v.co.z)

    bm_to_mesh(bm, stem.data)


def set_stem_radius(curve, lsr_tree):
    height      = lsr_tree.stem_height
    base_radius = lsr_tree.stem_base_radius / 100
    radius      = (height * base_radius) / 10
    radius_comp = (radius * (lsr_tree.stem_radius_min / 100))*0.25
    
    # set radius
    spline = curve.splines[0]
    points = spline.bezier_points
    for point in points:
        r = stem_radius(point.co.z, radius, height)
        point.radius = r

    # thicken root
    points[0].radius = points[1].radius * 1.25

    # compensate radius
    for point in reversed(points):
        compensation = radius_comp_fn(point.co.z, radius_comp)
        point.radius += compensation
    

def stem_radius(z, radius, height):
    w = radius
    h = height
    ln1 = ln(h+1)
    ln2 = ln(z+1)
    r = (-w/ln1)*(ln2)+w
    return r


def radius_comp_fn(x, radius_comp):
    return radius_comp * x


# =================================================
# STEM PIVOT
# =================================================

def add_stem_pivot(src_obj):
    # copy stem
    obj      = src_obj.copy()
    obj.data = src_obj.data.copy()
    obj.name      = 'StemPivot'
    obj.data.name = 'c_StemPivot'
    col = select_collection('LSR_TREE_META_STEM')
    link_to(obj, col)

    pivot_to_mesh(obj)
    obj = bpy.data.objects['StemPivot']
    set_stem_pivot(obj)
    obj.hide_set(True)


def set_stem_pivot(obj):
    bm = bm_from_mesh(obj.data)
    
    # subdivide
    bm.edges.ensure_lookup_table()
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=4)
    
    # sort
    bm.verts.ensure_lookup_table()
    bm.verts.sort(key=lambda v: v.co.z)
    
    bm_to_mesh(bm, obj.data)
    

# =================================================
# BRANCHES
# =================================================
def add_branches(context):
    scene = bpy.context.scene
    stem = scene.target_stem
    lsr_tree = scene.lsr_tree

    if bpy.context.active_object is not None:
        set_mode(context.active_object, 'OBJECT')
    
    # stem props
    stem_height = lsr_tree.stem_height
    col = select_collection('LSR_TREE_BRANCHES')

    # branch props
    count = lsr_tree.branches_count
    height_start = stem_height*(lsr_tree.branches_start_height/100)
    overtop = lsr_tree.branches_crown_overtop

    tilt_start = lsr_tree.branches_start_tilt
    tilt_max   = lsr_tree.branches_max_tilt
    tilt_difference = tilt_max - tilt_start
    tilt_distance = tilt_difference / count
    tilt = tilt_start

    height_difference = (stem_height*0.9) - height_start
    branch_distance = height_difference / count
    height = height_start

    # get crown intersection with x axis
    crown_width = lsr_tree.branches_crown_width
    xn = crown_x_zero(crown_width, stem_height+overtop) * 0.5

    # add branches
    for b in range(count):
        # get x max
        xmax = newton(xn, crown_width, tilt, stem_height+overtop, height)
        add_branch(context, xmax, tilt, height)
        height += branch_distance
        tilt += tilt_distance
        xn = xmax * 0.5

    # add stem pivot for branches
    stem_pivot_exists = 'StemPivot' in select_collection('LSR_TREE_META_STEM').objects
    if not stem_pivot_exists:
        add_stem_pivot(stem)

    snap_branches_to_stem()

    rotate_branches(context)

    # add material
    mat = add_material('Branch')
    
    # set materials
    for branch in col.objects:
        set_material(branch, mat)

    # parent branches to stem
    select (bpy.context.scene.target_stem)
    for branch in col.objects: select(branch, False)
    ops.object.parent_set(type='OBJECT', keep_transform=True)

    select (bpy.context.scene.target_stem)
    deselect_all()


def add_branch(context, xmax, tilt, height):
    scene = bpy.context.scene
    lsr_tree = scene.lsr_tree

    # create stem object
    col = select_collection('LSR_TREE_BRANCHES')
    branch = add_object('Branch')
    link_to(branch, col)

    # create stem mesh
    add_branch_mesh(branch, lsr_tree, xmax, tilt, height)

    # create stem curve
    convert_to_curve(branch)
    curve = branch.data

    # set stem curve properties
    curve.resolution_u = 3
    curve.bevel_resolution = 1
    curve.bevel_depth = 0.66
    set_branch_radius(curve, lsr_tree, height, xmax)


def add_branch_mesh(obj, lsr_tree, xmax, tilt, height):
    offset = (xmax * (lsr_tree.branches_random_pos / 100)) / 20
    segments = lsr_tree.branches_segments
    vert_count  = segments+1
    step_width = xmax / segments

    bm = bm_from_mesh(obj.data)

    x = 0.0
    y = 0.0
    ry = 0.0
    rz = 0.0
    
    points = []
    for v in range(vert_count):
        if v != 0:
            ry = uniform(-offset, offset)
            rz = uniform(-offset, offset)
        z = branch_fn(x, tilt, height)
        points.append((x, y+ry, z+rz))
        x += step_width

    verts = []
    for vert in points:
        verts.append( bm.verts.new(vert) )

    for i in range(len(verts)):
        if i != 0:
            bm.edges.new((verts[i-1], verts[i]))

    bm.verts.sort(key=lambda v: v.co.x)

    bm_to_mesh(bm, obj.data)


def snap_branches_to_stem():
    pivot = bpy.data.objects['StemPivot']

    # get branches
    col = select_collection('LSR_TREE_BRANCHES')
    branches = col.objects

    # origin to branch start
    for branch in branches:
        spline = branch.data.splines[0]
        point = spline.bezier_points[0]
        co = point.co
        cursor_to_co(co)
        select(branch)
        origin_to_co(co)

    # snap branches to stem
    me = pivot.data
    for branch in branches:
        h = branch.location.z
        tolerance = 0.01

        for v in me.vertices:
            z = v.co.z
            max = h+tolerance
            min = h-tolerance
            if z >= min and z <= max:
                branch.location = v.co
                break
    
    bpy.context.scene.cursor.location = (0.0,0.0,0.0)


def rotate_branches(context):
    branches = select_collection('LSR_TREE_BRANCHES').objects
    angle_offset = bpy.context.scene.lsr_tree.branches_rotation
    angle = 0.0
    i = 0
    for b in branches:
        select(b)
        if i % 2 == 0:
            b.rotation_euler[2] = radians(180.0+angle)
        else:
            b.rotation_euler[2] = radians(0.0+angle)
            angle += angle_offset
        i += 1
    
    for b in branches:
        select(b)
        random_rotation = radians(uniform(uniform(-15.0, 0.0), uniform(0.0, 15.0)))
        b.rotation_euler[2] += random_rotation


def branch_radius(z, radius, height, radius_comp):
    c = radius_comp * 0.5
    w = radius
    h = height
    ln1 = ln(h+1)
    ln2 = ln(z+1)
    r = (-w/ln1)*(ln2)+w
    return r + c


def set_branch_radius(curve, lsr_tree, height, xmax):

    stem_height      = lsr_tree.stem_height
    base_radius = lsr_tree.stem_base_radius / 100
    radius_stem      = (stem_height * base_radius) / 10
    radius_comp = (radius_stem * (lsr_tree.stem_radius_min / 100))*0.25

    radius = stem_radius(height, radius_stem, stem_height)
    
    spline = curve.splines[0]
    points = spline.bezier_points
    for point in points:
        #r = branch_radius(point.co.x, radius*(1.05), xmax, radius_comp)
        r = branch_radius(point.co.x, radius, xmax, radius_comp)
        point.radius = r


def crown(x, c, hs):
    y = -c * pow(x, 2) + hs
    return y

def crown_x_zero(c, hs):
    x = sq(-hs/-c)
    return x

def branch_fn(x, b, hb):
    y = b * ln(x+1) + hb
    return y


def f1(x, c, b, hs, hb):
    # equated crown() and branch()
    # -cx² +hs = b*ln(x+1) + hb            | -hs
    #     -cx² = b*ln(x+1) + (hb-hs)       | +ax²
    #        0 = cx² + b*ln(x+1) + (hb-hs)

    #     f(x) = cx² + b*ln(x+1) + (hb-hs)
    #    f'(x) = 2cx + b*(1/(x+1))

    #     n(x) = x-((f(x))/(f'(x)))
    return c*pow(x,2) + b*ln(x+1) + (hb-hs)

def f2(x, c, b):
    # derivative of f1()
    return (2*c*x) + (b*((1)/(x+1)))

def newton(xn, c, b, hs, hb):
    for i in range(20):
        equated    = f1(xn, c, b, hs, hb)
        derivative = f2(xn, c, b)
        xn = xn-(equated/derivative)
    return xn

# =================================================
# CONVERT TO MESH
# =================================================
def stem_and_branch_to_mesh(context):
    stem = bpy.data.objects['Stem']
    col = select_collection('LSR_TREE_BRANCHES')
    
    # make sure that resolution is 3 and 1
    objects = [obj for obj in col.objects]
    for branch in objects:
        curve = branch.data
        curve.resolution_u = 3
        curve.bevel_resolution = 1

    objects.append(stem)

    # convert and unwrap
    for obj in objects:
        if obj.type == 'CURVE':
            convert_to_mesh(obj)
            mark_seam(obj, 6)
            select(obj)
            unwrap(obj)

    # fill holes (tips and roots)
    for obj in objects:
        select(obj)
        set_mode(obj, 'EDIT')
        for v in obj.data.vertices:
            v.select = True
        set_mode(obj, 'OBJECT')
        set_mode(obj, 'EDIT')
        ops.mesh.fill_holes(sides=7)
        set_mode(obj, 'OBJECT')

    select(stem)
    deselect_all()

# =================================================
# UNWRAP
# =================================================
def mark_seam(obj, verts_per_segment):
    set_mode(obj, 'EDIT')
    ops.mesh.select_mode(type="VERT")
    ops.mesh.select_all(action = 'DESELECT')
    set_mode(obj, 'OBJECT')

    # get seam vertices
    verts = obj.data.vertices
    index = 0
    indecies = []
    for i in range(int(len(verts)/verts_per_segment)):
        indecies.append(index)
        index += verts_per_segment

    # select all verts
    for i in indecies:
        verts[i].select = True
        
    set_mode(obj, 'EDIT')
    ops.mesh.mark_seam(clear=False)
    set_mode(obj, 'OBJECT')


def unwrap(obj):
    set_mode(obj, 'EDIT')
    ops.mesh.select_mode(type='FACE')
    ops.mesh.select_all(action='DESELECT')

    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()

    ops.mesh.select_all(action='SELECT')
    bm.faces.active = bm.faces[0]
   
    ops.uv.follow_active_quads(mode='EVEN')
    # needs to be reset and unwarped again (maybe a bug?) 
    ops.uv.reset()
    ops.uv.follow_active_quads(mode='EVEN')

    # position cursor in uv editor
    bpy.data.screens[10].areas[2].spaces[0].cursor_location = (0.5, 0.5)
    ops.uv.select_all(action='SELECT')
    
    set_mode(obj, 'OBJECT')
    bm.free()

    # get the uv map
    me = obj.data
    uvm = me.uv_layers.active

    # get the offset
    segment_count = int(len(me.polygons)/6)
    offset = (0.5 * (segment_count * (1/6))) - 0.5 

    scale_factor = 1/6
    pivot = 0.5
    for uv_index in range( len(uvm.data) ):
        # scale the uvs
        x = uvm.data[uv_index].uv.x
        y = uvm.data[uv_index].uv.y
        xn = pivot + scale_factor*(x - pivot)
        yn = pivot + scale_factor*(y - pivot)
        uvm.data[uv_index].uv = ( xn - pivot + scale_factor*0.5, yn - pivot + scale_factor*0.5)
        uvm.data[uv_index].uv.x -= offset

        # rotate the uvs
        x = uvm.data[uv_index].uv.x + 0
        y = uvm.data[uv_index].uv.y - 1
        xn = x * cos(radians(90)) - y * sin(radians(90))
        yn = x * sin(radians(90)) + y * cos(radians(90))
        uvm.data[uv_index].uv.x = xn
        uvm.data[uv_index].uv.y = yn


# =================================================
# TWIGS
# =================================================
def add_twigs(context, branch):
    scene = bpy.context.scene
    stem = scene.target_stem
    branch_segments = scene.lsr_tree.branches_segments
    select(branch)

    # get branch
    all_polys = branch.data.polygons

    # don't use first and last polygon (root and tip poly)
    all_polys = all_polys[1:len(all_polys)-2]

    # deselect all polygons
    for poly in all_polys:
        poly.select = False

    # calculate properties
    poly_max = len(all_polys) - 1
    polys_per_segment = 6
    segments = branch_segments * 3
    middle = (polys_per_segment * segments) * 0.5

    # calulate start factor
    start_factor = int((segments*0.45) * bpy.context.scene.lsr_tree.twigs_start_factor) 
    end_factor = int((segments*0.5) * bpy.context.scene.lsr_tree.twigs_end_factor) 

    # map to index
    i_start = int(start_factor * polys_per_segment)
    i_end   = int(end_factor * polys_per_segment + middle) - 1

    filtered_polys = all_polys[i_start:i_end]

    # use bool list to randomly select polygons 
    bools = [True, False, False, True, False, False, False, True]
    index_last = len(bools)-1

    # select final polygons
    polys = []
    for poly in filtered_polys:
        random_select = bools[randint(0, index_last)]
        if random_select:
            polys.append(poly)
    
    # no polys selected?
    if len(polys) == 0:
        return 
    
    # make instances
    twigs = []
    add_twig_instances(context, polys, branch, twigs)

    # select stem
    deselect_all()
    select(stem)
    
    # min max angle factors
    start_angle = bpy.context.scene.lsr_tree.twigs_start_angle
    end_angle   = bpy.context.scene.lsr_tree.twigs_end_angle
    f_min = start_angle
    f_max = (( 0.5 * end_angle ) + 0.5) * 0.1
    f_ran = (f_min-f_max)
    poly_max = len(branch.data.polygons) - 1

    # move twig instances to random poly normals
    for i in range(len(polys)):
        poly = polys[i]
        p_fac = (poly.index + 1) / poly_max
        factor = f_min - p_fac * f_ran
        move_twig_to_normal(twigs[i], branch, poly, factor, axis_vector('z'))

    # rotate twigs just a bit
    for twig in twigs:
        twig.rotation_euler[0] += radians(uniform(-10.0, 10.0))
        twig.rotation_euler[1] += radians(uniform(-10.0, 10.0))
    
    # rotate twigs on z-axis
    bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
    for twig in twigs:
        select(twig)
        random_rotation = radians(uniform(-360, 360.0))
        ops.transform.rotate(value=random_rotation, orient_axis='Z', orient_type='NORMAL', constraint_axis=(False, False, True))

    # set display type
    for twig in twigs:
        select(twig)
        bpy.context.object.display_type = 'TEXTURED'

    deselect_all()


def add_twig_instances(context, polygons, parent, instances):
    twigs_ref =  bpy.context.scene.target_twigs.objects
    twigs_count = len(twigs_ref) - 1
    deselect_all()
    select(parent)

    col = select_collection('LSR_TREE_TWIGS')
    for i in range(len(polygons)):
        # get random twig from twig input collection
        random_index = randint(0, twigs_count) 
        random_twig_name = twigs_ref[random_index].name
        data_of_random_twig = twigs_ref[random_index].data
        # add new twig instance
        obj = bpy.data.objects.new(random_twig_name, data_of_random_twig)
        instances.append(obj)
        col.objects.link(obj)
        select(obj, False)
    
    # parent twigs to corresponding branch
    ops.object.parent_set(type='OBJECT', keep_transform=True)


def move_twig_to_normal(obj, target, poly, factor, up_axis):
    co = target.matrix_world @ poly.center
    v1 = up_axis
    v2 = get_rot_vector(target, poly, factor)
    rotation = v1.rotation_difference( v2 ).to_euler()
    obj.rotation_euler = rotation
    obj.location = co

def get_rot_vector(obj, poly, factor):

    vert = obj.data.vertices[len(obj.data.vertices)-1]

    # positional vector: branch tip
    pos_tip = obj.matrix_world @ vert.co

    # positional vector: twig origin
    pos_origin = obj.matrix_world @ poly.center 

    # directional vector: normal
    dir_n = poly.normal

    # positional vector: normal tip
    dir_nt = pos_origin + 1.0 * dir_n

    # directional vector: normal tip <-> branch tip
    dir_nb = dir_nt - pos_tip

    # positional vector: rotation tip
    rot_tip = pos_tip + factor * dir_nb

    # directional vector: rotation
    dir_rot = rot_tip - pos_origin
    return dir_rot


# =================================================
# DISPLAY TYPE
# =================================================
def set_display_type(display_type='TEXTURED'):
    twigs = select_collection('LSR_TREE_TWIGS').objects
    for twig in twigs:
        select(twig)
        bpy.context.object.display_type = display_type
    
    select (bpy.context.scene.target_stem)
    deselect_all()

# =================================================
# SHADING
# =================================================
def shade_smooth():
    obj = bpy.context.scene.target_stem
    col = bpy.data.collections['LSR_TREE_BRANCHES']

    objects = [o for o in col.objects]
    objects.append(obj)
    for o in objects:
        select(o)
        ops.object.shade_smooth()
    deselect_all()

def shade_flat():
    obj = bpy.context.scene.target_stem
    col = bpy.data.collections['LSR_TREE_BRANCHES']

    objects = [o for o in col.objects]
    objects.append(obj)
    for o in objects:
        select(o)
        ops.object.shade_flat()
    deselect_all()

# =================================================
# TREE
# =================================================
def make_tree():
    twigs    = select_collection('LSR_TREE_TWIGS').objects
    branches = select_collection('LSR_TREE_BRANCHES').objects
    stem     = bpy.context.scene.target_stem

    # create object list
    objects = [stem]
    for b in branches: objects.append(b)
    for t in twigs: objects.append(t)

    # remember branch meshes for deletion
    branch_meshes = []
    for b in branches: branch_meshes.append(b.data)

    # select all make stem active
    deselect_all()
    for obj in objects: select(obj, False)
    bpy.context.view_layer.objects.active = stem

    # join all
    ops.object.join()
    bpy.context.scene.target_stem = None

    # move joind object (tree) and rename
    in_col = bpy.data.collections['LSR_TREE_STEM']
    out_col = add_collection('LSR_TREE_OUT')
    in_col.objects.unlink(stem)
    out_col.objects.link(stem)
    stem.name = 'Tree'
    stem.data.name = 'm_Tree'

    ## clean up
    # remove branch meshes
    for branch_mesh in branch_meshes: bpy.data.meshes.remove(branch_mesh)

    # remove stem pivot
    stem_pivot = bpy.data.objects['StemPivot']
    remove_object(stem_pivot)

"""
# ======================================
# TRANSFORM ORIENTATION
# ======================================
ops = bpy.ops
scene = context.scene
orientation = scene.transform_orientation_slots[0]

ops.transform.create_orientation(name='Branch', overwrite=True)
orientation.type = 'Branch'
#bpy.ops.transform.delete_orientation() # how to delete orientation
"""