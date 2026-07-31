from datetime import datetime

from base_datos import conectar, crear_tabla_reportes


def obtener_compras_rango(fecha_inicio, fecha_fin):
    conexion = conectar()
    filas = conexion.execute(
        "SELECT producto, cantidad, precio, fecha FROM compras "
        "WHERE fecha BETWEEN ? AND ? ORDER BY fecha, id",
        (fecha_inicio, fecha_fin),
    ).fetchall()
    conexion.close()
    return filas


def mostrar_reporte(filas):
    if not filas:
        print("\nNo hay compras en el rango indicado.")
        return

    total = 0.0
    print("\n=============== REPORTE DE COMPRAS ===============")
    print(f"{'Producto':<25} {'Fecha':<12} {'Cantidad':>8} {'Precio':>10} {'Total':>12}")
    print("-" * 70)
    for producto, cantidad, precio, fecha in filas:
        subtotal = cantidad * precio
        total += subtotal
        print(
            f"{producto:<25} {fecha:<12} {cantidad:>8} {precio:>10.2f} {subtotal:>12.2f}"
        )
    print("-" * 70)
    print(f"TOTAL COMPRADO: ${total:.2f}")
    print(f"CANTIDAD DE COMPRAS: {len(filas)}")
    return total, len(filas)


def guardar_reporte(fecha_inicio, fecha_fin, total, cantidad_compras):
    conexion = conectar()
    crear_tabla_reportes(conexion)
    conexion.execute(
        "INSERT INTO reportes_guardados "
        "(fecha_generacion, fecha_inicio, fecha_fin, total, cantidad_compras) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            datetime.now().isoformat(timespec="minutes"),
            fecha_inicio,
            fecha_fin,
            total,
            cantidad_compras,
        ),
    )
    conexion.commit()
    conexion.close()


def listar_reportes_guardados():
    conexion = conectar()
    crear_tabla_reportes(conexion)
    filas = conexion.execute(
        "SELECT id, fecha_generacion, fecha_inicio, fecha_fin, total, cantidad_compras "
        "FROM reportes_guardados ORDER BY id DESC"
    ).fetchall()
    conexion.close()
    return filas
