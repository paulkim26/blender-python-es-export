import bpy
import os

# Parameters
collection_name = "export"
export_path = "C:/Users/<user>/AppData/LocalLow/Pine Studio/Escape Simulator 2/UGC/Room_x/_CustomModels" # CHANGE THIS!

def export_gltf(obj, export_path):
    if obj.hide_get(): # Skip hidden objects
        return
    
    # Clear out pre-existing selections
    for all_objects in bpy.context.scene.objects:
        all_objects.select_set(False)
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    object_name = obj.name
    object_export_path = os.path.join(export_path, object_name)
    
    if not os.path.exists(object_export_path):
        os.makedirs(object_export_path)
        
    # Temporarily modify object for export
    obj_original_state = {
        'location': obj.location.copy(),
    }
    obj.location = (0, 0, 0) # Force object origin to (0, 0, 0)
    
    # Export
    bpy.ops.export_scene.gltf(
        filepath=os.path.join(object_export_path, f"{object_name}.gltf"),
        export_format='GLTF_SEPARATE', # Keep separate textures
        use_selection=True, # Export selected only
        export_apply=True, # Apply modifiers
    )
    
    # Revert object to original state
    obj.location = obj_original_state['location']
    
    obj.select_set(False)

def export_collection_to_gltf(collection_name, export_path):
    # Get the collection by name
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"Collection '{collection_name}' not found.")
        return
    
    if not os.path.exists(export_path):
        os.makedirs(export_path)
        
    for obj in collection.objects:
        if obj.type in {'MESH', 'CURVE'}:
            print(f"Exporting: {obj.name}")

            if obj.type == 'CURVE':
                # Duplicate so the original curve remains untouched
                duplicate = obj.copy()
                duplicate.data = obj.data.copy()
                collection.objects.link(duplicate)

                # Convert duplicate to mesh
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = duplicate
                duplicate.select_set(True)
                bpy.ops.object.convert(target='MESH')

                export_gltf(duplicate, export_path)

                # Remove temporary object
                bpy.data.objects.remove(duplicate, do_unlink=True)
            else:
                export_gltf(obj, export_path)

export_collection_to_gltf(collection_name, export_path)
print("Done")