from datetime import date

class Ingrediente:
    def __init__(self, nombre, tipo, unidad, cantidad_disponible, precio_unitario):
        self.nombre = nombre
        self.tipo = tipo
        self.unidad = unidad
        self.stock = cantidad_disponible  # antes llamado cantidad
        self.precio_unitario = precio_unitario

    def usar(self, cantidad):
        if cantidad > self.stock:
            raise ValueError(f"No hay suficiente {self.nombre}. Stock disponible: {self.stock}")
        self.stock -= cantidad

class Receta:
    def __init__(self, nombre, litros_objetivo):
        self.nombre = nombre
        self.litros_objetivo = litros_objetivo
        self.ingredientes = []  # Aquí es donde guardamos los ingredientes usados

    def agregar_ingrediente(self, ingrediente, cantidad):
        ingrediente.usar(cantidad)
        self.ingredientes.append((ingrediente, cantidad))

    def calcular_costo_total(self):
        total = 0
        for ing, cantidad in self.ingredientes:
            total += cantidad * ing.precio_unitario
        return total

    def calcular_costo_por_litro(self):
        if self.litros_objetivo == 0:
            return 0
        return self.calcular_costo_total() / self.litros_objetivo


class Lote:
    def __init__(self, receta, fecha, densidad_inicial, densidad_final, litros_embotellados):
        self.receta = receta
        self.fecha = fecha
        self.densidad_inicial = densidad_inicial
        self.densidad_final = densidad_final
        self.litros_embotellados = litros_embotellados

    def abv(self):
        return round((self.densidad_inicial - self.densidad_final) * 131.25, 2)

    def costo_por_litro(self):
        return round(self.receta.costo_total() / self.litros_embotellados, 2)

    def calcular_abv(self):
    # Fórmula común para calcular ABV: (OG - FG) * 131.25
        return round((self.densidad_inicial - self.densidad_final) * 131.25, 2)

