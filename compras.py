from datetime import date, datetime

from base_datos import conectar, crear_tabla, crear_tabla_productos


def registrar_compra(articulos, fecha=None, hora=None):
    if fecha is None:
        fecha = date.today().isoformat()
    if hora is None:
        hora = datetime.now().strftime("%H:%M")
    monto = sum(cantidad * precio for _, cantidad, precio in articulos)
    conexion = conectar()
    crear_tabla(conexion)
    crear_tabla_productos(conexion)
    cursor = conexion.execute(
        "INSERT INTO compras (monto, fecha, hora) VALUES (?, ?, ?)",
        (monto, fecha, hora),
    )
    compra_id = cursor.lastrowid
    conexion.executemany(
        "INSERT INTO productos (compra_id, nombre, cantidad, precio) "
        "VALUES (?, ?, ?, ?)",
        [
            (compra_id, nombre, cantidad, precio)
            for nombre, cantidad, precio in articulos
        ],
    )
    conexion.commit()
    conexion.close()
    return compra_id


def listar_compras_del_dia(fecha=None):
    if fecha is None:
        fecha = date.today().isoformat()
    conexion = conectar()
    filas = conexion.execute(
        "SELECT c.id, c.monto, c.hora, p.nombre, p.cantidad, p.precio "
        "FROM compras c JOIN productos p ON p.compra_id = c.id "
        "WHERE c.fecha = ? ORDER BY c.id, p.id",
        (fecha,),
    ).fetchall()
    conexion.close()
    return filas


def listar_compras():
    conexion = conectar()
    filas = conexion.execute(
        "SELECT c.id, c.fecha, c.hora, c.monto, "
        "(SELECT SUM(p.cantidad) FROM productos p WHERE p.compra_id = c.id) "
        "FROM compras c ORDER BY c.fecha, c.hora, c.id"
    ).fetchall()
    conexion.close()
    return filas


def listar_articulos(compra_id):
    conexion = conectar()
    filas = conexion.execute(
        "SELECT id, nombre, cantidad, precio FROM productos "
        "WHERE compra_id = ? ORDER BY id",
        (compra_id,),
    ).fetchall()
    conexion.close()
    return filas


def eliminar_articulo(id_articulo):
    conexion = conectar()
    fila = conexion.execute(
        "SELECT compra_id FROM productos WHERE id = ?", (id_articulo,)
    ).fetchone()
    if fila:
        compra_id = fila[0]
        conexion.execute("DELETE FROM productos WHERE id = ?", (id_articulo,))
        monto = conexion.execute(
            "SELECT SUM(cantidad * precio) FROM productos WHERE compra_id = ?",
            (compra_id,),
        ).fetchone()[0]
        if monto is None:
            conexion.execute("DELETE FROM compras WHERE id = ?", (compra_id,))
        else:
            conexion.execute(
                "UPDATE compras SET monto = ? WHERE id = ?", (monto, compra_id)
            )
        conexion.commit()
    conexion.close()


def listar_productos(nombre=None):
    conexion = conectar()
    if nombre:
        filas = conexion.execute(
            "SELECT p.nombre, SUM(p.cantidad), "
            "(SELECT precio FROM productos WHERE nombre = p.nombre "
            "ORDER BY id DESC LIMIT 1) "
            "FROM productos p WHERE p.nombre LIKE ? "
            "GROUP BY p.nombre ORDER BY p.nombre",
            (f"%{nombre}%",),
        ).fetchall()
    else:
        filas = conexion.execute(
            "SELECT p.nombre, SUM(p.cantidad), "
            "(SELECT precio FROM productos WHERE nombre = p.nombre "
            "ORDER BY id DESC LIMIT 1) "
            "FROM productos p GROUP BY p.nombre ORDER BY p.nombre"
        ).fetchall()
    conexion.close()
    return filas


def listar_detalle_producto(nombre):
    conexion = conectar()
    filas = conexion.execute(
        "SELECT c.fecha, c.hora, p.cantidad, p.precio "
        "FROM productos p JOIN compras c ON c.id = p.compra_id "
        "WHERE p.nombre = ? ORDER BY c.fecha, c.hora, p.id",
        (nombre,),
    ).fetchall()
    conexion.close()
    return filas
