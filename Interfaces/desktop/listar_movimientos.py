import tkinter as tk
from tkinter import ttk
from BdD.basededatos import SessionLocal
from Modelos.modelos import MovimientoInventario, Producto

class ListarMovimientosWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Movimientos de Inventario")
        self.geometry("1000x420")

        self.db = SessionLocal()

        container = ttk.Frame(self, padding=8)
        container.pack(fill="both", expand=True)

        cols = ("ID_mov","Producto","Tipo","Cantidad","Fecha")
        self.tree = ttk.Treeview(container, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        self.load_data()

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        session = self.db
        resultados = session.query(MovimientoInventario, Producto).join(
            Producto, MovimientoInventario.producto_id == Producto.id_peluche
        ).order_by(MovimientoInventario.fecha).all()
        session.close()

        for mov, prod in resultados:
            self.tree.insert("", "end", values=(mov.id_movimiento, prod.nombre, mov.tipo, mov.cantidad, mov.fecha))
