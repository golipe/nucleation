# -*- coding: utf-8 -*-
from interface import ANuClaApp
from controller import Controller
import sys
import os

global AppPath
global NucleationModeSizeLimit

if __name__ == "__main__":
    controller = Controller(os.getcwd())
    # Iniciar una instancia de la aplicación wxWidgets
    app = ANuClaApp(controller)
    # Asignar al controlador la ventana para poder llamar a métodos de actualización de la interfaz
    controller.setView(app)
    # Iniciar el bucle de escucha de eventos de la aplicación
    app.MainLoop()
