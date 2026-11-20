import bpy
import os

# Parameters
export_path = "C:/Users/<user>/AppData/LocalLow/Pine Studio/Escape Simulator 2/UGC/Room_x/_CustomModels" # CHANGE THIS


def is_renderable(obj):
    """True if the object's render toggle (camera icon) is on, and
    none of the collections that directly hold it have rendering turned off."""
    if obj.hide_render:
        return False
    return not any(col.hide_render for col in obj.users_collection)


def unhide(obj):
    """Make an object visible and selectable. Returns its previous state."""
    state = {
        'hide': obj.hide_get(),               # eye icon
        'hide_viewport': obj.hide_viewport,   # monitor icon
        'hide_select': obj.hide_select,       # arrow icon
    }
    obj.hide_viewport = False
    obj.hide_set(False)
    obj.hide_select = False
    return state


def restore_visibility(obj, state):
    obj.hide_viewport = state['hide_viewport']
    obj.hide_set(state['hide'])
    obj.hide_select = state['hide_select']


def deselect_all():
    for o in bpy.context.view_layer.objects:
        o.select_set(False)


def export_gltf(obj, export_path, object_name=None):
    object_name = object_name or obj.name
    object_export_path = os.path.join(export_path, object_name)
    os.makedirs(object_export_path, exist_ok=True)

    # Temporarily unhide so the object can be selected and exported
    visibility_state = unhide(obj)
    original_location = obj.location.copy()

    try:
        deselect_all()
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        obj.location = (0, 0, 0) # Force object origin to (0, 0, 0)

        bpy.ops.export_scene.gltf(
            filepath=os.path.join(object_export_path, f"{object_name}.gltf"),
            export_format='GLTF_SEPARATE', # Keep separate textures
            use_selection=True, # Export selected only
            export_apply=True, # Apply modifiers
        )
    finally:
        # Revert object to original state
        obj.location = original_location
        obj.select_set(False)
        restore_visibility(obj, visibility_state)


def export_curve_as_mesh(obj, export_path):
    # Duplicate so the original curve remains untouched
    duplicate = obj.copy()
    duplicate.data = obj.data.copy()
    bpy.context.scene.collection.objects.link(duplicate)

    try:
        unhide(duplicate)

        # Convert duplicate to mesh
        deselect_all()
        bpy.context.view_layer.objects.active = duplicate
        duplicate.select_set(True)
        bpy.ops.object.convert(target='MESH')

        # Export under the original curve's name, not "Curve.001"
        export_gltf(duplicate, export_path, object_name=obj.name)
    finally:
        # Remove temporary object and its mesh data
        mesh = duplicate.data
        bpy.data.objects.remove(duplicate, do_unlink=True)
        if mesh and mesh.users == 0:
            bpy.data.meshes.remove(mesh)


def export_renderable_to_gltf(export_path):
    os.makedirs(export_path, exist_ok=True)

    view_layer_objects = bpy.context.view_layer.objects
    # Snapshot the list, since curve export adds/removes temporary objects
    candidates = [
        obj for obj in bpy.context.scene.objects
        if obj.type in {'MESH', 'CURVE'} and is_renderable(obj)
    ]

    for obj in candidates:
        if obj.name not in view_layer_objects:
            # Object's collection is excluded from the view layer (unchecked box)
            print(f"Skipping (collection excluded from view layer): {obj.name}")
            continue

        print(f"Exporting: {obj.name}")
        if obj.type == 'CURVE':
            export_curve_as_mesh(obj, export_path)
        else:
            export_gltf(obj, export_path)


export_renderable_to_gltf(export_path)
print("Done")
