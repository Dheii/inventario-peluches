import sqlite3

# Conectar a la base
conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

# Ver todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()
print("Tablas en la base:", tablas)

# Ver contenido de 'productos'
cursor.execute("SELECT * FROM productos;")
productos = cursor.fetchall()
print("Contenido de productos:")
for p in productos:
    print(p)

# Ver contenido de 'movimientos_inventario'
cursor.execute("SELECT * FROM movimientos_inventario;")
movimientos = cursor.fetchall()
print("Contenido de movimientos_inventario:")
for m in movimientos:
    print(m)

conn.close()