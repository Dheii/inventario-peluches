from textual.app import App
from textual.screen import Screen
from .screens.menu_principal import MenuPrincipalScreen

class InventarioApp(App):
    CSS_PATH = None
    TITLE = "Inventario de Peluches"

    def on_mount(self):
        self.push_screen(MenuPrincipalScreen())

if __name__ == "__main__":
    InventarioApp().run()