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
        print("✅ Todo está sincronizado. No hay cambios pendientes.")

def agregar_ingrediente_interactivo(inventario):
    print("\n🆕 Agregar nuevo ingrediente al inventario")

    # Verificar si hay ingredientes existentes
    if inventario:
        print("\n📋 Ingredientes existentes:")
        for idx, ing in enumerate(inventario, 1):
            print(f"{idx}. {ing.nombre} ({ing.tipo}) - {ing.stock} {ing.unidad} - ${ing.precio_unitario} por {ing.unidad}")
        
        seleccion = input("\n¿Deseas agregar stock a uno existente? (s/n): ").lower()

        if seleccion == "s":
            try:
                num = int(input("Selecciona el número del ingrediente: "))
                if 1 <= num <= len(inventario):
                    ing = inventario[num - 1]
                    cantidad = float(input(f"Ingresaste cantidad adicional en {ing.unidad}: "))
                    nuevo_precio = float(input(f"¿Cuál fue el precio por {ing.unidad} esta vez?: "))

                    # Recalcular precio promedio ponderado
                    precio_promedio = (
                        (ing.stock * ing.precio_unitario) + (cantidad * nuevo_precio)
                    ) / (ing.stock + cantidad)

                    ing.precio_unitario = round(precio_promedio, 2)
                    ing.stock += cantidad

                    datos.guardar_ingredientes(inventario)
                    print(f"\n✅ Stock actualizado: {ing.stock} {ing.unidad}")
                    print(f"💰 Nuevo precio promedio por {ing.unidad}: {ing.precio_unitario}")
                    return  # salir después de actualizar
                else:
                    print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Entrada inválida. Intenta nuevamente.")

    # Si no quiere usar ingrediente existente o no hay ingredientes
    nombre = input("Nombre del ingrediente: ").strip()
    tipo = input("Tipo (Malta, Lupulo, Levadura, Agua, ManoObra, Packing, etc): ").strip()
    unidad = input("Unidad de medida (g, kg, l, unidad, etc): ").strip()
    cantidad = float(input(f"Cantidad inicial ({unidad}): "))
    precio = float(input(f"Precio por {unidad}: "))

    nuevo = registrar_ingrediente(nombre, tipo, unidad, cantidad, precio)
    inventario.append(nuevo)

    datos.guardar_ingredientes(inventario)
    print(f"\n✅ Ingrediente '{nombre}' agregado con {cantidad} {unidad} a ${precio} por {unidad}")
