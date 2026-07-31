import analisis
import compras
import reportes


def mostrar_menu():
    print("\n============ COMPRA FACIL ============")
    print("1. Registrar compra")
    print("2. Ver compras del dia")
    print("3. Reporte por rango de fechas")
    print("4. Comparar compras")
    print("5. Ver reportes guardados")
    print("6. Salir")
    print("=====================================")


def registrar_compra():
    print("\n--- Registrar compra ---")
    articulos = []
    while True:
        producto = input(
            "Nombre del producto (Enter para terminar): "
        ).strip()
        if not producto:
            break
        try:
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio por unidad: "))
        except ValueError:
            print("Cantidad y precio deben ser numeros.")
            continue
        if cantidad <= 0 or precio < 0:
            print("Valores invalidos.")
            continue
        articulos.append((producto, cantidad, precio))
        print(f"Articulo agregado: {producto} x{cantidad} a ${precio:.2f}")
    if not articulos:
        print("No se registro ningun articulo.")
        return
    compra_id = compras.registrar_compra(articulos)
    print(f"Compra {compra_id} registrada con {len(articulos)} articulos.")


def ver_compras_del_dia():
    print("\n--- Compras del dia ---")
    filas = compras.listar_compras_del_dia()
    if not filas:
        print("No hay compras registradas hoy.")
        return
    compra_actual = None
    for compra_id, producto, cantidad, precio in filas:
        if compra_id != compra_actual:
            if compra_actual is not None:
                print("-" * 45)
            compra_actual = compra_id
            print(f"Compra {compra_id}:")
        print(f"  {producto:<25} {cantidad:>8} {precio:>10.2f}")
    print("-" * 45)


def reporte_rango():
    print("\n--- Reporte por rango de fechas ---")
    fecha_inicio = input("Fecha inicio (AAAA-MM-DD): ").strip()
    fecha_fin = input("Fecha fin (AAAA-MM-DD): ").strip()
    if fecha_inicio > fecha_fin:
        print("La fecha de inicio no puede ser mayor a la de fin.")
        return
    filas = reportes.obtener_compras_rango(fecha_inicio, fecha_fin)
    resultado = reportes.mostrar_reporte(filas)
    if resultado:
        total, cantidad = resultado
        reportes.guardar_reporte(fecha_inicio, fecha_fin, total, cantidad)
        print("Reporte guardado.")


def ver_reportes_guardados():
    print("\n--- Reportes guardados ---")
    filas = reportes.listar_reportes_guardados()
    if not filas:
        print("No hay reportes guardados.")
        return
    print(f"{'#':>3} {'Generado':<18} {'Desde':<12} {'Hasta':<12} {'Total':>12} {'Compras':>8}")
    print("-" * 70)
    for id_reporte, fecha_generacion, fecha_inicio, fecha_fin, total, cantidad in filas:
        print(
            f"{id_reporte:>3} {fecha_generacion:<18} {fecha_inicio:<12} "
            f"{fecha_fin:<12} {total:>12.2f} {cantidad:>8}"
        )


def comparar_compras():
    print("\n--- Comparar compras ---")
    compras_registradas = compras.listar_compras()
    if len(compras_registradas) < 2:
        print("Se necesitan al menos dos compras registradas.")
        return
    print(f"{'#':>3} {'Fecha':<12} {'Total':>12} {'Unidades':>9}")
    print("-" * 40)
    for i, (compra_id, fecha, total, unidades) in enumerate(
        compras_registradas, 1
    ):
        print(f"{i:>3} {fecha:<12} {total:>12.2f} {unidades:>9}")
    try:
        opcion_uno = int(input("Seleccione la primera compra: "))
        opcion_dos = int(input("Seleccione la segunda compra: "))
    except ValueError:
        print("Opciones invalidas.")
        return
    total_compras = len(compras_registradas)
    if (
        opcion_uno < 1
        or opcion_dos < 1
        or opcion_uno > total_compras
        or opcion_dos > total_compras
    ):
        print("Opciones invalidas.")
        return
    if opcion_uno == opcion_dos:
        print("Debe seleccionar dos compras distintas.")
        return
    compra_uno = compras_registradas[opcion_uno - 1][0]
    compra_dos = compras_registradas[opcion_dos - 1][0]
    analisis.comparar_compras(compra_uno, compra_dos)


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "1":
            registrar_compra()
        elif opcion == "2":
            ver_compras_del_dia()
        elif opcion == "3":
            reporte_rango()
        elif opcion == "4":
            comparar_compras()
        elif opcion == "5":
            ver_reportes_guardados()
        elif opcion == "6":
            print("Hasta luego.")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()
