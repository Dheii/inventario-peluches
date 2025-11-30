import tkinter as tk
from tkinter import ttk
from BdD.basededatos import SessionLocal
from Managers.producto_manager import ProductoManager

class ListarProductosWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Productos en inventario")
        self.geometry("1000x420")

        self.db = SessionLocal()
        self.manager = ProductoManager(self.db)

        container = ttk.Frame(self, padding=8)
        container.pack(fill="both", expand=True)

        cols = ("ID","Nombre","Categoría","Tamaño","Stock","Precio (Bs)")
        self.tree = ttk.Treeview(container, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center")

        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.load_data()

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        productos = self.manager.listar_productos()
        for p in productos:
            self.tree.insert("", "end", values=(
                p.id_peluche, p.nombre, p.categoria, p.tamano, p.cantidad_stock, p.precio_unitario
            ))
