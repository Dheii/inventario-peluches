from sqlalchemy import Column, Integer, String, Float
from BdD.basededatos import base

class Producto(base):

	_tablename_= "PRODUCTOS"

	id_peluche= Column(Integer, primary_key= True, index= True)
	nombre= Column(String, nullable= False)
	categoria= Column(String, nullable=False)
	tamaño= Column(String, nullable=False)
	precio_unitario= Column(Float, nullable=False)
	cantidad_stock= Column(Int, nullable=False)
	fecha_ingreso= Column(String, nullable= False)

class MOVIMIENTO_INVENTARIO(base):
	
	_tablename_= "MOVIMIENTO DE INVENTARIO"

        tipo= Column(String, nullable= False)
        cantidad= Column(Int, nullable= False)
        Fecha= Column(Integer, primary_key= index= True)
        tamaño= Column(String, nullable=False)
