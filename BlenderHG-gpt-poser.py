### BlenderHG-GPT-Poser_v0.01a, Created by Chenxing Liu (liuchenxing.ai@gmail.com), with the help of OPENAI GPT4
### I am not a Blender developer, just a Blender user that has a little Pythohn knowledge & some freetime.
### This is in a super early prototype stage, it works but it sucks lol.

import bpy
from mathutils import Euler, Quaternion, Vector


# Get the active object in the scene
armature_obj = bpy.context.active_object

# Pose Reset
def reset_A_pose():
    for bone in pose.bones:
        bone.rotation_quaternion = (1, 0, 0, 0)  # Identity quaternion (no rotation)
        bone.rotation_euler = Euler((0, 0, 0), 'XYZ')  # Identity Euler (no rotation)
        bone.location = Vector((0, 0, 0))  # Reset location ('Grab', that is)
    bpy.context.view_layer.update()  # Update the viewport display


if armature_obj and armature_obj.type == 'ARMATURE':
    # Set to POSE mode
    bpy.ops.object.mode_set(mode='POSE')
    armature_data = armature_obj.data
    pose = armature_obj.pose

    # Reset the pose to A-pose
    reset_A_pose()


# This function calculates the orientation matrix of a bone using its world matrix
def get_bone_orientation_matrix(bone):
    bone_matrix = bone.matrix
    world_matrix = armature_obj.matrix_world
    world_to_bone_matrix = world_matrix @ bone_matrix
    orientation_matrix = world_to_bone_matrix.to_3x3()
    return orientation_matrix

# This function does the actual job of moving the bones. Note that it's gettnig matrix values from the function abolve.

def move_bone(bone_name, rotation, grab):
    if rotation is None:
        rotation = (0, 0, 0)

    if grab is None:
        grab = (0, 0, 0)
    
    bpy.context.view_layer.objects.active = armature_obj
    armature_obj.select_set(True)

    bone = pose.bones.get(bone_name)
    bpy.ops.pose.select_all(action='DESELECT')
    bone.bone.select = True

    # Get the current orientation matrix of the bone
    current_orient_matrix = get_bone_orientation_matrix(bone)

    # Assuming rotation is provided in radians
    rotation_x = rotation[0]
    rotation_y = rotation[1]
    rotation_z = rotation[2]

    # Set the rotation mode.
    for axis, value in zip(['X', 'Y', 'Z'], [rotation_x, rotation_y, rotation_z]):
        bpy.ops.transform.rotate(
            value=value,
            orient_axis=axis,
            orient_type='GLOBAL',
            orient_matrix=current_orient_matrix,
            orient_matrix_type='GLOBAL',
            mirror=False,
            snap=False,
            snap_elements={'INCREMENT'},
            use_snap_project=False,
            snap_target='CLOSEST',
            use_snap_self=True,
            use_snap_edit=True,
            use_snap_nonedit=True,
            use_snap_selectable=False
        )

    # Assuming grab is provided in the global coordinate system
    grab_x = grab[0]
    grab_y = grab[1]
    grab_z = grab[2]

    # Set the translation mode.
    bpy.ops.transform.translate(
        value=(grab_x, grab_y, grab_z),
        orient_type='GLOBAL',
        orient_matrix=current_orient_matrix,
        orient_matrix_type='GLOBAL',
        mirror=False,
        snap=False,
        snap_elements={'INCREMENT'},
        use_snap_project=False,
        snap_target='CLOSEST',
        use_snap_self=True,
        use_snap_edit=True,
        use_snap_nonedit=True,
        use_snap_selectable=False
    )

## Paste your GPT generated commands below. They should all look like these:


## Rotate the neck to make the head look slightly to the right
#move_bone("neck", rotation=(0, 0, -0.3), grab=None)

## Move the left shoulder up for the shrug
#move_bone("shoulder.L", rotation=None, grab=(0, 0, 0.1))

## Move the right shoulder up for the shrug
#move_bone("shoulder.R", rotation=None, grab=(0, 0, 0.1))

## Raise and bend the left forearm
#move_bone("upper_arm.L", rotation=(0, 1, 0), grab=None)
#move_bone("forearm.L", rotation=(0, 1.2, 0), grab=None)

## Raise and bend the right forearm
#move_bone("upper_arm.R", rotation=(0, -1, 0), grab=None)
#move_bone("forearm.R", rotation=(0, -1.4, 0), grab=None)

## Grab the eyeball_lookat_master bone to make the eyes look to the right
#move_bone("eyeball_lookat_master", rotation=None, grab=(0.3, 0, 0))
