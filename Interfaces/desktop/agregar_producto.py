import tkinter as tk
from tkinter import ttk, messagebox
from BdD.basededatos import SessionLocal
from Managers.producto_manager import ProductoManager

class AgregarProductoWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Agregar producto")
        self.geometry("380x360")
        self.resizable(False, False)

        self.db = SessionLocal()
        self.manager = ProductoManager(self.db)

        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="both", expand=True)

        labels = ["Nombre", "Categoría", "Tamaño", "Cantidad inicial", "Precio unitario"]
        self.entries = {}

        for lbl in labels:
            row = ttk.Frame(frame)
            row.pack(fill="x", pady=6)
            ttk.Label(row, text=lbl, width=18).pack(side="left")
            ent = ttk.Entry(row)
            ent.pack(side="left", fill="x", expand=True)
            self.entries[lbl] = ent

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=12)
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side="left", expand=True)
        ttk.Button(btn_frame, text="Cerrar", command=self.destroy).pack(side="right")

    def guardar(self):
        try:
            nombre = self.entries["Nombre"].get().strip()
            categoria = self.entries["Categoría"].get().strip()
            tamano = self.entries["Tamaño"].get().strip()
            cantidad = int(self.entries["Cantidad inicial"].get())
            precio = float(self.entries["Precio unitario"].get())

            if not nombre:
                raise ValueError("Nombre vacío")

            producto = self.manager.agregar_producto(nombre, categoria, tamano, precio, cantidad)
            messagebox.showinfo("Éxito", f"Producto agregado con ID {producto.id_peluche}")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))
