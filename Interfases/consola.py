import sys
import os

sys.path.append(r"C:\Users\Admin\Documents\inventario-peluches")

import argparse
from BdD.basededatos import SessionLocal
from Managers.producto_manager import ProductoManager
from Modelos.modelos import MovimientoInventario


db = SessionLocal()
manager = ProductoManager(db)

def cmd_agregar(args):
    producto = manager.agregar_producto(
        nombre=args.nombre,
        categoria=args.categoria,
        tamano=args.tamano,
        precio=args.precio,
        cantidad=args.cantidad
    )
    print(f"Producto agregado: {producto.id_peluche} - {producto.nombre}")

def cmd_listar(args):
    productos = manager.listar_productos()
    if not productos:
        print("No hay productos en inventario.")
    for p in productos:
        print(f"{p.id_peluche}: {p.nombre}, Categoría: {p.categoria}, "
              f"Tamaño: {p.tamano}, Precio: {p.precio_unitario}, Stock: {p.cantidad_stock}")

def cmd_actualizar(args):
    try:
        producto = manager.actualizar_stock(
            id_peluche=args.id,
            cantidad=args.cantidad,
            tipo=args.tipo
        )
        print(f"Stock actualizado: {producto.id_peluche} - {producto.nombre}, Stock actual: {producto.cantidad_stock}")
    except ValueError as e:
        print("Error:", e)

def cmd_movimientos(args):
    movimientos = db.query(MovimientoInventario).all()
    if not movimientos:
        print("No hay movimientos registrados.")
    for m in movimientos:
        print(f"Tipo: {m.tipo}, Cantidad: {m.cantidad}, Fecha: {m.fecha}")

def cmd_eliminar(args):
    exito = manager.eliminar_producto(id_peluche=args.id)
    if exito:
        print(f"Producto {args.id} eliminado.")
    else:
        print(f"No se encontró el producto con id {args.id}.")

parser = argparse.ArgumentParser(description="Gestión de inventario de peluches")
subparsers = parser.add_subparsers()

#para agregar
parser_agregar = subparsers.add_parser("agregar", help="Agregar un nuevo producto")
parser_agregar.add_argument("nombre", type=str)
parser_agregar.add_argument("categoria", type=str)
parser_agregar.add_argument("tamano", type=str)
parser_agregar.add_argument("precio", type=float)
parser_agregar.add_argument("cantidad", type=int)
parser_agregar.set_defaults(func=cmd_agregar)

#para listar
parser_listar = subparsers.add_parser("listar", help="Listar todos los productos")
parser_listar.set_defaults(func=cmd_listar)

#para actualizar mi stock
parser_actualizar = subparsers.add_parser("actualizar", help="Actualizar stock de un producto")
parser_actualizar.add_argument("id", type=int)
parser_actualizar.add_argument("cantidad", type=int)
parser_actualizar.add_argument("tipo", type=str, choices=["entrada","salida"])
parser_actualizar.set_defaults(func=cmd_actualizar)

#mostrar movimientos
parser_movimientos = subparsers.add_parser("movimientos", help="Mostrar movimientos de inventario")
parser_movimientos.set_defaults(func=cmd_movimientos)

#para eliminar
parser_eliminar = subparsers.add_parser("eliminar", help="Eliminar un producto")
parser_eliminar.add_argument("id", type=int)
parser_eliminar.set_defaults(func=cmd_eliminar)

args = parser.parse_args()
if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()

db.close()