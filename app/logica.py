from app.modelo import Ingrediente, Receta, Lote
from app import datos
from app.datos_lotes import guardar_lote_csv
from app.datos import guardar_receta_en_csv
from datetime import date

inventario = datos.cargar_ingredientes()
recetas = []
lotes = []

def registrar_ingrediente(nombre, tipo, unidad, cantidad, precio_unitario):
    ing = Ingrediente(nombre, tipo, unidad, cantidad, precio_unitario)
    inventario.append(ing)
    datos.guardar_ingredientes(inventario)
    return ing

def buscar_ingrediente(nombre):
    for i in inventario:
        if i.nombre == nombre:
            return i
    raise ValueError(f"Ingrediente '{nombre}' no encontrado")

def crear_receta(nombre, litros_objetivo, ingredientes_usados):
    receta = Receta(nombre, litros_objetivo)
    for nombre_ing, cantidad in ingredientes_usados:
        ing = buscar_ingrediente(nombre_ing)
        receta.agregar_ingrediente(ing, cantidad)
    recetas.append(receta)
    return receta

def crear_lote(receta, fecha, densidad_inicial, densidad_final, litros_embotellados):
    lote = Lote(receta, fecha, densidad_inicial, densidad_final, litros_embotellados)
    lotes.append(lote)
    guardar_lote_csv(lote)  # <-- NUEVA línea
    return lote

def mostrar_resumen_lotes():
    from app.datos_lotes import cargar_lotes_csv
    lotes_guardados = cargar_lotes_csv()

    if not lotes_guardados:
        print("\n📭 No hay lotes registrados todavía.")
        return

    print("\n📦 RESUMEN DE LOTES PRODUCIDOS")
    print("-" * 40)
    for lote in lotes_guardados:
        print(f"Nombre receta: {lote.receta.nombre}")
        print(f"Fecha cocción: {lote.fecha}")
        print(f"Litros embotellados: {lote.litros_embotellados}")
        print(f"ABV (%): {lote.calcular_abv()}")
        print(f"Costo total receta: {lote.receta.calcular_costo_total():,.2f}")
        print(f"Costo por litro: {lote.receta.calcular_costo_por_litro():,.2f}")
        print("-" * 40)

def crear_receta_desde_consola(inventario):
    nombre = input("Nombre de la receta: ")
    litros = float(input("Litros objetivo: "))
    receta = Receta(nombre, litros)

    while True:
        print("\nIngredientes disponibles:")
        for idx, ing in enumerate(inventario):
            print(f"{idx + 1}. {ing.nombre} ({ing.tipo}) - Stock: {ing.stock} {ing.unidad}")

        opcion = input("Selecciona el número del ingrediente a agregar (o 'fin' para terminar): ")

        if opcion.lower() == "fin":
            break

        try:
            idx = int(opcion) - 1
            if 0 <= idx < len(inventario):
                cantidad = float(input(f"Cantidad de {inventario[idx].unidad} a usar: "))
                receta.agregar_ingrediente(inventario[idx], cantidad)
            else:
                print("❌ Opción inválida.")
        except ValueError:
            print("❌ Entrada inválida. Intenta de nuevo.")

    print("\n✅ Receta creada con éxito:")
    for ing, cant in receta.ingredientes:
        print(f"  - {ing.nombre} ({ing.tipo}) - {cant} {ing.unidad}")

    guardar_receta_en_csv(receta)  # <--- esta línea guarda en CSV correctamente
    return receta

# Dentro de la función crear_receta_desde_consola
    ...
    print("\n✅ Receta creada con éxito:")
    for ing, cant in receta.ingredientes:
        print(f"  - {ing.nombre} ({ing.tipo}) - {cant}")

    guardar_receta_en_csv(receta)  # <--- esta línea guarda en CSV
    return receta

def crear_lote_interactivo(receta):
    fecha_input = input("📅 Fecha del lote (YYYY-MM-DD) [presiona ENTER para usar hoy]: ")
    if fecha_input.strip() == "":
        fecha = str(date.today())
    else:
        fecha = fecha_input

    # Captura y corrección de densidades
    og_input = input("🔬 Densidad inicial (OG): ")
    fg_input = input("🧪 Densidad final (FG): ")

    try:
        og = float(og_input)
        fg = float(fg_input)

        # Si el usuario puso 1040 en lugar de 1.040, lo corregimos
        if og > 2:
            og /= 1000
        if fg > 2:
            fg /= 1000
    except ValueError:
        print("❌ Densidad no válida. Usa formato decimal (ej: 1.040)")
        return

    litros_embotellados = float(input("🍾 Litros embotellados: "))
    lote = crear_lote(receta, fecha, og, fg, litros_embotellados)

    print("\n✅ Lote creado exitosamente")
    print(f"Nombre: {receta.nombre}")
    print(f"ABV: {lote.calcular_abv()}%")
    print(f"Costo total: {receta.calcular_costo_total():,.2f}")
    print(f"Costo por litro: {receta.calcular_costo_por_litro():,.2f}")

def mostrar_estadisticas_generales():
    from app.datos_lotes import cargar_lotes_csv

    lotes = cargar_lotes_csv()
    if not lotes:
        print("\n📭 No hay lotes registrados para mostrar estadísticas.")
        return

    total_lotes = len(lotes)
    total_litros = sum(l.litros_embotellados for l in lotes)
    promedio_abv = sum(l.calcular_abv() for l in lotes) / total_lotes

    print("\n📊 ESTADÍSTICAS GENERALES")
    print("-" * 40)
    print(f"Total de lotes: {total_lotes}")
    print(f"Litros totales embotellados: {total_litros}")
    print(f"ABV promedio: {promedio_abv:.2f}%")
    print("-" * 40)

import subprocess

def sincronizar_con_github():
    print("\n🔄 Guardando y sincronizando con GitHub...")

    try:
        # Agregar todos los cambios
        subprocess.run(["git", "add", "."], check=True)

        # Confirmar los cambios
        subprocess.run(["git", "commit", "-m", "sync changes"], check=True)

        # Subir los cambios
        subprocess.run(["git", "push"], check=True)

        print("✅ Cambios sincronizados con éxito.")
    except subprocess.CalledProcessError as e:
        print("❌ Ocurrió un error al sincronizar con GitHub.")
        print(e)
