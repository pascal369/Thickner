#***************************************************************************
#*    Copyright (C) 2023 
#*    This library is free software
#***************************************************************************
import inspect
import os
import sys
import FreeCAD
import FreeCADGui

class thicknerShowCommand:
    def GetResources(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        return { 
          'Pixmap': os.path.join(module_path, "icons", "thickner.svg"),
          'MenuText': "thickner",
          'ToolTip': "Show/Hide thickner"}

    def IsActive(self):
        import Thickner
        Thickner
        return True

    def Activated(self):
        try:
          import Thickner
          Thickner.main.d.show()
        except Exception as e:
          FreeCAD.Console.PrintError(str(e) + "\n")

    def IsActive(self):
        import Thickner
        return not FreeCAD.ActiveDocument is None

class thicknerWB(FreeCADGui.Workbench):
    def __init__(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        self.__class__.Icon = os.path.join(module_path, "icons", "thickner.svg")
        self.__class__.MenuText = "thickner"
        self.__class__.ToolTip = "thickner by Pascal"

    def Initialize(self):
        self.commandList = ["thickner_Show"]
        self.appendToolbar("&thickner", self.commandList)
        self.appendMenu("&thickner", self.commandList)

    def Activated(self):
        import Thickner
        Thickner
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        return

    def GetClassName(self): 
        return "Gui::PythonWorkbench"
FreeCADGui.addWorkbench(thicknerWB())
FreeCADGui.addCommand("thickner_Show", thicknerShowCommand())

