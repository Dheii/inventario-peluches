from BdD.basededatos import SessionLocal
from Modelos.modelos import Producto, MovimientoInventario
from Managers.producto_manager import ProductoManager
from datetime import datetime

# Crear sesión
db = SessionLocal()

# Crear manager
manager = ProductoManager(db)

# --- Agregar productos ---
print("Agregando productos...")
producto1 = manager.agregar_producto(
    nombre="Peluche Oso",
    categoria="Oso",
    tamano="Mediano",
    precio=15.50,
    cantidad=10
)

producto2 = manager.agregar_producto(
    nombre="Peluche Conejo",
    categoria="Conejo",
    tamano="Pequeño",
    precio=12.00,
    cantidad=5
)

# --- Listar productos ---
print("\nProductos actuales:")
for p in manager.listar_productos():
    print(f"{p.id_peluche}: {p.nombre}, Stock: {p.cantidad_stock}, Precio: {p.precio_unitario}")

# --- Actualizar stock ---
print("\nActualizando stock...")
manager.actualizar_stock(id_peluche=producto1.id_peluche, cantidad=5, tipo="entrada")
manager.actualizar_stock(id_peluche=producto2.id_peluche, cantidad=2, tipo="salida")

# Listar productos después de actualizar stock
print("\nProductos después de actualizar stock:")
for p in manager.listar_productos():
    print(f"{p.id_peluche}: {p.nombre}, Stock: {p.cantidad_stock}")

# --- Eliminar un producto ---
print("\nEliminando producto 2 (Conejo)...")
manager.eliminar_producto(id_peluche=producto2.id_peluche)

# Listar productos finales
print("\nProductos finales:")
for p in manager.listar_productos():
    print(f"{p.id_peluche}: {p.nombre}, Stock: {p.cantidad_stock}")

# --- Mostrar movimientos de inventario ---
print("\nMovimientos de inventario registrados:")
movimientos = db.query(MovimientoInventario).all()
for m in movimientos:
    print(f"{m.id_movimiento}: Tipo: {m.tipo}, Cantidad: {m.cantidad}, Fecha: {m.fecha}")

# Cerrar sesión
db.close()