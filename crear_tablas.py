from BdD.basededatos import engine, base
import Modelos.modelos
base.metadata.create_all(bind=engine)
print("Tablas creadas en inventario.db")