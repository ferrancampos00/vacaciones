import tkinter as tk
from login import login_screen  # Importamos la función para la pantalla de login
from admin import mostrar_admin  # Importamos la función para mostrar la pantalla de administración de usuarios
from usuario import elegir_vacaciones  # Importamos la función para la pantalla de solicitud de vacaciones

def iniciar_app():
    # Llamamos a la función de login al iniciar la aplicación
    login_screen()

if __name__ == "__main__":
    iniciar_app()  # Ejecutamos la aplicación llamando a la función principal


