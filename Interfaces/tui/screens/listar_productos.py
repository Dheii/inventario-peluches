from textual.screen import Screen
from textual.widgets import Static
from BdD.basededatos import SessionLocal
from Managers.producto_manager import ProductoManager

class ListarProductosScreen(Screen):

    BINDINGS = [
        ("escape", "go_back", "Atrás")
    ]

    def action_go_back(self):
        self.app.pop_screen()

    def on_mount(self):
        self.db = SessionLocal()
        self.manager = ProductoManager(self.db)

        self.output = Static("", id="output")
        self.mount(self.output)

        self.show_products()

    def show_products(self):
        productos = self.manager.listar_productos()

        if productos:
            texto = "\n".join(
                f"ID {p.id_peluche} | {p.nombre} ({p.categoria}, {p.tamano}) - "
                f"{p.cantidad_stock} unidades, {p.precio_unitario} Bs"
                for p in productos
            )
            self.output.update(texto)
        else:
            self.output.update("[red]No hay productos registrados.[/red]")
