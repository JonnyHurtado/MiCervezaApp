from app.datos_lotes import cargar_lotes_csv

def obtener_estadisticas_lotes():
    lotes = cargar_lotes_csv()
    if not lotes:
        print("\n📭 No hay lotes registrados.")
        return

    total_lotes = len(lotes)
    total_litros = sum(l.litros_embotellados for l in lotes)
    total_costo = sum(l.receta.calcular_costo_total() for l in lotes)
    promedio_abv = sum(l.calcular_abv() for l in lotes) / total_lotes

    print("\n📊 Estadísticas generales:")
    print(f"🔢 Total de lotes: {total_lotes}")
    print(f"🍾 Total litros producidos: {total_litros}")
    print(f"💰 Total invertido: {total_costo:,.2f}")
    print(f"🍺 Promedio ABV: {promedio_abv:.2f}%")
