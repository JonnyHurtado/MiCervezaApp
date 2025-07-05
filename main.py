from app.modelo import Ingrediente, Receta, Lote
from app.datos import cargar_ingredientes
from app.logica import crear_lote, crear_receta_desde_consola
from app.logica import crear_lote_interactivo
from datetime import date
from app.logica import crear_lote, crear_receta_desde_consola, mostrar_resumen_lotes
from app.estadisticas import obtener_estadisticas_lotes


def mostrar_ingredientes(inventario):
    print("\n📦 Ingredientes disponibles:")
    for i, ing in enumerate(inventario):
        print(f"{i + 1}. {ing.nombre} ({ing.tipo}) - {ing.precio_unitario:.2f}/gr - Stock: {ing.stock}g")

def seleccionar_ingrediente(inventario):
    mostrar_ingredientes(inventario)
    try:
        seleccion = int(input("\nSelecciona el número del ingrediente: "))
        if 1 <= seleccion <= len(inventario):
            return inventario[seleccion - 1]
        else:
            print("Número fuera de rango.")
    except ValueError:
        print("Entrada inválida.")
    return None

def crear_receta_interactiva(inventario):
    nombre = input("\n🧪 Nombre de la nueva receta: ")
    litros = float(input("🎯 Litros objetivo: "))
    receta = Receta(nombre, litros)

    while True:
        ing = seleccionar_ingrediente(inventario)
        if ing:
            cantidad = float(input(f"Cantidad (en gramos) de {ing.nombre} a usar: "))
            receta.agregar_ingrediente(ing, cantidad)
            print(f"✅ {cantidad}g de {ing.nombre} agregado.")
        otra = input("¿Agregar otro ingrediente? (s/n): ").lower()
        if otra != "s":
            break

    return receta

def crear_lote_interactivo(receta):
    fecha = input("\n📅 Fecha del lote (YYYY-MM-DD) [presiona ENTER para usar hoy]: ")
    if not fecha:
        fecha = str(date.today())

    try:
        og = float(input("🔬 Densidad inicial (OG): "))
        fg = float(input("🧪 Densidad final (FG): "))

        # Conversión si el usuario ingresa por error 1040 en vez de 1.040
        if og > 2:
            og /= 1000
        if fg > 2:
            fg /= 1000

        litros = float(input("🍾 Litros embotellados: "))

        lote = crear_lote(receta, fecha, og, fg, litros)
        print("\n✅ Lote creado exitosamente")
        print(f"Nombre: {receta.nombre}")
        print(f"ABV: {lote.calcular_abv()}%")
        print(f"Costo total: {receta.calcular_costo_total():,.2f}")
        print(f"Costo por litro: {receta.calcular_costo_por_litro():,.2f}")

    except ValueError:
        print("❌ Entrada inválida. Verifica que las densidades y litros sean números.")

def main():
    inventario = cargar_ingredientes()
    while True:
        print("\n=== MENÚ CERVECERO ===")
        print("1. Ver ingredientes")
        print("2. Crear receta nueva")
        print("3. Salir")
        print("4. Ver resumen de lotes")
        print("5. Ver estadísticas generales")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            mostrar_ingredientes(inventario)
        elif opcion == "2":
            receta = crear_receta_desde_consola(inventario)
            crear_lote_interactivo(receta)
        elif opcion == "3":
            print("👋 ¡Hasta la próxima cocinada!")
            break
        elif opcion == "4":
            mostrar_resumen_lotes()
        elif opcion == "5":
            obtener_estadisticas_lotes()
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()
