import sqlite3

NOMBRE_BD = "compras.db"


def conectar():
    return sqlite3.connect(NOMBRE_BD)


def crear_tabla(conexion):
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            compra_id INTEGER NOT NULL DEFAULT 0,
            producto TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            fecha TEXT NOT NULL
        )
    """)
    columnas = [
        fila[1]
        for fila in conexion.execute("PRAGMA table_info(compras)").fetchall()
    ]
    if "compra_id" not in columnas:
        conexion.execute(
            "ALTER TABLE compras ADD COLUMN compra_id INTEGER NOT NULL DEFAULT 0"
        )
        conexion.execute("UPDATE compras SET compra_id = id WHERE compra_id = 0")
    conexion.commit()


def crear_tabla_reportes(conexion):
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS reportes_guardados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_generacion TEXT NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT NOT NULL,
            total REAL NOT NULL,
            cantidad_compras INTEGER NOT NULL
        )
    """)
    conexion.commit()
