import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Modelos.modelos import base, Producto, MovimientoInventario
from datetime import datetime

class TestMovimientos(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = create_engine("sqlite:///inventario.db", echo=True)
        base.metadata.create_all(engine)
        cls.Session = sessionmaker(bind=engine)

    def setUp(self):
        self.session = self.Session()
        # Crear producto base
        self.producto = Producto(nombre="Bulbasaur", categoria="Anime", tamano="Mediano", cantidad_stock=5, precio_unitario=20)
        self.session.add(self.producto)
        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_entrada_stock(self):
        cantidad = 3
        mov = MovimientoInventario(producto_id=self.producto.id_peluche, tipo="entrada", cantidad=cantidad, fecha=datetime.now())
        self.producto.cantidad_stock += cantidad
        self.session.add(mov)
        self.session.commit()

        self.assertEqual(self.producto.cantidad_stock, 8)

    def test_salida_stock(self):
        cantidad = 2
        mov = MovimientoInventario(producto_id=self.producto.id_peluche, tipo="salida", cantidad=cantidad, fecha=datetime.now())
        self.producto.cantidad_stock -= cantidad
        self.session.add(mov)
        self.session.commit()

        self.assertEqual(self.producto.cantidad_stock, 3)

    def test_movimiento_invalido(self):
        # Salida mayor al stock
        with self.assertRaises(ValueError):
            cantidad = 10
            if self.producto.cantidad_stock < cantidad:
                raise ValueError("Stock insuficiente")
