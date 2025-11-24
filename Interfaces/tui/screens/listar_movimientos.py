from textual.screen import Screen
from textual.widgets import Static
from BdD.basededatos import SessionLocal
from Managers.producto_manager import ProductoManager
from Modelos.modelos import MovimientoInventario, Producto


class ListarMovimientosScreen(Screen):

    BINDINGS = [
        ("escape", "go_back", "Atrás")
    ]

    def action_go_back(self):
        self.app.pop_screen()

    def on_mount(self):
        self.db = SessionLocal()

        self.output = Static("", id="output")
        self.mount(self.output)

        self.show_movimientos()

    def show_movimientos(self):
        resultados = (
            self.db.query(MovimientoInventario, Producto)
            .join(Producto, MovimientoInventario.producto_id == Producto.id_peluche)
            .order_by(MovimientoInventario.fecha)
            .all()
        )

        if resultados:
            texto = "\n".join(
                f"ID {mov.id_movimiento} | Producto: {prod.nombre} | "
                f"Tipo: {mov.tipo} | Cantidad: {mov.cantidad} | Fecha: {mov.fecha}"
                for mov, prod in resultados
            )
            self.output.update(texto)
        else:
            self.output.update("[yellow]No hay movimientos registrados[/yellow]")
