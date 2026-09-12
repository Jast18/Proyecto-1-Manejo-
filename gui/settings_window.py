#Almacenara las dirferentes funciones como una pregrca del sistema general que ujunto con main conectaran y administraran junto a manager_config los datos de almacenamiento y ser4ealizacion
#Implementara una funcion mas que todo con tkinter al almacenar incluso una fotorgrafia para el usuario

import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from core import config_manager


class SettingsWindow(tk.Toplevel):
    def __init__(self, master, config_actual: dict, al_guardar_callback=None):  #al_guardar_callback nos ayuda a pasar la configuracion implementada a la ventana principal

        super().__init__(master) # Super(). llama al constructor de la clase "tk.Toplevel" para inicializar su vetana
        self.title("Settings")
        self.geometry("420x480")

        self.al_guardar_callback = al_guardar_callback

        self.color_barra = list(config_actual["color_barra"])
        self.color_letra = list(config_actual["color_letra"])
        self.ruta_foto_perfil = config_actual["foto_perfil"]

        self._construir_formulario(config_actual)

    def _construir_formulario(self, config_actual):
        
        tk.Label(self, text="Nombre de usuario:").pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_nombre = tk.Entry(self, width=40)
        self.entry_nombre.insert(0, config_actual["nombre_usuario"])
        self.entry_nombre.pack(padx=10)

        #Tema de la interfaaz
        tk.Label(self, text="Tema de interfaz:").pack(anchor="w", padx=10, pady=(10, 0))
        self.var_tema = tk.StringVar(value=config_actual["tema_interfaz"])
        tk.Radiobutton(self, text="Claro", variable=self.var_tema, value="claro").pack(anchor="w", padx=20)
        tk.Radiobutton(self, text="Oscuro", variable=self.var_tema, value="oscuro").pack(anchor="w", padx=20)

        #Seleccion del idioma
        tk.Label(self, text="Idioma:").pack(anchor="w", padx=10, pady=(10, 0))
        self.var_idioma = tk.StringVar(value=config_actual["idioma"])
        opciones_idioma = ["es", "es-ES", "en", "en-US"]
        tk.OptionMenu(self, self.var_idioma, *opciones_idioma).pack(anchor="w", padx=10)

        # Tamaño de la fuente
        tk.Label(self, text="Tamaño de fuente:").pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_tamano_fuente = tk.Entry(self, width=10)
        self.entry_tamano_fuente.insert(0, str(config_actual["tamaño_fuente"]))
        self.entry_tamano_fuente.pack(anchor="w", padx=10)

        # Color barra de menu
        tk.Label(self, text="Color de la barra de menú:").pack(anchor="w", padx=10, pady=(10, 0))
        self.boton_color_barra = tk.Button(
            self, text="Elegir color", command=self._elegir_color_barra,
            bg=self._rgb_a_hex(self.color_barra)
        )
        self.boton_color_barra.pack(anchor="w", padx=10)

        # Letra
        tk.Label(self, text="Color de letra:").pack(anchor="w", padx=10, pady=(10, 0))
        self.boton_color_letra = tk.Button(
            self, text="Elegir color", command=self._elegir_color_letra,
            bg=self._rgb_a_hex(self.color_letra)
        )
        self.boton_color_letra.pack(anchor="w", padx=10)

        # Perfil
        tk.Label(self, text="Foto de perfil:").pack(anchor="w", padx=10, pady=(10, 0))
        self.label_ruta_foto = tk.Label(self, text=self.ruta_foto_perfil or "(ninguna seleccionada)", wraplength=380)
        self.label_ruta_foto.pack(anchor="w", padx=10)
        tk.Button(self, text="Seleccionar imagen...", command=self._elegir_foto).pack(anchor="w", padx=10, pady=(5, 0))

        # Almacenar los cambios seleccionados 
        tk.Button(self, text="Guardar", command=self._guardar, bg="#4CAF50", fg="white").pack(pady=20)

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
            messagebox.showinfo("Settings", "Configuración guardada correctamentee")
            if self.al_guardar_callback:
                self.al_guardar_callback(nueva_config)
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar la configuración... Revisa los permisos del archivo")