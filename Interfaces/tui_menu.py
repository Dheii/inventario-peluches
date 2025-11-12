from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static, Input
from textual.reactive import reactive
from BdD.basededatos import SessionLocal
from Managers.producto_manager import ProductoManager
from Modelos.modelos import Producto, MovimientoInventario
from datetime import datetime

class Inventario(App):
    CSS_PATH = None
    menu_state = reactive("main")
    temp_data = reactive({})

    def __init__(self):
        super().__init__()
        self.db = SessionLocal()
        self.manager = ProductoManager(self.db)
        self.temp_data = {}

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Static("\n[bold orange]INVENTARIO DE PELUCHES[/bold orange]\n", classes="titulo"),
            Static("", id="output"),
            Input(placeholder="Ingresa tu opción (0 para ir Atrás)...", id="entrada"),
        )
        

    async def on_mount(self):
        self.mostrar_menu_principal()

    def mostrar_menu_principal(self):
        output = self.query_one("#output", Static)
        output.update(
            "\n[bold]MENÚ PRINCIPAL[/bold]\n"
            "[bold]1.[/bold] Agregar producto\n"
            "[bold]2.[/bold] Listar productos\n"
            "[bold]3.[/bold] Actualizar producto\n"
            "[bold]4.[/bold] Eliminar producto\n"
            "[bold]5.[/bold] Listar movimientos\n"
            "[bold]6.[/bold] Salir"
        )
        self.menu_state = "main"

    def mostrar_menu_actualizacion(self):
        output = self.query_one("#output", Static)
        output.update(
            "\n[bold cyan]MENÚ ACTUALIZACIÓN[/bold cyan]\n"
            "[bold cyan]1.[/bold cyan] Actualizar nombre\n"
            "[bold cyan]2.[/bold cyan] Actualizar precio\n"
            "[bold cyan]3.[/bold cyan] Actualizar categoría\n"
            "[bold cyan]4.[/bold cyan] Actualizar tamaño\n"
            "[bold cyan]5.[/bold cyan] Actualizar cantidad (stock)\n"
            "[bold cyan]0.[/bold cyan] Atrás"
        )
        self.menu_state = "sub_actualizar"
        self.temp_data = {}

    async def on_input_submitted(self, event: Input.Submitted):
        entrada = event.value.strip()
        event.input.value = ""

        if entrada == "0":
            if self.menu_state.startswith("main"):
                return
            self.mostrar_menu_principal()
            self.temp_data = {}
            return

        # Ruteo según estado
        if self.menu_state.startswith("main"):
            await self.ejecutar_opcion_principal(entrada)
        elif self.menu_state.startswith("sub_actualizar"):
            await self.proceso_actualizar_flujo(entrada)
        elif self.menu_state.startswith("agregar"):
            await self.proceso_agregar(entrada)
        elif self.menu_state == "eliminar":
            await self.proceso_eliminar(entrada)

    async def ejecutar_opcion_principal(self, opcion: str):
        output = self.query_one("#output", Static)
        try:
            if opcion == "1":
                output.update("[bold yellow]Agregar producto[/bold yellow]\nIngrese nombre:")
                self.menu_state = "agregar_nombre"
            elif opcion == "2":
                productos = self.manager.listar_productos()
                if productos:
                    texto = "\n".join(
                        f"ID {p.id_peluche} | {p.nombre} ({p.categoria}, {p.tamano}) - "
                        f"{p.cantidad_stock} unidades, {p.precio_unitario} Bs"
                        for p in productos
                    )
                    output.update("[bold green]Productos en inventario:[/bold green]\n" + texto + "\n\n0 para ir Atrás")
                    self.menu_state = "listar_productos"
                else:
                    output.update("[bold red]No hay productos registrados.[/bold red]")
            elif opcion == "3":
                self.mostrar_menu_actualizacion()
            elif opcion == "4":
                output.update("[bold red]Eliminar producto[/bold red]\nIngrese ID del producto (0 para ir Atrás):")
                self.menu_state = "eliminar"
            elif opcion == "5":
                movimientos = (
                    self.db.query(MovimientoInventario, Producto)
                    .join(Producto, MovimientoInventario.producto_id == Producto.id_peluche)
                    .order_by(MovimientoInventario.fecha)
                    .all()
                )
                if movimientos:
                    texto = "\n".join(
                        f"ID {mov.id_movimiento} | {prod.nombre} | {mov.tipo} | {mov.cantidad} | {mov.fecha}"
                        for mov, prod in movimientos
                    )
                    output.update("[bold magenta]Movimientos de inventario:[/bold magenta]\n" + texto + "\n\n0 para ir Atrás")
                    self.menu_state = "listar_movimientos"
                else:
                    output.update("[bold yellow]No hay movimientos registrados.[/bold yellow]")
            elif opcion == "6":
                output.update("[bold red]Saliendo...[/bold red]")
                await self.action_quit()
            else:
                output.update("[bold red]Opción inválida.[/bold red]")
        except Exception as e:
            output.update(f"[bold red]Error: {e}[/bold red]")

    async def proceso_agregar(self, entrada: str):
        output = self.query_one("#output", Static)
        try:
            if self.menu_state == "agregar_nombre":
                self.temp_data["nombre"] = entrada
                output.update("Categoría del producto (0 para ir Atrás):")
                self.menu_state = "agregar_categoria"
            elif self.menu_state == "agregar_categoria":
                self.temp_data["categoria"] = entrada
                output.update("Tamaño del producto (0 para irAtrás):")
                self.menu_state = "agregar_tamano"
            elif self.menu_state == "agregar_tamano":
                self.temp_data["tamano"] = entrada
                output.update("Cantidad inicial (0 para ir Atrás):")
                self.menu_state = "agregar_cantidad"
            elif self.menu_state == "agregar_cantidad":
                self.temp_data["cantidad"] = int(entrada)
                output.update("Precio unitario (Bs) (0 para ir Atrás):")
                self.menu_state = "agregar_precio"
            elif self.menu_state == "agregar_precio":
                self.temp_data["precio"] = float(entrada)
                producto = self.manager.agregar_producto(
                    self.temp_data["nombre"],
                    self.temp_data["categoria"],
                    self.temp_data["tamano"],
                    self.temp_data["precio"],
                    self.temp_data["cantidad"]
                )
                output.update(f"[green]Producto '{producto.nombre}' agregado con ID {producto.id_peluche}[/green]")
                self.mostrar_menu_principal()
        except Exception as e:
            output.update(f"[red]Error: {e}[/red]")

    async def proceso_eliminar(self, entrada: str):
        output = self.query_one("#output", Static)
        try:
            id_peluche = int(entrada)
            if self.manager.eliminar_producto(id_peluche):
                output.update(f"[green]Producto eliminado.[/green]")
            else:
                output.update(f"[red]Producto no encontrado.[/red]")
            self.mostrar_menu_principal()
        except Exception as e:
            output.update(f"[red]Error: {e}[/red]")

    async def proceso_actualizar_flujo(self, entrada: str):
        output = self.query_one("#output", Static)

        if "update_step" not in self.temp_data:
            opciones = {
                "1": "nombre",
                "2": "precio unitario",
                "3": "categoria",
                "4": "tamano",
                "5": "cantidad_stock"
            }
            campo = opciones.get(entrada)
            if not campo:
                output.update("[red]Opción inválida.[/red]")
                self.mostrar_menu_actualizacion()
                return
            self.temp_data["campo"] = campo
            self.temp_data["update_step"] = "awaiting_id"
            output.update("Introduce el ID del producto a actualizar (0 para ir Atrás):")
            return

        if self.temp_data["update_step"] == "awaiting_id":
            try:
                self.temp_data["id_p"] = int(entrada)
                self.temp_data["update_step"] = "awaiting_value"
                campo = self.temp_data["campo"]
                if campo == "cantidad_stock":
                    output.update("Introduce la cantidad a actualizar (0 para ir Atrás):")
                else:
                    output.update(f"Introduce el nuevo valor para {campo} (0 para ir Atrás):")
            except ValueError:
                output.update("[red]ID inválido.[/red]")
            return

        if self.temp_data["update_step"] == "awaiting_value":
            campo = self.temp_data["campo"]
            id_p = self.temp_data["id_p"]
            try:
                if campo == "precio_unitario":
                    nuevo_valor = float(entrada)
                    producto = self.manager.actualizar_precio(id_p, nuevo_valor)
                elif campo == "cantidad_stock":
                    cantidad = int(entrada)
                    self.temp_data["cantidad"] = cantidad
                    self.temp_data["update_step"] = "awaiting_tipo"
                    output.update("Tipo de movimiento: 'entrada' o 'salida' (0 para ir Atrás):")
                    return
                elif campo == "nombre":
                    producto = self.manager.actualizar_nombre(id_p, entrada)
                elif campo == "categoria":
                    producto = self.manager.actualizar_categoria(id_p, entrada)
                elif campo == "tamano":
                    producto = self.manager.actualizar_tamano(id_p, entrada)
                else:
                    raise ValueError("Campo desconocido")
                output.update(f"[green]{campo} actualizado correctamente.[/green]")
                self.temp_data = {}
                self.mostrar_menu_principal()
            except Exception as e:
                output.update(f"[red]Error: {e}[/red]")
                self.temp_data = {}
                self.mostrar_menu_actualizacion()
            return

        if self.temp_data["update_step"] == "awaiting_tipo":
            tipo = entrada.strip().lower()
            if tipo not in ("entrada", "salida"):
                output.update("[red]Tipo inválido. Debe ser 'entrada' o 'salida'.[/red]")
                return
            id_p = self.temp_data["id_p"]
            cantidad = self.temp_data["cantidad"]
            try:
                producto = self.manager.actualizar_stock(id_p, cantidad, tipo)
                output.update(f"[green]Stock actualizado: {producto.cantidad_stock} unidades[/green]")
            except Exception as e:
                output.update(f"[red]Error: {e}[/red]")
            self.temp_data = {}
            self.mostrar_menu_principal()

    async def action_quit(self):
        self.db.close()
        await super().action_quit()

if __name__ == "__main__":
    Inventario().run()
