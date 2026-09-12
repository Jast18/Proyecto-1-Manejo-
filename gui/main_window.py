
import tkinter as tk
from tkinter import Menu
from gui.settings_window import SettingsWindow


class MainWindow(tk.Tk):
    def __init__(self, config_inicial: dict):
        super().__init__()
        self.title("Aplicacion de Configuracion de Usuario")
        self.geometry("500x320")

        self.config_actual = config_inicial

        self._construir_menu()
        self._construir_contenido()
        self._aplicar_configuracion_visual()

    def _construir_menu(self): #Iniciamos con la construccion de el manu en barra
        barra_menu = Menu(self)

        menu_archivo = Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Nuevo")
        menu_archivo.add_command(label="Abrir")
        menu_archivo.add_command(label="Guardar")
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

        menu_edicion = Menu(barra_menu, tearoff=0)
        menu_edicion.add_command(label="Copiar")
        menu_edicion.add_command(label="Pegar")
        barra_menu.add_cascade(label="Edicion", menu=menu_edicion)

        menu_ver = Menu(barra_menu, tearoff=0)
        menu_ver.add_command(label="Zoom")
        barra_menu.add_cascade(label="Ver", menu=menu_ver)

        # Unico item funcional del menu: abre la ventana de Settings
        barra_menu.add_command(label="Settings", command=self._abrir_settings)

        self.config(menu=barra_menu)

    def _construir_contenido(self):
        self.label_bienvenida = tk.Label(self, text="") # tk.Label exportaran los parametros de texto y la configuracion de la ventana principal
        self.label_bienvenida.pack(pady=30) #pady = 30 nos ayuda a almacenar un espacio especificado en este caso de 30 para cada celda

        self.label_info = tk.Label(self, text="", justify="left") #justify = "left" alineamos el texto a a izquierda
        self.label_info.pack(pady=10)

    def _abrir_settings(self):
        SettingsWindow(self, self.config_actual, al_guardar_callback=self._al_guardar)

    def _al_guardar(self, nueva_config: dict):
        
        self.config_actual = nueva_config
        self._aplicar_configuracion_visual()

    def _aplicar_configuracion_visual(self):

        color_fondo = "#2b2b2b" if self.config_actual["tema_interfaz"] == "oscuro" else "#f5f5f5"
        color_texto_tema = "#ffffff" if self.config_actual["tema_interfaz"] == "oscuro" else "#000000"

        r, g, b = self.config_actual["color_letra"]
        color_letra_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)

        tamano = self.config_actual["tamaño_fuente"]

        self.configure(bg=color_fondo)

        self.label_bienvenida.config(
            text=f"Bienvenido, {self.config_actual['nombre_usuario']}",
            font=("Arial", tamano + 4, "bold"),
            fg=color_letra_hex,
            bg=color_fondo,
        )

        info = (
            f"Idioma: {self.config_actual['idioma']}\n"
            f"Tema: {self.config_actual['tema_interfaz']}\n"
            f"Tamaño de fuente: {tamano}"
        )
        self.label_info.config(
            text=info,
            font=("Arial", tamano),
            fg=color_letra_hex,
            bg=color_fondo,
        )