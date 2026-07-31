import base_datos
import compras
import reportes


def pedir_entrada(mensaje):
    try:
        return input(mensaje)
    except EOFError:
        print("\nEntrada no disponible. Saliendo.")
        raise SystemExit(0)


def mostrar_menu():
    print("\n============ COMPRA FACIL ============")
    print("1. Registrar compra")
    print("2. Ver compras del dia")
    print("3. Ver lista de compras")
    print("4. Generador de reporte entre compras")
    print("5. Consultar stock")
    print("6. Eliminar articulo")
    print("7. Salir")
    print("=====================================")


def registrar_compra():
    print("\n--- Registrar compra ---")
    articulos = []
    while True:
        producto = pedir_entrada(
            "Nombre del producto (Enter para terminar): "
        ).strip()
        if not producto:
            break
        try:
            cantidad = int(pedir_entrada("Cantidad: "))
            precio = float(pedir_entrada("Precio por unidad: "))
        except ValueError:
            print("Cantidad y precio deben ser numeros.")
            continue
        if cantidad <= 0 or precio < 0:
            print("Valores invalidos.")
            continue
        indice_existente = None
        for i, (nombre_existente, _, _) in enumerate(articulos):
            if nombre_existente.lower() == producto.lower():
                indice_existente = i
                break
        if indice_existente is not None:
            confirmar = pedir_entrada(
                f"{producto} ya existe en la lista. Queres agregarlo igual? (s/n): "
            ).strip().lower()
            if confirmar != "s":
                print("No se agrego el articulo.")
                continue
            nombre_existente, cantidad_existente, _ = articulos[indice_existente]
            articulos[indice_existente] = (
                nombre_existente,
                cantidad_existente + cantidad,
                precio,
            )
            print(
                f"Articulo actualizado: {nombre_existente} "
                f"x{cantidad_existente + cantidad} a ${precio:.2f}"
            )
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
    for compra_id, monto, hora, producto, cantidad, precio in filas:
        if compra_id != compra_actual:
            if compra_actual is not None:
                print("-" * 45)
            compra_actual = compra_id
            if hora:
                print(f"Compra {compra_id} a las {hora} - ${monto:.2f}:")
            else:
                print(f"Compra {compra_id} - ${monto:.2f}:")
        print(f"  {producto:<25} {cantidad:>8} {precio:>10.2f}")
    print("-" * 45)


def ver_lista_compras():
    print("\n--- Lista de compras ---")
    compras_registradas = compras.listar_compras()
    if not compras_registradas:
        print("No hay compras registradas.")
        return
    print(f"{'#':>3} {'Fecha':<12} {'Hora':<6} {'Total':>12} {'Unidades':>9}")
    print("-" * 48)
    for i, (compra_id, fecha, hora, total, unidades) in enumerate(
        compras_registradas, 1
    ):
        print(f"{i:>3} {fecha:<12} {hora:<6} {total:>12.2f} {unidades:>9}")
    opcion = pedir_entrada(
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
    descargar = pedir_entrada(
        "Descargar esta compra en txt? (s/n): "
    ).strip().lower()
    if descargar == "s":
        fecha, hora, total, unidades = compras_registradas[indice - 1][1:]
        nombre_archivo = reportes.guardar_compra_txt(
            compra_id, fecha, hora, total, unidades, articulos
        )
        print(f"Compra guardada en {nombre_archivo}.")


def _obtener_datos_compra(compra_id, compras_registradas):
    for compra in compras_registradas:
        if compra[0] == compra_id:
            _, fecha, hora, monto, unidades = compra
            articulos = compras.listar_articulos(compra_id)
            return compra_id, fecha, hora, monto, unidades, articulos
    return None


def generar_reporte_entre_compras():
    print("\n--- Generar reporte entre compras ---")
    compras_registradas = compras.listar_compras()
    if len(compras_registradas) < 2:
        print("Se necesitan al menos dos compras registradas.")
        return
    print(f"{'#':>3} {'Fecha':<12} {'Hora':<6} {'Total':>12} {'Unidades':>9}")
    print("-" * 48)
    for i, (compra_id, fecha, hora, total, unidades) in enumerate(
        compras_registradas, 1
    ):
        print(f"{i:>3} {fecha:<12} {hora:<6} {total:>12.2f} {unidades:>9}")
    try:
        opcion_uno = int(pedir_entrada("Seleccione la primera compra: "))
        opcion_dos = int(pedir_entrada("Seleccione la segunda compra: "))
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
    compra_uno = _obtener_datos_compra(
        compras_registradas[opcion_uno - 1][0], compras_registradas
    )
    compra_dos = _obtener_datos_compra(
        compras_registradas[opcion_dos - 1][0], compras_registradas
    )
    texto = reportes.mostrar_reporte_entre_compras(compra_uno, compra_dos)
    descargar = pedir_entrada(
        "Descargar el reporte en txt? (s/n): "
    ).strip().lower()
    if descargar == "s":
        nombre_archivo = reportes.guardar_reporte_entre_compras_txt(
            compra_uno, compra_dos, texto
        )
        print(f"Reporte guardado en {nombre_archivo}.")
    guardar = pedir_entrada(
        "Guardar el reporte? (s/n): "
    ).strip().lower()
    if guardar == "s":
        reportes.guardar_reporte_entre_compras(compra_uno, compra_dos, texto)
        print("Reporte guardado en la lista de reportes.")


def reporte_entre_compras():
    while True:
        print("\n--- Generador de reporte entre compras ---")
        print("1. Generar reporte entre compras")
        print("2. Ver reportes guardados")
        print("0. Volver")
        opcion = pedir_entrada("Seleccione una opcion: ").strip()
        if opcion == "1":
            generar_reporte_entre_compras()
        elif opcion == "2":
            ver_reportes_guardados()
        elif opcion == "0":
            break
        else:
            print("Opcion invalida.")


def ver_reportes_guardados():
    print("\n--- Reportes guardados ---")
    filas = reportes.listar_reportes_guardados()
    if not filas:
        print("No hay reportes guardados.")
        return
    print(
        f"{'#':>3} {'Generado':<18} {'Compra 1':>8} {'Compra 2':>8} "
        f"{'Diferencia':>14}"
    )
    print("-" * 60)
    for id_reporte, fecha_generacion, compra_uno, compra_dos, diferencia in filas:
        print(
            f"{id_reporte:>3} {fecha_generacion:<18} {compra_uno:>8} "
            f"{compra_dos:>8} {diferencia:>14.2f}"
        )
    opcion = pedir_entrada(
        "Seleccione un reporte para ver su contenido (Enter para volver): "
    ).strip()
    if not opcion:
        return
    try:
        id_reporte = int(opcion)
    except ValueError:
        print("Opcion invalida.")
        return
    contenido = reportes.obtener_reporte_guardado(id_reporte)
    if contenido is None:
        print("El reporte no existe.")
        return
    print()
    print(contenido)


def consultar_stock():
    print("\n--- Consultar stock ---")
    nombre = pedir_entrada("Producto a buscar (Enter para ver todos): ").strip()
    productos = compras.listar_productos(nombre)
    if not productos:
        print("No hay productos en el inventario.")
        return
    print(f"{'Producto':<25} {'Cantidad':>9} {'Precio':>10}")
    print("-" * 48)
    for producto, cantidad, precio in productos:
        print(f"{producto:<25} {cantidad:>9} {precio:>10.2f}")
    seleccion = pedir_entrada(
        "Nombre del producto para ver su detalle (Enter para volver): "
    ).strip()
    if seleccion:
        nombres = [producto[0] for producto in productos]
        if seleccion not in nombres:
            print("Producto no encontrado.")
            return
        detalle = compras.listar_detalle_producto(seleccion)
        print(f"\n--- Detalle de {seleccion} ---")
        print(f"{'Fecha':<12} {'Hora':<6} {'Cantidad':>9} {'Precio':>10}")
        print("-" * 42)
        for fecha, hora, cantidad, precio in detalle:
            print(f"{fecha:<12} {hora:<6} {cantidad:>9} {precio:>10.2f}")
        total_unidades = sum(cantidad for _, _, cantidad, _ in detalle)
        total_monto = sum(cantidad * precio for _, _, cantidad, precio in detalle)
        print("-" * 42)
        print(f"{'TOTAL:':<18} {total_unidades:>9} {total_monto:>10.2f}")
        return
    descargar = pedir_entrada(
        "Descargar el inventario en txt? (s/n): "
    ).strip().lower()
    if descargar == "s":
        nombre_archivo = reportes.guardar_inventario_txt(productos)
        print(f"Inventario guardado en {nombre_archivo}.")


def eliminar_articulo():
    print("\n--- Eliminar articulo ---")
    compras_registradas = compras.listar_compras()
    if not compras_registradas:
        print("No hay compras registradas.")
        return
    print(f"{'#':>3} {'Fecha':<12} {'Hora':<6} {'Total':>12} {'Unidades':>9}")
    print("-" * 48)
    for i, (compra_id, fecha, hora, total, unidades) in enumerate(
        compras_registradas, 1
    ):
        print(f"{i:>3} {fecha:<12} {hora:<6} {total:>12.2f} {unidades:>9}")
    try:
        opcion = int(pedir_entrada("Seleccione la compra del articulo: "))
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
        id_articulo = int(pedir_entrada("Id del articulo a eliminar: "))
    except ValueError:
        print("Id invalido.")
        return
    ids = [articulo[0] for articulo in articulos]
    if id_articulo not in ids:
        print("El id no pertenece a la compra seleccionada.")
        return
    confirmacion = pedir_entrada(
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
        opcion = pedir_entrada("Seleccione una opcion: ").strip()
        match opcion:
            case "1":
                registrar_compra()
            case "2":
                ver_compras_del_dia()
            case "3":
                ver_lista_compras()
            case "4":
                reporte_entre_compras()
            case "5":
                consultar_stock()
            case "6":
                eliminar_articulo()
            case "7":
                print("Hasta luego.")
                break
            case _:
                print("Opcion invalida.")


if __name__ == "__main__":
    main()
