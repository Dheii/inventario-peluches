from Modelos.modelos import Producto, MovimientoInventario
from datetime import datetime

class ProductoManager:
    def __init__(self, db):
        self.db = db

    def agregar_producto(self, nombre, categoria, tamano, precio, cantidad):
        nuevo = Producto(
            nombre=nombre,
            categoria=categoria,
            tamano=tamano,
            precio_unitario=precio,
            cantidad_stock=cantidad,
            fecha_ingreso=datetime.now()
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def listar_productos(self):
        return self.db.query(Producto).all()

    def actualizar_nombre(self, id_peluche, nuevo_nombre):
        producto = self.db.query(Producto).filter_by(id_peluche=id_peluche).first()
        if not producto:
            raise ValueError("Producto no encontrado")
        producto.nombre = nuevo_nombre
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def actualizar_precio(self, id_peluche, nuevo_precio):
        producto = self.db.query(Producto).filter_by(id_peluche=id_peluche).first()
        if not producto:
            raise ValueError("Producto no encontrado")
        producto.precio_unitario = nuevo_precio
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def actualizar_categoria(self, id_peluche, nueva_categoria):
        producto = self.db.query(Producto).filter_by(id_peluche=id_peluche).first()
        if not producto:
            raise ValueError("Producto no encontrado")
        producto.categoria = nueva_categoria
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def actualizar_tamano(self, id_peluche, nuevo_tamano):
        producto = self.db.query(Producto).filter_by(id_peluche=id_peluche).first()
        if not producto:
            raise ValueError("Producto no encontrado")
        producto.tamano = nuevo_tamano
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def actualizar_stock(self, id_peluche, cantidad, tipo="entrada"):
        producto = self.db.query(Producto).filter_by(id_peluche=id_peluche).first()
        if not producto:
            raise ValueError("Producto no encontrado")

        if tipo == "entrada":
            producto.cantidad_stock += cantidad
        elif tipo == "salida":
            if producto.cantidad_stock >= cantidad:
                producto.cantidad_stock -= cantidad
            else:
                raise ValueError("Stock insuficiente")
        else:
            raise ValueError("Tipo de movimiento inválido")
        movimiento = MovimientoInventario(
            producto_id=producto.id_peluche,
            tipo=tipo,
            cantidad=cantidad,
            fecha=datetime.now()
        )
        self.db.add(movimiento)
        try:
            self.db.commit()
            self.db.refresh(producto)
        except Exception as e:
            self.db.rollback()
            raise e
        return producto

    def eliminar_producto(self, id_peluche):
        producto = self.db.query(Producto).filter_by(id_peluche=id_peluche).first()
        if producto:
            self.db.delete(producto)
            self.db.commit()
            return True
        return False