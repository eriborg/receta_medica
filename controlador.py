from tkinter import Tk
import vista

__author__ = "Erica Borgeat"
__maintainer__ = "Erica Borgeat"
__copyright__ = "Copyright 2023"
__version__ = "0.1"

class Controller: 
    """
	    Inicia la Pantalla de Tkinter.
	
	    :param root: Ventana Principal del programa.
	"""
    def __init__(self, root):
        self.main = root
        self.main_window = vista.MainWindow(self.main)

if __name__ == "__main__":

    root_tk = Tk()
    app = Controller(root_tk)
    app.main_window.vista_tv()
    root_tk.mainloop()
