import watchdog as wd
from tkinter import * 
from tkinter import filedialog
import os
import time
import sys
import logging
import platform 
import pickle
import inspect
import re
from threading import Thread
from pathlib import Path
import subprocess as shell
from matplotlib import pyplot as plt
from watchdog.observers import Observer
# from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler


class Handler(FileSystemEventHandler): 

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print( "New Receipt- %s."  % event.src_path +" at " + time.strftime("%c", time.gmtime()) )
            App.saveReceiptToPhone(event.src_path ); 
        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            # print ("Received modified event - %s." % event.src_path)
            pass


# class Widgets: 

#     def __init__(self):
#         self.root =  None  
#         self.chooseDirBtn = None 
#         self.receiptDirLabel = None
#         self.scanDeviceBtn = None
#         self.adbList = None
#         self.adbNameLabel = None
#         self.adbIdLabel = None
#         self.lastReceiptImage = None
#         self.lastReceiptTmstmp = None
#         # self.mainLoop()




 
#     # def initWidgets(self): 
#     #     self.root = Tk()  
#     #     self.chooseDirBtn = Button(self.root, text = "Choose Receipts Directory", command = )


#     # def packWidgets(self): 
#     #     for attr in self.__dict__.items():
#     #         attr.pack()  

    

class App:
    deviceNameLabel = None
    def __init__(self):
        self.OS = ""
        self.prefsFile = "prefs.pkl"
        self.prefs = {
            "deviceId" :"",
            "recptDir":"",
        } 
        self.cnnctdDvcs = []
        self.device = None
        self.deviceName = "None"
        self.deviceId = ""
        self.recptDir = "None" 
        # widgets

        self.root =  None  
        self.chooseDirBtn = None 
        self.recptDirTextLabel = "Receipt Directory:"
        self.receiptDirLabel = None
        self.deviceNameTextLabel = None
        self.deviceNameLabel = None

        self.scanDeviceBtn = None
        self.curDirLabel = None
        self.curDir =""
        self.adbList = None
        self.adbNameLabel = None
        self.adbIdLabel = None
        self.lastReceiptImage = None
        self.lastReceiptTmstmpLabel = None 
        self.lastReceiptTmstmpLabelText = None 
        self.main()

    def linkDevice(self, data):
        print("lined?")
        self.deviceNameLabel.configure(text = " ".join( data)) 
        # adb -s 7f1c864e shell
        # shell.call(  ['adb' , '-s' , data[1], 'shell'],  shell = True)
        shell.Popen(['adb' , '-s' , data[1], 'shell']  , stdout=shell.PIPE, stderr=shell.PIPE)
        Thread(target = self.watchForRecptFiles).start()
        # self.watchForRecptFiles()

        # adb push Settings.apk /system/apps/

        # print(shell.check_output( ['adb' , '-s' , data[1], 'shell']) )
    def callback(self):
        print("hey file changed")
    def watchForRecptFiles(self):
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
        # path = sys.argv[1] if len(sys.argv) > 1 else '.'
        path = self.recptDir
        event_handler = Handler( )
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        # try:
        #     while True:
        #         # print('detecting')
        #         # time.sleep(1)
        #         pass
        # except KeyboardInterrupt:
        #     observer.stop()
        observer.join()
        pass
    
    @staticmethod
    def saveReceiptToPhone(  recptFilePath   ):
        
        shell.Popen(['adb' , 'push' , recptFilePath, 'storage/sdcard0/Papyrus Invoices'] , stdout=shell.PIPE, stderr=shell.PIPE  )
        #  'storage/sdcard0/com.aetherapps.papyrus/Papyrus Invoices'
        # updateRcptLabel()
        # caller.lastReceiptTmstmpLabel.configure(text =)
 
    def main(self):
        self.init()
    
    def checkDir(self):
        for aa in (shell.check_output(['cd'], shell = True)  ):
            self.curDir+= chr(aa)
        self.curDirLabel.configure(text = self.curDir)
        

    def savePrefs(self):
        filehandler = open(self.prefsFile,"wb")
        pickle.dump(self.prefs,filehandler)
        filehandler.close()
        
 

    def loadPrefs(self):  
        # loading preferences through pickle
        # if pref file exists, then set prefs to its value
        if(Path(self.prefsFile).is_file()): 
            prefsFile = open(self.prefsFile, "wb") 
            self.prefs = pickle.load(prefsFile)
            print("Loaded preferences")
            self.recptDir = self.prefs.get('recptDir')
            self.deviceId = self.prefs.get('deviceId')
            return True
        else: 
            print("Select Preferences")
            return False
 

    def chooseRecptDir(self):
        file  = filedialog.askdirectory()
        if(file != ""):
            self.recptDir = file
        # print(self.recptDir)
        self.receiptDirLabel.configure(text = self.recptDir)
        
        pass
    def setdeviceId(self):
        pass

    # @staticmethod
    # def linkDevice(  device):
    #     print(device)
    #     self.deviceNameLabel.configure(text = " ".join(device))
    #     pass
    
    


        
    def displayDevices(self):
        self.adbWdgts = []
        for a in self.cnnctdDvcs:
            self.adbWdgts.append(adbDevice(  self.root, a, self))
            # device = Frame(self.root)
            # label = Label(device, text = " ".join(a))
            # btn = Button(device, text = "LINK", command = lambda:self.linkDevice )
            # device.pack(side = TOP, pady = 10)
            # label.pack(side = LEFT)
            # btn.pack(side = RIGHT)


        pass
    def scanDevices(self):
        if("Win" in self.OS or "win" in self.OS):
            output = ""
            adbCodes = []
            reading = False
            currSub = ""
            
            

            for l in shell.check_output(['adb' ,  'devices'  ]): 
                l = chr(l) 
                output+=l
                if(l == '\n'):
                    reading = True
                if(l == '\t'):
                    reading = False
                    adbCodes.append(currSub)
                    currSub = ""
                if(reading and l!= '\n'):
                    currSub+=l 
            names = []
            for a in adbCodes:
                
                name = ""
                for b in (shell.check_output(['adb', '-s', a, 'shell', 'getprop' ,'ro.product.model'])):
                    name += chr(b)

                names.append(name.rstrip())
                self.cnnctdDvcs.append([name.rstrip(), a])
        if("Linux" in self.OS):
            pass

 
        self.displayDevices() 

    def init(self):  
        self.OS = platform.system()
        

        # if successful preferences load
        if(self.loadPrefs()):
            pass
        else: 
            pass
        self.initWidgets()
        self.checkDir()


        #   self.ui.root = Tk(screenName="Papyrus - Digital Receipt Solutioons")
#         # self.rootGui.title = "Papyrus - Digital Receipt Solutioons"
#         self.ui.root.geometry("480x700")
#         self.ui.root.update()
        
#         label = Label(self.ui.root, text = "helddddddddddddddddddddddddddddlo")
#         label.pack()

#         chooseDirBtn = Button(self.ui.root,text = "Choose Receipts Directory",command = self.chooseDir)
#         chooseDirBtn.place(x =  self.ui.root.winfo_width()/2, y = self.ui.root.winfo_height()/2)

    def initWidgets(self): 
        print("widgets inited")
        self.root = Tk(screenName="Main")  
        self.root.title("Papyrus - Digital Receipt Solutioons")
        self.root.geometry("480x700") 
        self.curDirLabel = Label(self.root, text = self.curDir)
        self.curDirLabel.pack(side = TOP, pady = 3)
        self.recptDirTextLabel = Label(self.root, text = self.recptDirTextLabel)
        self.recptDirTextLabel.pack(side = TOP, pady = 3)
        self.receiptDirLabel = Label(self.root, text = self.recptDir )
        self.receiptDirLabel.pack(side = TOP, pady =10 ) 
        
        self.chooseDirBtn = Button(self.root, text = "Choose Receipts Directory", command = self.chooseRecptDir )
        self.chooseDirBtn.pack( side = TOP, pady = 3)
        self.deviceNameTextLabel = Label(self.root, text = "Connected Device: ")
        self.deviceNameTextLabel.pack(side = TOP)
        self.deviceNameLabel = Label(self.root, text = self.deviceName+" "+ self.deviceId )
        self.deviceNameLabel.pack(side = TOP)
        self.adbCnnctBtn = Button(self.root, text = "Scan for connected devices", command = self.scanDevices)
        self.adbCnnctBtn.pack(side = TOP)

        self.adbNameLabel = Label(self.root, text = self.deviceId)
        self.adbIdLabel = Label(self.root, text =self.deviceId)

        # self.lastReceiptTmstmpLabelText = Label(self.root, text = "Last Receipt")
        # self.lastReceiptTmstmpLabel = Label(self.root, text = "") 
        # self.lastReceiptTmstmpLabelText.pack(side = TOP)
        # self.lastReceiptTmstmpLabel.pack(side = TOP)
        self.checkDir()
    


        
        self.mainLoop()
        



 
    def mainLoop(self):
        self.root.mainloop()

#     # def mainLoop(self):
#     #     self.root.mainloop()



class adbDevice :
    def __init__(self, root, a, parent):
        self.caller = parent
        self.data = a
        self.device = Frame(root)
        self.label = Label(self.device, text = " ".join(a))
        self.btn = Button(self.device, text = "LINK", command =  lambda: self.linkDeviceAdb()  )
        self.device.pack(side = TOP, pady = 10)
        self.label.pack(side = LEFT)
        self.btn.pack(side = RIGHT) 
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__
        the_method = stack[1][0].f_code.co_name
        # self.caller = the_class

        print("I was called by {}.{}()".format(str(the_class), the_method))
        # print(self.caller.items())
            
    def linkDeviceAdb(  self   ):
        print(self.data)
        self.caller.device = self.data
        
        self.caller.linkDevice(  self.data) 
        self.btn.configure(state = DISABLED, text = "LINKED")
        
    

app = App()

def updateRcptLabel():
        app.lastReceiptTmstmpLabel.configure(text = time.now() + "")
     
# root = tk.Tk()
# root.withdraw()


# file_path = filedialog.askdirectory()
# print(file_path)