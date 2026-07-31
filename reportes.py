from datetime import date, datetime

from base_datos import conectar, crear_tabla_reportes


def construir_texto_reporte_entre_compras(compra_uno, compra_dos):
    id_uno, fecha_uno, hora_uno, monto_uno, unidades_uno, articulos_uno = compra_uno
    id_dos, fecha_dos, hora_dos, monto_dos, unidades_dos, articulos_dos = compra_dos
    lineas = []
    lineas.append("=============== REPORTE ENTRE COMPRAS ===============")
    for compra_id, fecha, hora, monto, unidades, articulos in (compra_uno, compra_dos):
        if hora:
            lineas.append(
                f"Compra {compra_id} - {fecha} {hora} - "
                f"${monto:.2f} en {unidades} unidades"
            )
        else:
            lineas.append(
                f"Compra {compra_id} - {fecha} - "
                f"${monto:.2f} en {unidades} unidades"
            )
        lineas.append(f"{'#':>3} {'Producto':<25} {'Cantidad':>8} {'Precio':>10}")
        lineas.append("-" * 50)
        for id_articulo, nombre, cantidad, precio in articulos:
            lineas.append(
                f"{id_articulo:>3} {nombre:<25} {cantidad:>8} {precio:>10.2f}"
            )
        lineas.append("-" * 50)

    productos_uno = {
        nombre: (cantidad, precio) for _, nombre, cantidad, precio in articulos_uno
    }
    productos_dos = {
        nombre: (cantidad, precio) for _, nombre, cantidad, precio in articulos_dos
    }
    comunes = sorted(set(productos_uno) & set(productos_dos))
    solo_uno = sorted(set(productos_uno) - set(productos_dos))
    solo_dos = sorted(set(productos_dos) - set(productos_uno))

    if comunes:
        lineas.append("PRODUCTOS EN AMBAS COMPRAS:")
        for nombre in comunes:
            cantidad_uno, precio_uno = productos_uno[nombre]
            cantidad_dos, precio_dos = productos_dos[nombre]
            subtotal_uno = cantidad_uno * precio_uno
            subtotal_dos = cantidad_dos * precio_dos
            lineas.append(
                f"  {nombre:<25} Compra {id_uno}: x{cantidad_uno} "
                f"(${subtotal_uno:.2f})"
            )
            lineas.append(
                f"  {'':<25} Compra {id_dos}: x{cantidad_dos} "
                f"(${subtotal_dos:.2f})"
            )
            if precio_uno != precio_dos:
                lineas.append(
                    f"  {'':<25} Precio distinto: ${precio_uno:.2f} "
                    f"vs ${precio_dos:.2f}"
                )
            if subtotal_dos > subtotal_uno:
                lineas.append(
                    f"  {'':<25} La compra {id_dos} supero por "
                    f"${subtotal_dos - subtotal_uno:.2f}"
                )
            elif subtotal_uno > subtotal_dos:
                lineas.append(
                    f"  {'':<25} La compra {id_uno} supero por "
                    f"${subtotal_uno - subtotal_dos:.2f}"
                )
            else:
                lineas.append(f"  {'':<25} Sin diferencia en el subtotal")
        lineas.append("")
    if solo_uno:
        lineas.append(f"SOLO EN LA COMPRA {id_uno}:")
        for nombre in solo_uno:
            cantidad, precio = productos_uno[nombre]
            lineas.append(f"  {nombre:<25} x{cantidad} (${cantidad * precio:.2f})")
        lineas.append("")
    if solo_dos:
        lineas.append(f"SOLO EN LA COMPRA {id_dos}:")
        for nombre in solo_dos:
            cantidad, precio = productos_dos[nombre]
            lineas.append(f"  {nombre:<25} x{cantidad} (${cantidad * precio:.2f})")
        lineas.append("")

    diferencia = monto_dos - monto_uno
    porcentaje = (diferencia / monto_uno * 100) if monto_uno > 0 else 0.0
    lineas.append("-" * 50)
    lineas.append(f"DIFERENCIA: ${diferencia:.2f}")
    lineas.append(f"PORCENTAJE: {porcentaje:.2f}%")
    if diferencia > 0:
        lineas.append(f"La compra {id_dos} supero a la compra {id_uno}")
    elif diferencia < 0:
        lineas.append(f"La compra {id_uno} supero a la compra {id_dos}")
    else:
        lineas.append("No hubo diferencia entre las compras")
    return "\n".join(lineas)


def mostrar_reporte_entre_compras(compra_uno, compra_dos):
    texto = construir_texto_reporte_entre_compras(compra_uno, compra_dos)
    print()
    for linea in texto.splitlines():
        print(linea)
    return texto


def guardar_reporte_entre_compras_txt(compra_uno, compra_dos, texto):
    nombre_archivo = f"reporte_entre_compras_{compra_uno[0]}_{compra_dos[0]}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(texto + "\n")
    return nombre_archivo


def generar_texto_compra(compra_id, fecha, hora, total, unidades, articulos):
    lineas = []
    lineas.append(f"=============== COMPRA {compra_id} ===============")
    if hora:
        lineas.append(f"Fecha: {fecha} {hora}")
    else:
        lineas.append(f"Fecha: {fecha}")
    lineas.append(f"{'#':>3} {'Producto':<25} {'Cantidad':>8} {'Precio':>10}")
    lineas.append("-" * 50)
    for id_articulo, producto, cantidad, precio in articulos:
        lineas.append(
            f"{id_articulo:>3} {producto:<25} {cantidad:>8} {precio:>10.2f}"
        )
    lineas.append("-" * 50)
    lineas.append(f"TOTAL: ${total:.2f}")
    lineas.append(f"UNIDADES: {unidades}")
    return "\n".join(lineas)


def guardar_compra_txt(compra_id, fecha, hora, total, unidades, articulos):
    contenido = generar_texto_compra(
        compra_id, fecha, hora, total, unidades, articulos
    )
    nombre_archivo = f"compra_{compra_id}_{fecha}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contenido + "\n")
    return nombre_archivo


def guardar_reporte_entre_compras(compra_uno, compra_dos, contenido):
    conexion = conectar()
    crear_tabla_reportes(conexion)
    diferencia = compra_dos[3] - compra_uno[3]
    conexion.execute(
        "INSERT INTO reportes_guardados "
        "(fecha_generacion, compra_uno, compra_dos, diferencia, contenido) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            datetime.now().isoformat(timespec="minutes"),
            compra_uno[0],
            compra_dos[0],
            diferencia,
            contenido,
        ),
    )
    conexion.commit()
    conexion.close()


def listar_reportes_guardados():
    conexion = conectar()
    crear_tabla_reportes(conexion)
    filas = conexion.execute(
        "SELECT id, fecha_generacion, compra_uno, compra_dos, diferencia "
        "FROM reportes_guardados ORDER BY id DESC"
    ).fetchall()
    conexion.close()
    return filas


def obtener_reporte_guardado(id_reporte):
    conexion = conectar()
    fila = conexion.execute(
        "SELECT contenido FROM reportes_guardados WHERE id = ?", (id_reporte,)
    ).fetchone()
    conexion.close()
    if not fila:
        return None
    return fila[0]


def generar_texto_inventario(productos):
    if not productos:
        return ""
    lineas = []
    lineas.append("=============== INVENTARIO ===============")
    lineas.append(f"{'Producto':<25} {'Cantidad':>9} {'Precio':>10}")
    lineas.append("-" * 48)
    for producto, cantidad, precio in productos:
        lineas.append(f"{producto:<25} {cantidad:>9} {precio:>10.2f}")
    lineas.append("-" * 48)
    return "\n".join(lineas)


def guardar_inventario_txt(productos):
    contenido = generar_texto_inventario(productos)
    if not contenido:
        return None
    nombre_archivo = f"inventario_{date.today().isoformat()}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contenido + "\n")
    return nombre_archivo
