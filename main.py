from core import config_manager
from gui.main_window import MainWindow
 
if __name__ == "__main__":
    config = config_manager.cargar_configuracion()
    app = MainWindow(config)
    app.mainloop()