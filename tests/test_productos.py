import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Modelos.modelos import base, Producto

class TestProductos(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = create_engine("sqlite:///inventario.db", echo=True)
        base.metadata.create_all(engine)
        cls.Session = sessionmaker(bind=engine)

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.close()

    def test_crear_producto(self):
        p = Producto(nombre="Oso Panda", categoria="Animal", tamano="Mediano", cantidad_stock=10, precio_unitario=25.5)
        self.session.add(p)
        self.session.commit()

        producto_bd = self.session.query(Producto).filter_by(nombre="Oso Panda").first()
        self.assertIsNotNone(producto_bd)
        self.assertEqual(producto_bd.cantidad_stock, 10)

    def test_actualizar_producto(self):
        p = Producto(nombre="Pikachu", categoria="Anime", tamano="Pequeño", cantidad_stock=5, precio_unitario=30)
        self.session.add(p)
        self.session.commit()

        p.precio_unitario = 35
        p.cantidad_stock += 3
        self.session.commit()

        self.assertEqual(p.precio_unitario, 35)
        self.assertEqual(p.cantidad_stock, 8)

    def test_eliminar_producto(self):
        p = Producto(nombre="Charmander", categoria="Anime", tamano="Mediano", cantidad_stock=6, precio_unitario=22)
        self.session.add(p)
        self.session.commit()

        self.session.delete(p)
        self.session.commit()

        eliminado = self.session.query(Producto).filter_by(nombre="Charmander").first()
        self.assertIsNone(eliminado)
