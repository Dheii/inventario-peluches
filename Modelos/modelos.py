from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey

from BdD.basededatos import base# importas la Base que definiste (la nombraste 'base')


class Producto(base):
    __tablename__ = "productos"

    id_peluche = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    tamano = Column(String(50), nullable=False)          # evité usar 'ñ' en el identificador
    precio_unitario = Column(Float, nullable=False)
    cantidad_stock = Column(Integer, nullable=False, default=0)
    fecha_ingreso = Column(DateTime, nullable=False)

    # Relación opcional con movimientos
    


class MovimientoInventario(base):
    __tablename__ = "movimientos_inventario"

    id_movimiento = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tipo = Column(String(20), nullable=False)     # por ejemplo: 'entrada' o 'salida'
    cantidad = Column(Integer, nullable=False)
    fecha = Column(DateTime, nullable=False)