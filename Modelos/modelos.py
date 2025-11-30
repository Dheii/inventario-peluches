from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from BdD.basededatos import base

class Producto(base):
    __tablename__ = "productos"

    id_peluche = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    tamano = Column(String(50), nullable=False)
    precio_unitario = Column(Float, nullable=False)
    cantidad_stock = Column(Integer, nullable=False, default=0)
    fecha_ingreso = Column(DateTime, nullable=False, default=datetime.now)
    
    movimientos = relationship("MovimientoInventario", back_populates="producto", cascade="all, delete-orphan")


class MovimientoInventario(base):
    __tablename__ = "movimientos_inventario"

    id_movimiento = Column(Integer, primary_key=True, autoincrement=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id_peluche"), nullable=False) 
    tipo = Column(String(20), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha = Column(DateTime, nullable=False)
    
    producto = relationship("Producto", back_populates="movimientos")