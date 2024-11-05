from bpy.types import PropertyGroup

from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
    StringProperty,
)

class LSR_PG_tree(PropertyGroup):
    stem_base_radius : IntProperty(
        name="base radius %",
        min=1,
        max=100,
        default=100
    )
    stem_radius_min : IntProperty(
        name="radius min",
        min=1,
        max=100,
        default=20
    )
    stem_height : FloatProperty(
        name="height",
        min=0.5,
        max=50.0,
        default=5.0  
    )
    stem_segments : IntProperty(
        name="segments",
        min=3,
        max=50,
        default=5  
    )
    stem_random_pos_factor : IntProperty(
        name="random",
        min=1,
        max=100,
        default=25
    )

    branches_count : IntProperty(
        name="count",
        min=1,
        max=50,
        default=12
    )
    branches_start_height : FloatProperty(
        name="start height %",
        min=1.0,
        max=95.0,
        default=10.0
    )
    branches_start_tilt : FloatProperty(
        name="tilt factor",
        min=0.01,
        max=2.5,
        default=1.5 
    )
    branches_max_tilt : FloatProperty(
        name="tilt max",
        min=2.0,
        max=8.0,
        default=2.0
    )
    branches_rotation : FloatProperty(
        name="rotation",
        min=0.0,
        max=180.0,
        default=45.0
    )
    branches_crown_width : FloatProperty(
        name="crown width",
        min=0.15,
        max=20.0,
        default=1.0
    )
    branches_crown_overtop : FloatProperty(
        name="crown overtop",
        min=0.0,
        max=5.0,
        default=0.5
    )
    branches_segments : IntProperty(
        name="segments",
        min=3,
        max=12,
        default=4
    )
    branches_random_pos : IntProperty(
        name="random",
        min=1,
        max=100,
        default=100
    )

    twigs_start_angle : FloatProperty(
        name="start angle",
        min=0.0,
        max=1.0,
        default=1.0
    )

    twigs_end_angle : FloatProperty(
        name="end angle",
        min=0.0,
        max=1.0,
        default=0.0
    )
    twigs_start_factor : FloatProperty(
        name="start",
        min=0.0,
        max=1.0,
        default=0.25 
    )

    twigs_end_factor : FloatProperty(
        name="end",
        min=0.0,
        max=1.0,
        default=0.75
    )
    twigs_wire : BoolProperty(
        name="wire",
        default=True 
    )
