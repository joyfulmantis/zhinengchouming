from wx import App
#import wx.lib.inspection
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass

from widgets.main_frame import MainFrame

if __name__ == '__main__':
    screen_app = App()
    main_frame = MainFrame()
    #wx.lib.inspection.InspectionTool().Show()
    screen_app.MainLoop()
