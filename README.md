1. Pyinstaller packages your python script to a stand alone desktop executable. To install, pip install pyinstaller
2. locate folder in command line then write
    'pyinstaller ${nameofscript.py}' , e.g. pyinstaller launcher.py
3. output exe of pyinstaller is in ./dist , copy that file to PAPYRUS and replace the LAUNCHER.exe.
4. That is the executable file, run the file and you're good to go.

This is just an mvp, i believe we can make something better. The features of the desktop app will be listening to receipt file saves, connecting to an android peripheral device, transfering the file to the device, and perform analytics and machine learning to the stored receipts. (sales mix, and market basket). The first three features are already implemented in this code. Ofc this code needs better ui. The receipts directory is where this app will listen to file writes, the choose phone is the phone this app will save the read new receipts. Make sure to have drivers installed.