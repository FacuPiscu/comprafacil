from base_datos import conectar


def obtener_total_compra(compra_id):
    conexion = conectar()
    filas = conexion.execute(
        "SELECT cantidad, precio FROM compras WHERE compra_id = ?",
        (compra_id,),
    ).fetchall()
    conexion.close()
    if not filas:
        return 0.0, 0
    total = sum(cantidad * precio for cantidad, precio in filas)
    unidades = sum(cantidad for cantidad, _ in filas)
    return float(total), int(unidades)


def comparar_compras(compra_uno, compra_dos):
    total_uno, unidades_uno = obtener_total_compra(compra_uno)
    total_dos, unidades_dos = obtener_total_compra(compra_dos)
    diferencia = total_dos - total_uno
    porcentaje = (diferencia / total_uno * 100) if total_uno > 0 else 0.0

    print("\n=============== COMPARACION DE COMPRAS ===============")
    print(f"Compra {compra_uno}: ${total_uno:.2f} en {unidades_uno} unidades")
    print(f"Compra {compra_dos}: ${total_dos:.2f} en {unidades_dos} unidades")
    print("-" * 50)
    if diferencia > 0:
        print(
            f"La compra {compra_dos} supero por ${diferencia:.2f} "
            f"({porcentaje:.2f}%)"
        )
    elif diferencia < 0:
        print(
            f"La compra {compra_uno} supero por ${abs(diferencia):.2f} "
            f"({abs(porcentaje):.2f}%)"
        )
    else:
        print("No hubo diferencia entre las compras")
