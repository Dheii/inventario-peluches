import sys
import os
from datetime import datetime

sys.path.append(r"C:\Users\Admin\Documents\inventario-peluches")

from BdD.basededatos import SessionLocal
from Managers.producto_manager import ProductoManager


def menu():
    print("\nINVENTARIO")
    print("1. Agregar producto")
    print("2. Listar productos")
    print("3. Actualizar stock")
    print("4. Eliminar producto")
    print("5. Listar movimientos")
    print("0. Salir")


def main():
    db = SessionLocal()
    manager = ProductoManager(db)

    while True:
        menu()
        opcion = input("Selecciona una opción: ")

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
                          f"{p.cantidad_stock} unidades, {p.precio_unitario} bs")
            else:
                print("No hay productos registrados.")

        elif opcion == "3":
            try:
                id_peluche = int(input("ID del producto: "))
                cantidad = int(input("Cantidad a actualizar: "))
                tipo = input("Tipo de movimiento (entrada/salida): ").strip().lower()
                actualizado = manager.actualizar_stock(id_peluche, cantidad, tipo)
                print(f"Stock actualizado. Nuevo stock: {actualizado.cantidad_stock}")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "4":
            id_peluche = int(input("ID del producto a eliminar: "))
            if manager.eliminar_producto(id_peluche):
                print("Producto eliminado.")
            else:
                print("Producto no encontrado.")

        elif opcion == "5":
            break
            
        elif opcion == "0":
            break

        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()