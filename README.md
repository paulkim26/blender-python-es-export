# blender-python-es-export

![blender-python-es-export-preview](https://github.com/user-attachments/assets/971295aa-aa0c-4e1f-acb2-93c7b40e47bc)

**WARNING**: This script comes with no warranty. Make backups of your room/model if this is your first time using this.

Simple repeatable Blender Python script to mass export objects for use in Escape Simulator Room Editor.

This is helpful if you find it annoying to:
- Individually export individual objects one by one from Blender.
- Double check that the proper Blender `.gltf` export options are correctly configured for Escape Simulator.
- Copy and paste them to your `UGC` directory in your file browser.

## Features

Exports models for Escape Simulator with these settings:
- `.gltf` format
- Applies all mesh modifiers
- Exports objects to their own directories
- Corrects the exported object's origin to `(0, 0, 0)`

## Requisites

This has been tested for:
- Windows 11
- Escape Simulator `v35389r` (Steam version as of February 1, 2025)
- Blender `4.3.2`

This should run fine for Linux/Mac and future Blender versions, but YMMV.

## Install

1. Open Blender.
2. Go to the "Scripting" tab.
3. Copy and paste the contents of `es-export.py` into the text editor.
4. In the script, change the `export_path` directory to point to your Escape Simulator room's `_CustomModels` folder.

Example:

```export_path = "C:/Users/Dude/AppData/LocalLow/Pine Studio/Escape Simulator/UGC/Room_1/_CustomModels"```

![image](https://github.com/user-attachments/assets/7ac8058e-e8fa-4673-8c38-5c11e0b51b81)

## Usage

1. In Blender, create a collection called `export` and put the mesh objects you want to export in there.
1. Run the script in Blender (click the "Run Script" button or press `Alt-P`).
2. You should now see the models.
    - If in Escape Simulator your Room Editor window was already open, you will need to exit back to the main menu and open your room again to see the updated models.
3. Re-run the script when your models are updated in Blender to export them again.

![image](https://github.com/user-attachments/assets/d1cb3be2-af59-4aca-9553-3f7e0fd4d2fd)


## Example

Let's say your Blender scene collection has the following objects in a collection named `export`:

```
/export
    mdl_box
    mdl_can
    mdl_shoe
```

![image](https://github.com/user-attachments/assets/3988b2a5-1b77-418b-bc45-319933c33d32)


These objects can have Blender Modifiers on them, those will be applied.

You run the script. You check your Escape Simulator `UGC` folder and will now see:

```
C:/Users/Dude/AppData/LocalLow/Pine Studio/Escape Simulator/UGC
    /Room_1
        /_CustomModels
            /mdl_box
                mdl_box.bin
                mdl_box.gltf
            /mdl_can
                mdl_can.bin
                mdl_can.gltf
            /mdl_shoe
                mdl_shoe.bin
                mdl_shoe.gltf
```

![image](https://github.com/user-attachments/assets/a70d43f6-2a01-4293-8806-7e1100e73827)


