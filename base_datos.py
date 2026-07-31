import sqlite3

NOMBRE_BD = "compras.db"


def conectar():
    return sqlite3.connect(NOMBRE_BD)


def crear_tabla(conexion):
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monto REAL NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    """)
    conexion.commit()


def crear_tabla_reportes(conexion):
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS reportes_guardados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_generacion TEXT NOT NULL,
            compra_uno INTEGER NOT NULL,
            compra_dos INTEGER NOT NULL,
            diferencia REAL NOT NULL,
            contenido TEXT NOT NULL
        )
    """)
    conexion.commit()


def crear_tabla_productos(conexion):
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            compra_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)
    conexion.commit()


def migrar_datos(conexion):
    columnas = [
        fila[1]
        for fila in conexion.execute("PRAGMA table_info(compras)").fetchall()
    ]
    if "producto" not in columnas:
        return
    conexion.execute("""
        CREATE TABLE compras_nueva (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monto REAL NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    """)
    conexion.execute("""
        CREATE TABLE productos_nueva (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            compra_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)
    conexion.execute("""
        INSERT INTO compras_nueva (id, monto, fecha, hora)
        SELECT compra_id, SUM(cantidad * precio),
               substr(fecha, 1, 10), substr(fecha, 12, 5)
        FROM compras GROUP BY compra_id
    """)
    conexion.execute("""
        INSERT INTO productos_nueva (compra_id, nombre, cantidad, precio)
        SELECT compra_id, producto, cantidad, precio FROM compras
    """)
    conexion.execute("DROP TABLE compras")
    conexion.execute("DROP TABLE IF EXISTS productos")
    conexion.execute("ALTER TABLE compras_nueva RENAME TO compras")
    conexion.execute("ALTER TABLE productos_nueva RENAME TO productos")
    conexion.commit()


def migrar_tabla_reportes(conexion):
    columnas = [
        fila[1]
        for fila in conexion.execute(
            "PRAGMA table_info(reportes_guardados)"
        ).fetchall()
    ]
    if "fecha_inicio" in columnas:
        conexion.execute("DROP TABLE reportes_guardados")
        crear_tabla_reportes(conexion)


def crear_tablas():
    conexion = conectar()
    migrar_datos(conexion)
    migrar_tabla_reportes(conexion)
    crear_tabla(conexion)
    crear_tabla_reportes(conexion)
    crear_tabla_productos(conexion)
    conexion.close()
