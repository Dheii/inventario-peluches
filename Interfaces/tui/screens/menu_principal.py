from textual.screen import Screen
from textual.widgets import ListView, ListItem, Static
from textual import events

from textual.widgets import Static, ListView, ListItem
from BdD.basededatos import SessionLocal
from Managers.producto_manager import ProductoManager
from .agregar_producto import AgregarProductoScreen
from .listar_productos import ListarProductosScreen
from .actualizar_producto import ActualizarProductoScreen
from .eliminar_producto import EliminarProductoScreen
from .listar_movimientos import ListarMovimientosScreen

class MenuPrincipalScreen(Screen):
    def compose(self):
        opciones = [
            ("Agregar producto", "agregar"),
            ("Listar productos", "listar"),
            ("Actualizar producto", "actualizar"),
            ("Eliminar producto", "eliminar"),
            ("Listar movimientos", "movimientos"),
            ("Salir", "salir")
        ]
        list_items = [ListItem(Static(text), name=_id) for text, _id in opciones]
        yield ListView(*list_items, id="menu")

    def on_list_view_selected(self, event: ListView.Selected):
        screen_id = event.item.name
        if screen_id == "agregar":
            self.app.push_screen(AgregarProductoScreen())
        elif screen_id == "listar":
            self.app.push_screen(ListarProductosScreen())
        elif screen_id == "actualizar":
            self.app.push_screen(ActualizarProductoScreen())
        elif screen_id == "eliminar":
            self.app.push_screen(EliminarProductoScreen())
        elif screen_id == "movimientos":
            self.app.push_screen(ListarMovimientosScreen())
        elif screen_id == "salir":
            self.app.exit()
            
    async def on_mount(self):
    # Al montar, asegurarse de que el ListView tenga foco
        menu = self.query_one("#menu", ListView)
        menu.focus()