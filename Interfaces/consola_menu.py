from BdD.basededatos import SessionLocal
from Managers.producto_manager import ProductoManager
from Modelos.modelos import MovimientoInventario, Producto

def menu_principal():
    print("\n=== INVENTARIO ===")
    print("1. Agregar producto")
    print("2. Listar productos")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Listar movimientos")
    print("6. Salir")

def menu_actualizacion():
    print("\n=== QUE DESEA ACTUALIZAR? ===")
    print("1. Actualizar nombre")
    print("2. Actualizar precio")
    print("3. Actualizar categoría")
    print("4. Actualizar tamaño")
    print("5. Actualizar cantidad (stock)")
    print("6. Atrás")

def main():
    db = SessionLocal()
    manager = ProductoManager(db)
    try:
        while True:
            menu_principal()
            opcion = input("Que desea hacer?: ").strip()
            if opcion == "1":
                nombre = input("Nombre: ")
                categoria = input("Categoría: ")
                tamano = input("Tamaño: ")
                precio = float(input("Precio unitario: "))
                cantidad = int(input("Cantidad inicial: "))
                producto = manager.agregar_producto(nombre, categoria, tamano, precio, cantidad)
                print(f"Producto agregado con ID {producto.id_peluche}")
            elif opcion == "2":
                productos = manager.listar_productos()
                if productos:
                    print("\nPRODUCTOS EN INVENTARIO:")
                    for p in productos:
                        print(f"ID {p.id_peluche} | {p.nombre} ({p.categoria}, {p.tamano}) - "
                              f"{p.cantidad_stock} unidades, {p.precio_unitario} Bs")
                else:
                    print("No hay productos registrados.")
            elif opcion == "3":
                while True:
                    menu_actualizacion()
                    sub_opcion = input("Seleccione una opción: ").strip()
                    if sub_opcion == "1":
                        try:
                            id_p = int(input("ID del producto: "))
                            nuevo_nombre = input("Nuevo nombre: ")
                            actualizado = manager.actualizar_nombre(id_p, nuevo_nombre)
                            print(f"Nombre actualizado a: {actualizado.nombre}")
                        except Exception as e:
                            print(f"Error:{e}")
                    elif sub_opcion == "2":
                        try:
                            id_p = int(input("ID del producto: "))
                            nuevo_precio = float(input("Nuevo precio unitario: "))
                            actualizado = manager.actualizar_precio(id_p, nuevo_precio)
                            print(f"Precio actualizado a: {actualizado.precio_unitario} Bs")
                        except Exception as e:
                            print(f"Error: {e}")
                    elif sub_opcion == "3":
                        try:
                            id_p = int(input("ID del producto: "))
                            nueva_categoria = input("Nueva categoría: ")
                            actualizado = manager.actualizar_categoria(id_p, nueva_categoria)
                            print(f"Categoría actualizada a: {actualizado.categoria}")
                        except Exception as e:
                            print(f"Error: {e}")
                    elif sub_opcion == "4":
                        try:
                            id_p = int(input("ID del producto: "))
                            nuevo_tamano = input("Nuevo tamaño: ")
                            actualizado = manager.actualizar_tamano(id_p, nuevo_tamano)
                            print(f"Tamaño actualizado a: {actualizado.tamano}")
                        except Exception as e:
                            print(f"Error: {e}")
                    elif sub_opcion == "5":
                        try:
                            id_p = int(input("ID del producto: "))
                            cantidad = int(input("Cantidad a actualizar: "))
                            tipo = input("Tipo de movimiento (entrada/salida): ").strip().lower()
                            actualizado = manager.actualizar_stock(id_p, cantidad, tipo)
                            print(f"Stock actualizado. Nuevo stock: {actualizado.cantidad_stock}")
                        except Exception as e:
                            print(f"Error: {e}")
                    elif sub_opcion == "6":
                        break
                    else:
                        print("Opción no válida.")
            elif opcion == "4":
                try:
                    id_peluche = int(input("ID del producto a eliminar: "))
                    if manager.eliminar_producto(id_peluche):
                        print("Producto eliminado.")
                    else:
                        print("Producto no encontrado.")
                except ValueError:
                    print("ID inválido.")
            elif opcion == "5":
                resultados = db.query(MovimientoInventario, Producto).join(
                    Producto, MovimientoInventario.producto_id == Producto.id_peluche
                ).order_by(MovimientoInventario.fecha).all()
                if resultados:
                    print("\nMOVIMIENTOS DE INVENTARIO:")
                    for mov, prod in resultados:
                        print(f"ID {mov.id_movimiento} | Producto: {prod.nombre} | "
                              f"Tipo: {mov.tipo} | Cantidad: {mov.cantidad} | Fecha: {mov.fecha}")
                else:
                    print("No hay movimientos registrados.")
            elif opcion == "6":
                break
            else:
                print("Opción no válida, intenta de nuevo.")
    finally:
        db.close()
if __name__ == "__main__":
    main()