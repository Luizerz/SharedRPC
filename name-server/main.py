import flet as ft
import threading
import Pyro4
import Pyro4.naming

logContainer = ft.Column()
ipInputField = ft.TextField(label="Seu IP")
connectButton = ft.ElevatedButton("Conectar")
debugLogText = ft.Text("Debug log:", size=25, color="white")
logContainer.controls.append(debugLogText)

class NameServer:
    def __init__(self):
        self.ip     = None

    def set_ip(self):
        self.ip = ipInputField.value
        if self.ip:
            self.launch_name_server()
        else:
            logContainer.controls.append(ft.Text("ERRO: ENTRADA VAZIA", color="red"))
            logContainer.update()

    def launch_name_server(self):
        threadNameServer = threading.Thread(
            target=Pyro4.naming.startNSloop, kwargs={"host": self.ip}, daemon=True
        )
        logContainer.controls.append(ft.Text("Servidor de nomes ativo", color="white"))
        logContainer.update()
        threadNameServer.start()

nameServer = NameServer()

def main(page: ft.Page):
    
    page.window.width = 600
    page.window.height = 400
    page.theme = ft.Theme(color_scheme=ft.ColorScheme("purple", secondary="white", tertiary= "white"))
    page.bgcolor = "white"
    
    
    def button_click(e):
        nameServer.set_ip()
        
    connectButton.on_click = button_click

    page.add(ft.Column([
       ft.Row([
           ipInputField,
           connectButton
           ]),
        ft.Container(logContainer, bgcolor=ft.colors.PURPLE_100, width=800, border_radius=5, padding=10)
    ]))

ft.app(main)
