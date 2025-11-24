from textual.screen import Screen
from textual.widgets import Static, Input
from textual.app import ComposeResult
from BdD.basededatos import SessionLocal
from Managers.producto_manager import ProductoManager
from textual import events
from textual.widgets import ListView

class EliminarProductoScreen(Screen):

    BINDINGS = [
        ("escape", "pop_screen", "Atrás")
    ]

    def __init__(self):
        super().__init__()
        self.db = SessionLocal()
        self.manager = ProductoManager(self.db)

    def compose(self) -> ComposeResult:
        yield Static("[b]Eliminar Producto[/b]", classes="titulo")
        yield Static("Ingrese ID del producto a eliminar:", id="mensaje")
        yield Input(placeholder="ID del producto", id="input_delete")
        yield Static("", id="output")

    async def on_mount(self) -> None:
        # poner foco en el input al montar la pantalla
        self.query_one("#input_delete", Input).focus()

    async def action_pop_screen(self) -> None:
        await self.app.pop_screen()
        if self.app.screen_stack:
            parent = self.app.screen_stack[-1]
            try:
                menu = parent.query_one("#menu", ListView)
                menu.focus()
            except Exception:
                pass

    async def on_input_submitted(self, event: Input.Submitted):
        value = event.value.strip()
        event.input.value = ""
        output = self.query_one("#output", Static)

        try:
            producto_id = int(value)
        except ValueError:
            output.update("[red]ID inválido[/red]")
            return

        try:
            eliminado = self.manager.eliminar_producto(producto_id)
            if eliminado:
                output.update("[green]Producto eliminado correctamente[/green]")
            else:
                output.update("[red]Producto no encontrado[/red]")
        except Exception as e:
            output.update(f"[red]Error: {str(e)}[/red]")
