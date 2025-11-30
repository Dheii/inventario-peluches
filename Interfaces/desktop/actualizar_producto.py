import tkinter as tk
from tkinter import ttk, messagebox
from BdD.basededatos import SessionLocal
from Modelos.modelos import Producto
from datetime import datetime

class ActualizarProductoWindow(tk.Toplevel):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Actualizar producto")
        self.geometry("460x420")
        self.resizable(False, False)

        self.db = SessionLocal()

        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="ID del producto:").pack(anchor="w")
        id_frame = ttk.Frame(frame)
        id_frame.pack(fill="x", pady=6)
        self.id_entry = ttk.Entry(id_frame)
        self.id_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(id_frame, text="Cargar", command=self.cargar_producto).pack(side="right", padx=6)

        # Info actual
        self.info = ttk.Label(frame, text="Cargue un producto para ver sus datos", anchor="w")
        self.info.pack(fill="x", pady=6)

        # Opciones
        ttk.Label(frame, text="Campo a actualizar:").pack(anchor="w", pady=(8,2))
        self.opcion_var = tk.StringVar(value="nombre")
        opciones = [
            ("Nombre", "nombre"),
            ("Precio", "precio"),
            ("Categoría", "categoria"),
            ("Tamaño", "tamano"),
            ("Ajustar stock (entrada/salida)", "stock"),
        ]
        for text,val in opciones:
            ttk.Radiobutton(frame, text=text, variable=self.opcion_var, value=val).pack(anchor="w")

        ttk.Separator(frame).pack(fill="x", pady=8)

        ttk.Label(frame, text="Nuevo valor:").pack(anchor="w")
        self.valor_entry = ttk.Entry(frame)
        self.valor_entry.pack(fill="x", pady=6)

        # Para operaciones de stock extra
        cantidad_frame = ttk.Frame(frame)
        cantidad_frame.pack(fill="x", pady=4)
        ttk.Label(cantidad_frame, text="Cantidad (solo para stock):").pack(side="left")
        self.cantidad_entry = ttk.Entry(cantidad_frame, width=10)
        self.cantidad_entry.pack(side="left", padx=6)
        ttk.Label(cantidad_frame, text="Tipo:").pack(side="left", padx=(12,4))
        self.tipo_var = tk.StringVar(value="entrada")
        ttk.Combobox(cantidad_frame, textvariable=self.tipo_var, values=["entrada","salida"], width=10).pack(side="left")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=12)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar).pack(side="left", expand=True)
        ttk.Button(btn_frame, text="Cerrar", command=self.destroy).pack(side="right")

        self.loaded_producto = None

    def cargar_producto(self):
        try:
            id_p = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Error", "ID inválido")
            return

        session = self.db
        producto = session.query(Producto).filter_by(id_peluche=id_p).first()
        session.close()
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return

        self.loaded_producto = producto
        self.info.configure(text=f"ID {producto.id_peluche} — {producto.nombre} — {producto.categoria} — {producto.tamano} — Stock: {producto.cantidad_stock} — Precio: {producto.precio_unitario}")

    def actualizar(self):
        if not self.loaded_producto:
            messagebox.showerror("Error", "Antes cargue el producto con 'Cargar'")
            return

        campo = self.opcion_var.get()
        session = self.db
        try:
            producto = session.query(Producto).filter_by(id_peluche=self.loaded_producto.id_peluche).first()
            if not producto:
                raise ValueError("Producto no existe")

            if campo == "nombre":
                nuevo = self.valor_entry.get().strip()
                if not nuevo:
                    raise ValueError("Nombre vacío")
                producto.nombre = nuevo

            elif campo == "precio":
                nuevo = float(self.valor_entry.get())
                producto.precio_unitario = nuevo

            elif campo == "categoria":
                producto.categoria = self.valor_entry.get().strip()

            elif campo == "tamano":
                producto.tamano = self.valor_entry.get().strip()

            elif campo == "stock":
                # La entrada usa cantidad_entry y tipo_var
                cantidad = int(self.cantidad_entry.get())
                tipo = self.tipo_var.get()
                if tipo == "entrada":
                    producto.cantidad_stock += cantidad
                else:
                    if producto.cantidad_stock < cantidad:
                        raise ValueError("Stock insuficiente")
                    producto.cantidad_stock -= cantidad
                    
                from Modelos.modelos import MovimientoInventario
                mov = MovimientoInventario(
                    producto_id=self.loaded_producto.id_peluche,
                    tipo=tipo,
                    cantidad=cantidad,
                    fecha=datetime.now()
                )
                session.add(mov)

            session.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            
            self.loaded_producto = producto
            self.info.configure(text=f"ID {producto.id_peluche} — {producto.nombre} — {producto.categoria} — {producto.tamano} — Stock: {producto.cantidad_stock} — Precio: {producto.precio_unitario}")

        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            session.close()
