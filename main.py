from app.modelo import Ingrediente, Receta, Lote
from app.datos import cargar_ingredientes
from app.logica import (
    crear_receta_desde_consola,
    crear_lote_interactivo,
    mostrar_resumen_lotes,
    mostrar_estadisticas_generales,
    sincronizar_con_github,
    agregar_ingrediente_interactivo
)

def mostrar_menu():
    print("\n=== MENÚ CERVECERO ===")
    print("1. Agregar nuevo ingrediente")
    print("2. Ver ingredientes")
    print("3. Crear receta nueva")
    print("4. Ver resumen de lotes")
    print("5. Ver estadísticas generales")
    print("6. Guardar y sincronizar con GitHub")
    print("7. Salir")

def mostrar_ingredientes(inventario):
    print("\n📦 Ingredientes disponibles:")
    if not inventario:
        print("⚠️ No hay ingredientes cargados.")
        return

    for i, ing in enumerate(inventario, start=1):
        print(f"{i}. {ing.nombre} ({ing.tipo}) - {ing.precio_unitario:.2f}/{ing.unidad} - Stock: {ing.stock} {ing.unidad}")

def main():
    inventario = cargar_ingredientes()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_ingrediente_interactivo(inventario)
            input("\nPresiona ENTER para volver al menú...")

        elif opcion == "2":
            mostrar_ingredientes(inventario)
            input("\nPresiona ENTER para volver al menú...")

        elif opcion == "3":
            receta = crear_receta_desde_consola(inventario)
            crear_lote_interactivo(receta)
            input("\nPresiona ENTER para volver al menú...")

        elif opcion == "4":
            mostrar_resumen_lotes()
            input("\nPresiona ENTER para volver al menú...")

        elif opcion == "5":
            mostrar_estadisticas_generales()
            input("\nPresiona ENTER para volver al menú...")

        elif opcion == "6":
            sincronizar_con_github()
            input("\nPresiona ENTER para volver al menú...")

        elif opcion == "7":
            print("👋 ¡Hasta la próxima cocinada!")
            break

        else:
            print("❌ Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
