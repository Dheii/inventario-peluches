import tkinter as tk
from tkinter import ttk, messagebox
from BdD.basededatos import SessionLocal
from Modelos.modelos import Producto

class EliminarProductoWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Eliminar producto")
        self.geometry("380x240")
        self.resizable(False, False)

        self.db = SessionLocal()

        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="ID del producto a eliminar:").pack(anchor="w")

        self.id_entry = ttk.Entry(frame)
        self.id_entry.pack(fill="x", pady=6)

        ttk.Button(frame, text="Eliminar", command=self.eliminar).pack(fill="x", pady=6)
        ttk.Button(frame, text="Cerrar", command=self.destroy).pack(fill="x", pady=6)

    def eliminar(self):
        try:
            id_p = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Error", "ID inválido")
            return

        session = self.db
        producto = session.query(Producto).filter_by(id_peluche=id_p).first()

        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return

        # Confirmación
        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar el producto:\n\n{producto.nombre}?\n\nEsta acción no se puede deshacer."
        ):
            return

        try:
            session.delete(producto)
            session.commit()
            messagebox.showinfo("Eliminado", "Producto eliminado correctamente")

        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            session.close()
            self.destroy()
