class TT_GeneralUse():
    def __init__(self, sys, arcpy, logPrint=False, debug=False):
        """"Pass sys, arcpy. Starttime is initialised.
        logPrint = False voor logging zonder print functie"""
        self.sys = sys
        self.arcpy = arcpy
        import time
        self.startTime = time.clock()
        self.logPrint = logPrint
        self.debug = debug

        if self.logPrint is False:
            print("Let op. Log Print is uitgeschakeld.")

    def StartAnalyse(self):
        """Reinitialise internal clock"""
        import time
        self.startTime = time.clock()

    def Traceback(self):
        """"Returns error messages in ArcPy object and prints them."""
        import traceback

        tb = self.sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + \
            "\nError Info:\n" + str(self.sys.exc_info()[1])
        msgs = "\nArcPy ERRORS:\n" + self.arcpy.GetMessages(2) + "\n"
        self.arcpy.AddError(pymsg)
        self.arcpy.AddError(msgs)
        if self.logPrint:
            print(pymsg + "\n")
            print(msgs)

    def AddMessage(self, strMessage, urg=0):
        """Urg = 1 is Error Message, Urg = 2 is Warning Message."""
        if urg == 1:
            self.arcpy.AddError(strMessage)
        elif urg == 2:
            self.arcpy.AddWarning(strMessage)
        else:
            self.arcpy.AddMessage(strMessage)
        if self.logPrint:
            print(strMessage)

    def AddTimeMessage(self, strMessage, urg=0):
        """Urg = 1 is Error Message, Urg = 2 is Warning Message."""
        import time
        strTime = "Elapsed time from start " + \
            str(round(time.clock() - self.startTime)) + \
            " seconds on " + time.strftime("%H:%M:%S") + "."
        if urg == 1:
            self.arcpy.AddError(strMessage)
            self.arcpy.AddMessage(strTime)
        elif urg == 2:
            self.arcpy.AddWarning(strMessage)
            self.arcpy.AddMessage(strTime)
        else:
            self.arcpy.AddMessage(strMessage)
            self.arcpy.AddMessage(strTime)
        if self.logPrint:
            print(strMessage)
            print(strTime)

    def AddDebug(self, strMessage):
        if self.debug is True:
            self.arcpy.AddMessage(strMessage)
            try:
                print(strMessage)
            except IOError:
                pass


if __name__ == '__main__':

    print('klaar!')
