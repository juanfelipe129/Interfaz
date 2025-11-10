from model.form import FormularioModelo
from views.app_view import FormularioVista

class FormularioControlador:
    def __init__(self, root):
        self.modelo = FormularioModelo()
        self.vista = FormularioVista(root, self)

    # --- Enviar datos del formulario ---
    def enviar_datos(self):
        nombre = self.vista.nombre_var.get().strip()
        correo = self.vista.correo_var.get().strip()
        fecha = self.vista.fecha_var.get().strip()
        telefono = self.vista.telefono_var.get().strip()
        empresa = self.vista.empresa_var.get().strip()
        hijos = self.vista.hijos_var.get()

        # Capitalizar
        nombre = nombre.title()
        self.vista.nombre_var.set(nombre)

        # Validaciones
        if not nombre:
            self.vista.mostrar_error("Debe ingresar un nombre.")
            return
        if "@" not in correo or "." not in correo:
            self.vista.mostrar_error("El correo electrónico no es válido.")
            return
        if not telefono.isdigit():
            self.vista.mostrar_error("El teléfono solo debe contener números.")
            return

        # Guardar y mostrar
        self.modelo.guardar_datos(nombre, correo, fecha, telefono, empresa, hijos)
        self.vista.mostrar_datos(self.modelo.obtener_datos())

    # --- Cargar JSON ---
    def cargar_json(self, archivo):
        return self.modelo.cargar_json(archivo)

    # --- Realizar búsqueda ---
    def realizar_busqueda(self):
        campo = self.vista.campo_var.get()
        valor = self.vista.buscar_var.get().strip()
        if not valor:
            self.vista.mostrar_error("Ingrese un valor para buscar.")
            return
        resultados = self.modelo.buscar_json(campo, valor)
        self.vista.mostrar_resultados(resultados)

