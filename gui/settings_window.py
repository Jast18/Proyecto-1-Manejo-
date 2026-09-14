#Almacenara las dirferentes funciones como una pregrca del sistema general que ujunto con main conectaran y administraran junto a manager_config los datos de almacenamiento y ser4ealizacion
#Implementara una funcion mas que todo con tkinter al almacenar incluso una fotorgrafia para el usuario

import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from core import config_manager

COLOR_FONDO = "#f4f6f8"
COLOR_ACENTO = "#3a5a78"
COLOR_BOTON_GUARDAR = "#2e7d32"


class SettingsWindow(tk.Toplevel):
    def __init__(self, master, config_actual: dict, al_guardar_callback=None):  #al_guardar_callback nos ayuda a pasar la configuracion implementada a la ventana principal

        super().__init__(master) # Super(). llama al constructor de la clase "tk.Toplevel" para inicializar su vetana
        self.title("Settings")
        self.geometry("480x680")
        self.resizable(True, True)  # Ventana redimensionable: evita que el boton "Guardar" quede oculto si el contenido crece (ej. ruta larga de la foto)
        self.configure(bg=COLOR_FONDO)

        # tema 'clam' de ttk: a diferencia de los widgets nativos de macOS,
        # SI respeta los colores personalizados que le indiquemos -- soluciona
        # el problema de botones con texto invisible que tuvimos antes.
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TFrame", background=COLOR_FONDO)
        estilo.configure("TLabel", background=COLOR_FONDO, font=("Arial", 11))
        estilo.configure("Titulo.TLabel", background=COLOR_FONDO, font=("Arial", 12, "bold"), foreground=COLOR_ACENTO)
        estilo.configure("TRadiobutton", background=COLOR_FONDO, font=("Arial", 11))
        estilo.configure("TButton", font=("Arial", 10), padding=6)
        estilo.configure("Guardar.TButton", font=("Arial", 11, "bold"), foreground="white", background=COLOR_BOTON_GUARDAR)
        estilo.map("Guardar.TButton", background=[("active", "#1b5e20")])

        self.al_guardar_callback = al_guardar_callback

        self.color_barra = list(config_actual["color_barra"])
        self.color_letra = list(config_actual["color_letra"])
        self.ruta_foto_perfil = config_actual["foto_perfil"]

        self._construir_formulario(config_actual)

    def _construir_formulario(self, config_actual):
        contenedor = ttk.Frame(self, padding=20)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(contenedor, text="Configuración de usuario", style="Titulo.TLabel", font=("Arial", 16, "bold")).pack(anchor="w", pady=(0, 15))

        # --- Nombre de usuario ---
        ttk.Label(contenedor, text="Nombre de usuario", style="Titulo.TLabel").pack(anchor="w", pady=(10, 2))
        self.entry_nombre = ttk.Entry(contenedor, width=42, font=("Arial", 11))
        self.entry_nombre.insert(0, config_actual["nombre_usuario"])
        self.entry_nombre.pack(anchor="w", ipady=3)

        ttk.Separator(contenedor).pack(fill="x", pady=15)

        # --- Tema de la interfaz ---
        ttk.Label(contenedor, text="Tema de interfaz", style="Titulo.TLabel").pack(anchor="w", pady=(0, 2))
        self.var_tema = tk.StringVar(value=config_actual["tema_interfaz"])
        fila_tema = ttk.Frame(contenedor)
        fila_tema.pack(anchor="w", pady=(2, 0))
        ttk.Radiobutton(fila_tema, text="Claro", variable=self.var_tema, value="claro").pack(side="left", padx=(0, 20))
        ttk.Radiobutton(fila_tema, text="Oscuro", variable=self.var_tema, value="oscuro").pack(side="left")

        ttk.Separator(contenedor).pack(fill="x", pady=15)

        # --- Idioma ---
        ttk.Label(contenedor, text="Idioma", style="Titulo.TLabel").pack(anchor="w", pady=(0, 2))
        self.var_idioma = tk.StringVar(value=config_actual["idioma"])
        combo_idioma = ttk.Combobox(contenedor, textvariable=self.var_idioma, values=["es", "es-ES", "en", "en-US"], state="readonly", width=15, font=("Arial", 11))
        combo_idioma.pack(anchor="w")

        ttk.Separator(contenedor).pack(fill="x", pady=15)

        # --- Tamaño de fuente ---
        ttk.Label(contenedor, text="Tamaño de fuente", style="Titulo.TLabel").pack(anchor="w", pady=(0, 2))
        self.entry_tamano_fuente = ttk.Entry(contenedor, width=8, font=("Arial", 11))
        self.entry_tamano_fuente.insert(0, str(config_actual["tamaño_fuente"]))
        self.entry_tamano_fuente.pack(anchor="w", ipady=3)

        ttk.Separator(contenedor).pack(fill="x", pady=15)

        # --- Colores ---
        fila_colores = ttk.Frame(contenedor)
        fila_colores.pack(fill="x", pady=(0, 5))

        col_barra = ttk.Frame(fila_colores)
        col_barra.pack(side="left", padx=(0, 30))
        ttk.Label(col_barra, text="Color de la barra de menú", style="Titulo.TLabel").pack(anchor="w", pady=(0, 5))
        self.boton_color_barra = tk.Button(
            col_barra, text="Elegir color", command=self._elegir_color_barra,
            bg=self._rgb_a_hex(self.color_barra), width=14, relief="flat", borderwidth=1
        )
        self.boton_color_barra.pack(anchor="w")

        col_letra = ttk.Frame(fila_colores)
        col_letra.pack(side="left")
        ttk.Label(col_letra, text="Color de letra", style="Titulo.TLabel").pack(anchor="w", pady=(0, 5))
        self.boton_color_letra = tk.Button(
            col_letra, text="Elegir color", command=self._elegir_color_letra,
            bg=self._rgb_a_hex(self.color_letra), width=14, relief="flat", borderwidth=1
        )
        self.boton_color_letra.pack(anchor="w")

        ttk.Separator(contenedor).pack(fill="x", pady=15)

        # --- Foto de perfil ---
        ttk.Label(contenedor, text="Foto de perfil", style="Titulo.TLabel").pack(anchor="w", pady=(0, 5))
        self.label_ruta_foto = ttk.Label(contenedor, text=self.ruta_foto_perfil or "(ninguna seleccionada)", wraplength=420, foreground="#666666")
        self.label_ruta_foto.pack(anchor="w", pady=(0, 8))
        ttk.Button(contenedor, text="Seleccionar imagen...", command=self._elegir_foto).pack(anchor="w")

        # --- Guardar ---
        ttk.Button(contenedor, text="Guardar cambios", style="Guardar.TButton", command=self._guardar).pack(pady=30, ipadx=10, ipady=4)

    def _rgb_a_hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    def _elegir_color_barra(self):
        color = colorchooser.askcolor(title="Color de la barra de menú")
        if color[0] is not None:  #Si el usuario no aplica los cambios cnacela la seleccion, sewrqa el primer dato en la lista de color
            self.color_barra = [int(c) for c in color[0]]
            self.boton_color_barra.config(bg=self._rgb_a_hex(self.color_barra))

    def _elegir_color_letra(self):
        color = colorchooser.askcolor(title="Color de letra")
        if color[0] is not None:
            self.color_letra = [int(c) for c in color[0]]
            self.boton_color_letra.config(bg=self._rgb_a_hex(self.color_letra)) #bg=self.rge_a_hex(self.color_letra) nos ayuda a cambiar el color del boton que se selecciono

    def _elegir_foto(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona una foto de perfil",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
        )
        if ruta:  # askopenfilename devuelve una cadena vacia si selecciona cancelar el usuario
            self.ruta_foto_perfil = ruta
            self.label_ruta_foto.config(text=ruta)

    def _guardar(self):
        try:
            tamano_fuente = int(self.entry_tamano_fuente.get())
        except ValueError:
            messagebox.showerror("Error", "El tamaño de fuente debe ser un número entero.")
            return

        nueva_config = {
            "nombre_usuario": self.entry_nombre.get(),
            "tema_interfaz": self.var_tema.get(),
            "idioma": self.var_idioma.get(),
            "tamaño_fuente": tamano_fuente,
            "color_barra": tuple(self.color_barra),
            "color_letra": tuple(self.color_letra),
            "foto_perfil": self.ruta_foto_perfil
        }

        exito = config_manager.guardar_configuracion(nueva_config)

        if exito:
            messagebox.showinfo("Settings", "Configuración guardada correctamente")
            if self.al_guardar_callback:
                self.al_guardar_callback(nueva_config)
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar la configuración. Revisa los permisos del archivo")