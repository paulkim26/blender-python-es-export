import bpy
import os

'''
Blender python script to easily mass export a collection of objects for use in Escape Simulator.
- Export objects from a specific collection to a specific folder
- Apply all modifiers
- .gltf format only
- Each export in its only folder
- Each folder and exported gltf matches the object's name
'''

# Parameters
collection_name = "export"
export_folder = "C:/filepath"

def export_gltf(obj, export_folder):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    object_name = obj.name
    object_export_path = os.path.join(export_folder, object_name)
    
    if not os.path.exists(object_export_path):
        os.makedirs(object_export_path)
        
    bpy.ops.export_scene.gltf(
        filepath=os.path.join(object_export_path, f"{object_name}.gltf"),
        export_format='GLTF_SEPARATE', # Keep separate textures
        use_selection=True, # Export selected only
        export_apply=True, # Apply modifiers
    )
    
    obj.select_set(False)

def export_collection_to_gltf(collection_name, export_folder):
    # Get the collection by name
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"Collection '{collection_name}' not found.")
        return
    
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
        
    for obj in collection.objects:
        if obj.type == 'MESH':  # Export only mesh objects
            print(f"Exporting: {obj.name}")
            export_gltf(obj, export_folder)

export_collection_to_gltf(collection_name, export_folder)
print("Done")
