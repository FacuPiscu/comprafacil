from datetime import date

from base_datos import conectar, crear_tabla


def registrar_compra(articulos, fecha=None):
    if fecha is None:
        fecha = date.today().isoformat()
    conexion = conectar()
    crear_tabla(conexion)
    compra_id = conexion.execute(
        "SELECT COALESCE(MAX(compra_id), 0) + 1 FROM compras"
    ).fetchone()[0]
    conexion.executemany(
        "INSERT INTO compras (compra_id, producto, cantidad, precio, fecha) "
        "VALUES (?, ?, ?, ?, ?)",
        [
            (compra_id, producto, cantidad, precio, fecha)
            for producto, cantidad, precio in articulos
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
        "SELECT compra_id, producto, cantidad, precio FROM compras "
        "WHERE fecha = ? ORDER BY compra_id, id",
        (fecha,),
    ).fetchall()
    conexion.close()
    return filas


def listar_compras():
    conexion = conectar()
    filas = conexion.execute(
        "SELECT compra_id, fecha, SUM(cantidad * precio), SUM(cantidad) "
        "FROM compras GROUP BY compra_id ORDER BY fecha, compra_id"
    ).fetchall()
    conexion.close()
    return filas


def listar_articulos(compra_id):
    conexion = conectar()
    filas = conexion.execute(
        "SELECT id, producto, cantidad, precio FROM compras "
        "WHERE compra_id = ? ORDER BY id",
        (compra_id,),
    ).fetchall()
    conexion.close()
    return filas


def eliminar_articulo(id_articulo):
    conexion = conectar()
    conexion.execute("DELETE FROM compras WHERE id = ?", (id_articulo,))
    conexion.commit()
    conexion.close()
