import json

class FormularioModelo:
    def __init__(self):
        self.datos = {}
        self.json_data = []

    # Guardar los datos del formulario en memoria
    def guardar_datos(self, nombre, correo, fecha, telefono, empresa, hijos):
        self.datos = {
            "Nombre": nombre,
            "Correo": correo,
            "Fecha de nacimiento": fecha,
            "Teléfono": telefono,
            "Empresa": empresa,
            "Cantidad de hijos": hijos
        }

    def obtener_datos(self):
        return self.datos

    # Cargar JSON desde archivo
    def cargar_json(self, archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            self.json_data = json.load(f)
        return self.json_data

    # Buscar en JSON por nombre, teléfono o empresa
    def buscar_json(self, campo, valor):
        valor = valor.lower()
        resultados = []
        for item in self.json_data:
            if campo in item and valor in str(item[campo]).lower():
                resultados.append(item)
        return resultados




