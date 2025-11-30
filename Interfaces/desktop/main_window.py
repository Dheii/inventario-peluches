import tkinter as tk
from tkinter import ttk
from .agregar_producto import AgregarProductoWindow
from .listar_productos import ListarProductosWindow
from .actualizar_producto import ActualizarProductoWindow
from .listar_movimientos import ListarMovimientosWindow
from .eliminar_producto import EliminarProductoWindow

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YONOLODESCARGOPORQUEYALOTENGO")
        self.geometry("420x480")
        self.resizable(False, False)

        header = ttk.Label(self, text="INVENTARIO DE PELUCHES", font=("Segoe UI", 16))
        header.pack(pady=18)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=30)

        ttk.Button(btn_frame, text="Agregar producto", command=self.open_agregar).pack(fill="x", pady=6)
        ttk.Button(btn_frame, text="Listar productos", command=self.open_listar).pack(fill="x", pady=6)
        ttk.Button(btn_frame, text="Actualizar producto", command=self.open_actualizar).pack(fill="x", pady=6)
        ttk.Button(btn_frame, text="Eliminar producto", command=self.open_eliminar).pack(fill="x", pady=6)
        ttk.Button(btn_frame, text="Listar movimientos", command=self.open_movimientos).pack(fill="x", pady=6)
        ttk.Button(btn_frame, text="Salir", command=self.destroy).pack(fill="x", pady=18)

        footer = ttk.Label(self, text="DE MI PARA MI UwU", font=("Segoe UI", 9))
        footer.pack(side="bottom", pady=12)

    def open_agregar(self):
        AgregarProductoWindow(self)

    def open_listar(self):
        ListarProductosWindow(self)

    def open_actualizar(self):
        ActualizarProductoWindow(self)

    def open_eliminar(self):
        EliminarProductoWindow(self)

    def open_movimientos(self):
        ListarMovimientosWindow(self)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
