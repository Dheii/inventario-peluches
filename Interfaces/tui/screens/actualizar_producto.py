from textual.screen import Screen
from textual.widgets import Static, ListView, ListItem, Input
from textual.reactive import reactive
from textual.app import ComposeResult
from textual import events
from BdD.basededatos import SessionLocal
from Managers.producto_manager import ProductoManager

class ActualizarProductoScreen(Screen):

    BINDINGS = [("escape", "pop_screen", "Atrás")]

    def __init__(self):
        super().__init__()
        self.db = SessionLocal()
        self.manager = ProductoManager(self.db)

        self.opciones = [
            ("Actualizar nombre", "nombre"),
            ("Actualizar precio", "precio"),
            ("Actualizar categoría", "categoria"),
            ("Actualizar tamaño", "tamano"),
            ("Actualizar cantidad (entrada/salida)", "cantidad"),
        ]

        self.current_step = reactive(None)
        self.selected_option = None
        self.product_id = None
        self.cantidad = None

    def compose(self) -> ComposeResult:
        yield Static("[b]Actualizar Producto[/b]")
        items = [ListItem(Static(text), id=_id) for text, _id in self.opciones]
        yield ListView(*items, id="menu")
        yield Static("", id="mensaje")

        input_widget = Input(placeholder="")
        input_widget.id = "input_update"
        input_widget.styles.display = "none"
        yield input_widget

    async def on_key(self, event: events.Key):
        if event.key == "escape":
            self.app.pop_screen()
            main_menu_screen = self.app.screen_stack[-1]
            menu_list = main_menu_screen.query_one("#menu", ListView) 
            menu_list.focus() 
            return

    async def on_list_view_selected(self, event: ListView.Selected):
        self.selected_option = event.item.id
        self.current_step = "id"

        input_widget = self.query_one("#input_update", Input)
        input_widget.placeholder = "Introduce ID del producto"
        input_widget.value = ""
        input_widget.styles.display = "block"
        input_widget.focus()

        self.query_one("#mensaje", Static).update("")

    async def on_input_submitted(self, message: Input.Submitted):
        value = message.value.strip()
        input_widget = self.query_one("#input_update", Input)

        if self.current_step == "id":
            try:
                self.product_id = int(value)
            except ValueError:
                self.query_one("#mensaje", Static).update("[red]ID inválido[/red]")
                input_widget.value = ""
                input_widget.focus()
                return

            if self.selected_option == "cantidad":
                self.current_step = "cantidad_valor"
                input_widget.placeholder = "Cantidad"
            else:
                self.current_step = "nuevo_valor"
                input_widget.placeholder = "Nuevo Dato"

            input_widget.value = ""
            input_widget.focus()
            return

        if self.current_step == "nuevo_valor":
            try:
                if self.selected_option == "nombre":
                    self.manager.actualizar_nombre(self.product_id, value)
                elif self.selected_option == "precio":
                    self.manager.actualizar_precio(self.product_id, float(value))
                elif self.selected_option == "categoria":
                    self.manager.actualizar_categoria(self.product_id, value)
                elif self.selected_option == "tamano":
                    self.manager.actualizar_tamano(self.product_id, value)

                self.query_one("#mensaje", Static).update("[green]Valor actualizado[/green]")

            except Exception as e:
                self.query_one("#mensaje", Static).update(f"[red]Error: {str(e)}[/red]")

            input_widget.styles.display = "none"
            self.current_step = None
            self.query_one("#menu", ListView).focus()
            return

        if self.current_step == "cantidad_valor":
            try:
                self.cantidad = int(value)
            except ValueError:
                self.query_one("#mensaje", Static).update("[red]Cantidad inválida[/red]")
                input_widget.value = ""
                input_widget.focus()
                return

            self.current_step = "cantidad_tipo"
            input_widget.placeholder = "Tipo (entrada / salida)"
            input_widget.value = ""
            input_widget.focus()
            return

        if self.current_step == "cantidad_tipo":
            tipo = value.lower()

            if tipo not in ["entrada", "salida"]:
                self.query_one("#mensaje", Static).update("[red]Tipo inválido[/red]")
                input_widget.value = ""
                input_widget.focus()
                return

            producto = self.manager.actualizar_stock(self.product_id, self.cantidad, tipo)
            self.query_one("#mensaje", Static).update(
                f"[green]Stock actualizado: {producto.cantidad_stock}[/green]"
            )

            input_widget.styles.display = "none"
            self.current_step = None
            self.query_one("#menu", ListView).focus()
