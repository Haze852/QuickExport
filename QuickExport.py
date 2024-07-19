import maya.cmds as mc
import maya.mel as mel
import os

def Export_selected_mesh(save_path, *args):
    selected_objects = mc.ls(selection= True, type= 'transform')

    if not selected_objects:
        mc.warning('No mesh object is currently selected.')
        return

    if not save_path:
        mc.warning('Save path is not specified.')
        return

    # Create a temporary file path
    temp_file_path = os.path.join(save_path, 'temp.ma')

    # Export the selected mesh as a .ma file
    mc.select(selected_objects, replace= True)
    mc.file(temp_file_path, exportSelected= True, type='mayaAscii', force= True)

    print('Selected mesh exported as temp.ma to the specified path.')


def Load_temp_file(save_path, *args):
    if not save_path:
        mc.warning('Save path is not specified.')
        return

    # Check if the temp.ma file exists
    temp_file_path = os.path.join(save_path, 'temp.ma')

    if not os.path.exists(temp_file_path):
        mc.warning('The temp.ma file does not exist at the specified save path.')
        return

    # Import the temp.ma file into the scene
    mc.file(temp_file_path, i= True, type= 'mayaAscii', ignoreVersion= True, namespace= 'Temp' )

    # Namespace
    print('temp.ma file loaded into the scene.')

def Merge_namespace():
    selected_objects = mc.ls(selection=True)
    namespaces = set()
    for obj in selected_objects:
        # Check if the object has a namespace
        if ':' in obj:
            # Split the object name to get the namespace and the name
            namespace = obj.split(':')[0]
            namespaces.add(namespace)

    # Merge each namespace with root
    for ns in namespaces:
        # Move all objects in the namespace to the root namespace
        mc.namespace(moveNamespace=[ns, ":"], force=True)
        # Remove the now empty namespace
        mc.namespace(removeNamespace=ns)

    print("Namespaces merged with root for selected objects.")

def Create_window():
    window_name = 'QuickExport'

    # Check if the window already exists, and if so, delete it
    if mc.window(window_name, exists= True):
       mc.deleteUI(window_name)

    # Create the main window
    window = mc.window(window_name, title= 'Quick Export', minimizeButton= False, maximizeButton= False, sizeable=False)
    cH0 = mc.columnLayout (adj= True, w= 300)
    mc.text(l= '')
    mc.rowColumnLayout (numberOfColumns= 5)

    # Save path text field with default path set to maya default project scenes folder.
    default_save_path = mc.internalVar(uwd= 1) + 'default/scenes'
    save_path_field = mc.textFieldGrp(label= 'Path : ', columnWidth= [1, 40], text= default_save_path)
    mc.text(l= '')

    # Button to select the save path from the computer
    mc.button(label=' ... ',
                c=lambda *args: mc.textFieldGrp(save_path_field, edit=True,
                                                       text=mc.fileDialog2(fileMode=3,
                                                                             caption= 'Select Save Path',
                                                                             startingDirectory=default_save_path)[0]))
    mc.text(l= '')
    mc.setParent(cH0)
    mc.text(l= '')

    cH1 = mc.columnLayout (adj= True)  
    mc.rowColumnLayout (numberOfColumns= 7)

    mc.text(l= '')

    # Button to load temp.ma into scene
    mc.button(label='> Import',h= 40, w= 70,
                c= lambda *args: Load_temp_file(mc.textFieldGrp(save_path_field, query= True, text= True)))
   
    mc.text(l= '   ')
    mc.button(label= 'Remove Namespace', c= lambda _: Merge_namespace())
    mc.separator(w= 53, hr= False)


    # Button to export selected mesh as temp.ma
    mc.button(label='Export >',w= 70,
                c=lambda *args: Export_selected_mesh(mc.textFieldGrp(save_path_field, query= True, text= True)))
    mc.text(l= '')
    mc.text(l= '')

    mc.setParent(cH1)

    mc.showWindow(window)
    

# Call the function to create the window
Create_window()
