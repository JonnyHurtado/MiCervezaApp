from app.modelo import Receta, Lote, Ingrediente
from app import datos
from datetime import date

def crear_receta_desde_consola(inventario):
    nombre = input("\n🧪 Nombre de la nueva receta: ")
    litros = float(input("🎯 Litros objetivo: "))
    receta = Receta(nombre, litros)

    while True:
        print("\nIngredientes disponibles:")
        for i, ing in enumerate(inventario, start=1):
            print(f"{i}. {ing.nombre} ({ing.tipo}) - Stock: {ing.stock} {ing.unidad}")

        seleccion = input("Selecciona el número del ingrediente a agregar (o 'fin' para terminar): ")
        if seleccion.lower() == "fin":
            break

        try:
            idx = int(seleccion) - 1
            if 0 <= idx < len(inventario):
                ingrediente = inventario[idx]
                cantidad = float(input(f"Cantidad de {ingrediente.unidad} a usar: "))
                receta.agregar_ingrediente(ingrediente, cantidad)
                ingrediente.stock -= cantidad
            else:
                print("❌ Selección fuera de rango.")
        except ValueError:
            print("❌ Entrada inválida.")

    print("\n✅ Receta creada con éxito:")
    for i in receta.ingredientes:
        print(f"  - {i.ingrediente.nombre} ({i.ingrediente.tipo}) - {i.cantidad} {i.ingrediente.unidad}")

    return receta

def crear_lote_interactivo(receta):
    fecha = input("\n📅 Fecha del lote (YYYY-MM-DD) [presiona ENTER para usar hoy]: ")
    if not fecha:
        fecha = str(date.today())

    try:
        og = float(input("🔬 Densidad inicial (OG): "))
        fg = float(input("🧪 Densidad final (FG): "))

        if og > 2: og /= 1000
        if fg > 2: fg /= 1000

        litros = float(input("🍾 Litros embotellados: "))
        lote = Lote(receta, fecha, og, fg, litros)
        datos.guardar_lote(lote)

        print("\n✅ Lote creado exitosamente")
        print(f"Nombre: {receta.nombre}")
        print(f"ABV: {lote.calcular_abv():.2f}%")
        print(f"Costo total: {receta.calcular_costo_total():,.2f}")
        print(f"Costo por litro: {receta.calcular_costo_por_litro():,.2f}")

    except ValueError:
        print("❌ Entrada inválida.")

def mostrar_resumen_lotes():
    lotes = datos.cargar_lotes()
    if not lotes:
        print("\n📭 No hay lotes registrados todavía.")
        return

    print("\n📦 RESUMEN DE LOTES PRODUCIDOS")
    print("-" * 40)
    for lote in lotes:
        print(f"Nombre receta: {lote.receta.nombre}")
        print(f"Fecha cocción: {lote.fecha}")
        print(f"Litros embotellados: {lote.litros_embotellados}")
        print(f"ABV (%): {lote.calcular_abv():.2f}")
        print(f"Costo total receta: {lote.receta.calcular_costo_total():,.2f}")
        print(f"Costo por litro: {lote.receta.calcular_costo_por_litro():,.2f}")
        print("-" * 40)

def mostrar_estadisticas_generales():
    from app.estadisticas import obtener_estadisticas_lotes
    estadisticas = obtener_estadisticas_lotes()
    if not estadisticas:
        print("\n📭 No hay datos suficientes para mostrar estadísticas.")
        return

    print("\n📊 ESTADÍSTICAS GENERALES")
    print(f"Total de lotes: {estadisticas['total_lotes']}")
    print(f"Promedio de ABV: {estadisticas['promedio_abv']:.2f}%")
    print(f"Promedio de costo por litro: {estadisticas['promedio_costo_litro']:,.2f}")
    print(f"Total litros embotellados: {estadisticas['total_litros']}")

def sincronizar_con_github():
    import os
    import subprocess

    print("\n🔄 Sincronizando con GitHub...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Cambios sincronizados desde app cervecera"], check=True)
        subprocess.run(["git", "pull", "--rebase"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Cambios sincronizados con éxito.")
    except subprocess.CalledProcessError:
        print("❌ Error al sincronizar con GitHub. Verifica tu conexión y configuración.")

def agregar_ingrediente_interactivo(inventario):
    print("\n🆕 Agregar nuevo ingrediente al inventario")

    # Mostrar ingredientes existentes para evitar duplicados
    if inventario:
        print("\n📦 Ingredientes existentes:")
        for i, ing in enumerate(inventario, start=1):
            print(f"{i}. {ing.nombre} ({ing.tipo}) - {ing.unidad}, Stock: {ing.stock}")
    else:
        print("⚠️ Aún no hay ingredientes en el inventario.")

    respuesta = input("\n¿Quieres agregar stock a un ingrediente existente? (s/n): ").strip().lower()

    if respuesta == "s":
        try:
            seleccion = int(input("Selecciona el número del ingrediente: "))
            if 1 <= seleccion <= len(inventario):
                ing = inventario[seleccion - 1]
                cantidad = float(input(f"Cantidad a sumar a '{ing.nombre}' ({ing.unidad}): "))
                ing.stock += cantidad
                datos.guardar_ingredientes(inventario)
                print(f"✅ Nuevo stock de {ing.nombre}: {ing.stock}")
                return
            else:
                print("❌ Número fuera de rango.")
                return
        except ValueError:
            print("❌ Entrada inválida.")
            return

    # Si desea agregar uno nuevo
    nombre = input("Nombre del nuevo ingrediente: ").strip()
    
    tipos_validos = ["Malta", "Lupulo", "Levadura", "Agua", "ManoObra", "Packing", "Branding", "Energía", "Otros"]
    print("\nTipos disponibles:")
    for i, t in enumerate(tipos_validos, start=1):
        print(f"{i}. {t}")
    
    try:
        tipo_index = int(input("Selecciona el número del tipo: "))
        tipo = tipos_validos[tipo_index - 1]
        unidad = input("Unidad de medida (g, kg, l, unidad, etc): ")
        cantidad = float(input(f"Cantidad inicial ({unidad}): "))
        precio = float(input(f"Precio por {unidad}: "))

        # Validar si ya existe un ingrediente con mismo nombre y unidad
        for ing in inventario:
            if ing.nombre.lower() == nombre.lower() and ing.unidad == unidad:
                print("⚠️ Ya existe un ingrediente con ese nombre y unidad.")
                return

        nuevo = Ingrediente(nombre, tipo, unidad, cantidad, precio)
        inventario.append(nuevo)
        datos.guardar_ingredientes(inventario)
        print("✅ Ingrediente agregado exitosamente.")

    except (ValueError, IndexError):
        print("❌ Entrada inválida.")


