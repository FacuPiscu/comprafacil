import analisis
import base_datos
import compras
import reportes


def mostrar_menu():
    print("\n============ COMPRA FACIL ============")
    print("1. Registrar compra")
    print("2. Ver compras del dia")
    print("3. Ver lista de compras")
    print("4. Reporte por rango de fechas")
    print("5. Comparar compras")
    print("6. Ver reportes guardados")
    print("7. Eliminar articulo")
    print("8. Salir")
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


def ver_lista_compras():
    print("\n--- Lista de compras ---")
    compras_registradas = compras.listar_compras()
    if not compras_registradas:
        print("No hay compras registradas.")
        return
    print(f"{'#':>3} {'Fecha':<12} {'Total':>12} {'Unidades':>9}")
    print("-" * 40)
    for i, (compra_id, fecha, total, unidades) in enumerate(
        compras_registradas, 1
    ):
        print(f"{i:>3} {fecha:<12} {total:>12.2f} {unidades:>9}")
    opcion = input(
        "Seleccione una compra para ver sus articulos (Enter para volver): "
    ).strip()
    if not opcion:
        return
    try:
        indice = int(opcion)
    except ValueError:
        print("Opcion invalida.")
        return
    if indice < 1 or indice > len(compras_registradas):
        print("Opcion invalida.")
        return
    compra_id = compras_registradas[indice - 1][0]
    articulos = compras.listar_articulos(compra_id)
    print(f"\n--- Articulos de la compra {compra_id} ---")
    print(f"{'#':>3} {'Producto':<25} {'Cantidad':>8} {'Precio':>10}")
    print("-" * 50)
    for id_articulo, producto, cantidad, precio in articulos:
        print(f"{id_articulo:>3} {producto:<25} {cantidad:>8} {precio:>10.2f}")


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


def eliminar_articulo():
    print("\n--- Eliminar articulo ---")
    compras_registradas = compras.listar_compras()
    if not compras_registradas:
        print("No hay compras registradas.")
        return
    print(f"{'#':>3} {'Fecha':<12} {'Total':>12} {'Unidades':>9}")
    print("-" * 40)
    for i, (compra_id, fecha, total, unidades) in enumerate(
        compras_registradas, 1
    ):
        print(f"{i:>3} {fecha:<12} {total:>12.2f} {unidades:>9}")
    try:
        opcion = int(input("Seleccione la compra del articulo: "))
    except ValueError:
        print("Opcion invalida.")
        return
    if opcion < 1 or opcion > len(compras_registradas):
        print("Opcion invalida.")
        return
    compra_id = compras_registradas[opcion - 1][0]
    articulos = compras.listar_articulos(compra_id)
    if not articulos:
        print("La compra no tiene articulos.")
        return
    print(f"\n--- Articulos de la compra {compra_id} ---")
    print(f"{'#':>3} {'Producto':<25} {'Cantidad':>8} {'Precio':>10}")
    print("-" * 50)
    for id_articulo, producto, cantidad, precio in articulos:
        print(f"{id_articulo:>3} {producto:<25} {cantidad:>8} {precio:>10.2f}")
    try:
        id_articulo = int(input("Id del articulo a eliminar: "))
    except ValueError:
        print("Id invalido.")
        return
    ids = [articulo[0] for articulo in articulos]
    if id_articulo not in ids:
        print("El id no pertenece a la compra seleccionada.")
        return
    confirmacion = input(
        f"Confirmar eliminacion del articulo {id_articulo}? (s/n): "
    ).strip().lower()
    if confirmacion != "s":
        print("Eliminacion cancelada.")
        return
    compras.eliminar_articulo(id_articulo)
    print(f"Articulo {id_articulo} eliminado.")


def main():
    base_datos.crear_tablas()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "1":
            registrar_compra()
        elif opcion == "2":
            ver_compras_del_dia()
        elif opcion == "3":
            ver_lista_compras()
        elif opcion == "4":
            reporte_rango()
        elif opcion == "5":
            comparar_compras()
        elif opcion == "6":
            ver_reportes_guardados()
        elif opcion == "7":
            eliminar_articulo()
        elif opcion == "8":
            print("Hasta luego.")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()
