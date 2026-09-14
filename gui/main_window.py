import tkinter as tk
from tkinter import ttk, Menu
from gui.settings_window import SettingsWindow

COLOR_ACENTO = "#3a5a78"


class MainWindow(tk.Tk):
    def __init__(self, config_inicial: dict):
        super().__init__()
        self.title("Aplicacion de Configuracion de Usuario")
        self.geometry("520x360")

        self.config_actual = config_inicial

        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("Bienvenida.TLabel", font=("Arial", 18, "bold"))
        estilo.configure("Info.TLabel", font=("Arial", 12))
        estilo.configure("Settings.TButton", font=("Arial", 11, "bold"), padding=10, foreground="white", background=COLOR_ACENTO)
        estilo.map("Settings.TButton", background=[("active", "#2c4459")])

        self._construir_menu()
        self._construir_contenido()
        self._aplicar_configuracion_visual()

    def _construir_menu(self):
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
        self.tarjeta = ttk.Frame(self, padding=30)
        self.tarjeta.pack(fill="both", expand=True)

        self.label_bienvenida = ttk.Label(self.tarjeta, text="", style="Bienvenida.TLabel")
        self.label_bienvenida.pack(pady=(20, 15))

        self.label_info = ttk.Label(self.tarjeta, text="", justify="left", style="Info.TLabel")
        self.label_info.pack(pady=10) # Espacio entre la información y el botón
        ttk.Button(self.tarjeta, text="Abrir Settings", style="Settings.TButton", command=self._abrir_settings).pack(pady=25)

    def _abrir_settings(self):
        SettingsWindow(self, self.config_actual, al_guardar_callback=self._al_guardar)

    def _al_guardar(self, nueva_config: dict):
        """Callback que SettingsWindow llama despues de guardar exitosamente."""
        self.config_actual = nueva_config
        self._aplicar_configuracion_visual()

    def _aplicar_configuracion_visual(self):

        # Ajusta colores y fuentes de la ventana principal segun la configuracion actual
        color_fondo = "#2b2b2b" if self.config_actual["tema_interfaz"] == "oscuro" else "#ffffff"

        r, g, b = self.config_actual["color_letra"]
        color_letra_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)

        tamano = self.config_actual["tamaño_fuente"]

        self.configure(bg=color_fondo)
        self.tarjeta.configure(style="Tarjeta.TFrame")

        estilo = ttk.Style(self)
        estilo.configure("Tarjeta.TFrame", background=color_fondo)
        estilo.configure("Bienvenida.TLabel", background=color_fondo, foreground=color_letra_hex, font=("Arial", tamano + 8, "bold"))
        estilo.configure("Info.TLabel", background=color_fondo, foreground=color_letra_hex, font=("Arial", tamano))

        self.label_bienvenida.config(text=f"Bienvenido, {self.config_actual['nombre_usuario']}")

        info = (
            f"Idioma: {self.config_actual['idioma']}\n"
            f"Tema: {self.config_actual['tema_interfaz']}\n"
            f"Tamaño de fuente: {tamano}"
        )
        self.label_info.config(text=info)