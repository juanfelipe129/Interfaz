import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry

class FormularioVista:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Formulario de Registro")
        self.root.state("zoomed")  # Pantalla completa

        # Variables
        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.empresa_var = tk.StringVar()
        self.hijos_var = tk.IntVar(value=0)
        self.buscar_var = tk.StringVar()
        self.campo_var = tk.StringVar(value="Nombre")

        self.crear_menu()
        self.crear_formulario()
        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_salida)

    # --- Menú superior ---
    def crear_menu(self):
        menu_principal = tk.Menu(self.root)
        self.root.config(menu=menu_principal)

        # Menu Buscar
        menu_buscar = tk.Menu(menu_principal, tearoff=0)
        menu_principal.add_cascade(label="Buscar", menu=menu_buscar)
        menu_buscar.add_command(label="Buscar empresario", command=self.abrir_busqueda)

        # Menu Ayuda
        menu_ayuda = tk.Menu(menu_principal, tearoff=0)
        menu_principal.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Cómo usar", command=lambda: messagebox.showinfo("Ayuda",
            "Ingrese los datos del empresario y presione Enviar.\nPuede buscar empresarios usando el menú Buscar."))

        # Menu Créditos
        menu_creditos = tk.Menu(menu_principal, tearoff=0)
        menu_principal.add_cascade(label="Créditos", menu=menu_creditos)
        menu_creditos.add_command(label="Autores", command=lambda: messagebox.showinfo(
            "Créditos",
            "Hecho por Juan Felipe Almeciga Diaz y Daniel Rojas\nCorreo: juan.almeciga@uniminuto.edu.co"
        ))

    # --- Formulario ---
    def crear_formulario(self):
        frame = tk.Frame(self.root, padx=50, pady=30)
        frame.pack(fill="both", expand=True)

        # Título principal
        tk.Label(frame, text="Formulario de Registro", font=("Arial", 24, "bold")).pack(pady=10)

        # Subtítulo
        tk.Label(frame, text="Datos Empleado", font=("Arial", 18, "bold")).pack(pady=10)

        # Contenedor de campos
        campos_frame = tk.Frame(frame)
        campos_frame.pack(pady=20, anchor="w")

        # Nombre
        tk.Label(campos_frame, text="Nombre:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_entry = tk.Entry(campos_frame, textvariable=self.nombre_var, width=50)
        self.nombre_entry.grid(row=0, column=1, pady=5)
        self.nombre_entry.bind("<FocusOut>", self.capitalizar_nombre)

        # Correo
        tk.Label(campos_frame, text="Correo electrónico:", font=("Arial", 14)).grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(campos_frame, textvariable=self.correo_var, width=50).grid(row=1, column=1, pady=5)

        # Fecha
        tk.Label(campos_frame, text="Fecha de nacimiento:", font=("Arial", 14)).grid(row=2, column=0, sticky="w", pady=5)
        self.fecha_entry = DateEntry(campos_frame, textvariable=self.fecha_var, width=47,
                                     background="darkblue", foreground="white", borderwidth=2,
                                     date_pattern='dd/mm/yyyy')
        self.fecha_entry.grid(row=2, column=1, pady=5)

        # Teléfono
        tk.Label(campos_frame, text="Teléfono:", font=("Arial", 14)).grid(row=3, column=0, sticky="w", pady=5)
        tk.Entry(campos_frame, textvariable=self.telefono_var, width=50).grid(row=3, column=1, pady=5)

        # Empresa
        tk.Label(campos_frame, text="Empresa:", font=("Arial", 14)).grid(row=4, column=0, sticky="w", pady=5)
        tk.Entry(campos_frame, textvariable=self.empresa_var, width=50).grid(row=4, column=1, pady=5)

        # Cantidad de hijos
        tk.Label(campos_frame, text="Cantidad de hijos:", font=("Arial", 14)).grid(row=5, column=0, sticky="w", pady=5)
        tk.Spinbox(campos_frame, from_=0, to=20, textvariable=self.hijos_var, width=5, justify="center").grid(row=5, column=1, pady=5, sticky="w")

        # Botón enviar
        tk.Button(frame, text="Enviar", bg="#4CAF50", fg="white", font=("Arial", 14),
                  command=self.controlador.enviar_datos).pack(pady=20)

    # --- Capitalizar nombre ---
    def capitalizar_nombre(self, event=None):
        nombre = self.nombre_var.get().strip()
        if nombre:
            self.nombre_var.set(nombre.title())

    # --- Confirmar salida ---
    def confirmar_salida(self):
        if messagebox.askquestion("Confirmar salida", "¿Está seguro de que desea salir?", icon="warning") == "yes":
            self.root.destroy()

    # --- Mostrar error ---
    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)

    # --- Mostrar datos del formulario ---
    def mostrar_datos(self, datos):
        ventana = tk.Toplevel(self.root)
        ventana.title("Datos ingresados")
        ventana.geometry("600x400")
        ventana.grab_set()
        tk.Label(ventana, text="Información registrada:", font=("Arial", 12, "bold")).pack(pady=10)
        for clave, valor in datos.items():
            tk.Label(ventana, text=f"{clave}: {valor}", font=("Arial", 12), anchor="w").pack(pady=2, fill="x")

    # --- Abrir búsqueda de JSON ---
    def abrir_busqueda(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo JSON",
            filetypes=(("Archivos JSON", "*.json"), ("Todos los archivos", "*.*"))
        )
        if archivo:
            try:
                self.controlador.cargar_json(archivo)
                self.mostrar_ventana_busqueda()
            except Exception as e:
                self.mostrar_error(f"No se pudo leer el archivo:\n{e}")

    # --- Ventana de búsqueda ---
    def mostrar_ventana_busqueda(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Buscar empresarios")
        ventana.geometry("700x500")
        ventana.grab_set()

        # Campo de búsqueda
        tk.Label(ventana, text="Buscar por:", font=("Arial", 12)).pack(pady=5)
        opciones = ["Nombre", "Teléfono", "Empresa"]
        self.campo_var.set("Nombre")
        tk.OptionMenu(ventana, self.campo_var, *opciones).pack(pady=5)

        tk.Label(ventana, text="Valor a buscar:", font=("Arial", 12)).pack(pady=5)
        tk.Entry(ventana, textvariable=self.buscar_var, width=50).pack(pady=5)

        tk.Button(ventana, text="Buscar", bg="#2196F3", fg="white", font=("Arial", 12),
                  command=self.controlador.realizar_busqueda).pack(pady=10)

        # Resultado
        self.resultados_frame = tk.Frame(ventana)
        self.resultados_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # --- Mostrar resultados ---
    def mostrar_resultados(self, resultados):
        # Limpiar
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
        if not resultados:
            tk.Label(self.resultados_frame, text="No se encontraron resultados.", font=("Arial", 12)).pack()
            return
        for item in resultados:
            texto = ", ".join(f"{k}: {v}" for k, v in item.items())
            tk.Label(self.resultados_frame, text=texto, font=("Arial", 12), wraplength=650, justify="left", anchor="w").pack(pady=2, fill="x")
