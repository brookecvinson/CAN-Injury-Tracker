from components.main_screen import *
from file_operations import authenticate_drive

if __name__ == '__main__':
    drive = authenticate_drive()
    mainScreen = MainScreen()
    mainScreen.mainloop()


