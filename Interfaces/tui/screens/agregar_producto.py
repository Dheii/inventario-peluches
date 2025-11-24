from textual.screen import Screen
from textual.widgets import Static, Input
from BdD.basededatos import SessionLocal
from Managers.producto_manager import ProductoManager

class AgregarProductoScreen(Screen):

    BINDINGS = [
        ("escape", "go_back", "Atrás")
    ]

    def action_go_back(self):
        self.app.pop_screen()

    def on_mount(self):
        self.db = SessionLocal()
        self.manager = ProductoManager(self.db)

        self.data = {}
        self.step = 0

        self.mensajes = [
            "Nombre",
            "Categoría",
            "Tamaño",
            "Cantidad inicial",
            "Precio unitario"
        ]

        self.output = Static("", id="output")
        self.input = Input(placeholder="Escribe aquí", id="input")

        self.mount(self.output)
        self.mount(self.input)

        self.input.focus()
        self.show_prompt()

    def show_prompt(self):
        self.output.update(f"Ingrese {self.mensajes[self.step]}:")

    async def on_input_submitted(self, event: Input.Submitted):
        value = event.value.strip()
        event.input.value = ""

        # Validar por paso
        try:
            if self.step == 3:   # Cantidad
                self.data[self.mensajes[self.step]] = int(value)
            elif self.step == 4: # Precio
                self.data[self.mensajes[self.step]] = float(value)
            else:
                if not value:
                    self.output.update("[red]Este campo no puede estar vacío[/red]")
                    return
                self.data[self.mensajes[self.step]] = value
        except:
            self.output.update("[red]Valor inválido, intente nuevamente[/red]")
            return

        # Pasar al siguiente
        self.step += 1

        # Si terminó todo → guardar
        if self.step >= len(self.mensajes):

            producto = self.manager.agregar_producto(
                self.data["Nombre"],
                self.data["Categoría"],
                self.data["Tamaño"],
                self.data["Precio unitario"],
                self.data["Cantidad inicial"]
            )

            self.output.update(
                f"[green]Producto agregado: '{producto.nombre}' "
                f"(ID {producto.id_peluche})[/green]"
            )

            # Preparar para agregar otro
            self.data = {}
            self.step = 0
            self.show_prompt()
            return

        # Mostrar siguiente mensaje
        self.show_prompt()

    def on_show(self):
        """Asegura que el input reciba foco al regresar a la pantalla."""
        self.input.focus()
