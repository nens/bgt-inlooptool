import sys
import arcpy


class GeneralUse:
    def __init__(self, logPrint=False, debug=False):
        """"Pass sys, arcpy. Starttime is initialised.
        logPrint = False voor logging zonder print functie"""
        import time
        self.startTime = time.clock()
        self.logPrint = logPrint
        self.debug = debug

    def StartAnalyse(self):
        """Reinitialise internal clock"""
        import time
        self.startTime = time.clock()

    def Traceback(self):
        """"Returns error messages in ArcPy object and prints them."""
        import traceback

        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + \
            "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = "\nArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
        arcpy.AddError(pymsg)
        arcpy.AddError(msgs)
        if self.logPrint:
            print(pymsg + "\n")
            print(msgs)

    def AddMessage(self, strMessage, urg=0):
        """Urg = 1 is Error Message, Urg = 2 is Warning Message."""
        if urg == 1:
            arcpy.AddError(strMessage)
        elif urg == 2:
            arcpy.AddWarning(strMessage)
        else:
            arcpy.AddMessage(strMessage)

    def AddTimeMessage(self, strMessage, urg=0):
        """Urg = 1 is Error Message, Urg = 2 is Warning Message."""
        import time
        strTime = "Elapsed time from start " + \
            str(round(time.clock() - self.startTime)) + \
            " seconds on " + time.strftime("%H:%M:%S") + "."
        if urg == 1:
            arcpy.AddError(strMessage)
            arcpy.AddMessage(strTime)
        elif urg == 2:
            arcpy.AddWarning(strMessage)
            arcpy.AddMessage(strTime)
        else:
            arcpy.AddMessage(strMessage)
            arcpy.AddMessage(strTime)
        if self.logPrint:
            print(strMessage)
            print(strTime)

    def AddDebug(self, strMessage):
        if self.debug is True:
            arcpy.AddMessage(strMessage)
            try:
                print(strMessage)
            except IOError:
                pass
