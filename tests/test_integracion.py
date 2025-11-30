import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Modelos.modelos import base, Producto, MovimientoInventario
from datetime import datetime

class TestIntegracion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = create_engine("sqlite:///inventario.db", echo=True)
        base.metadata.create_all(engine)
        cls.Session = sessionmaker(bind=engine)

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.close()

    def test_crear_producto_y_entrada_stock(self):
        # Crear producto
        p = Producto(nombre="Oso Polar", categoria="Animal", tamano="Grande", cantidad_stock=0, precio_unitario=50)
        self.session.add(p)
        self.session.commit()

        # Entrada de stock
        mov = MovimientoInventario(producto_id=p.id_peluche, tipo="entrada", cantidad=10, fecha=datetime.now())
        p.cantidad_stock += 10
        self.session.add(mov)
        self.session.commit()

        producto_bd = self.session.query(Producto).filter_by(nombre="Oso Polar").first()
        self.assertEqual(producto_bd.cantidad_stock, 10)
