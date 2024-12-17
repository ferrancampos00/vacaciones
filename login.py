import tkinter as tk
from tkinter import messagebox
from base_datos import verificar_usuario  # Importamos la función para verificar usuarios en la base de datos
from admin import mostrar_admin  # Importamos la función para mostrar la interfaz de admin
from usuario import elegir_vacaciones  # Importamos la función para mostrar la interfaz del usuario

# Función principal de la pantalla de login
def login_screen():
    global correo_usuario
    global admin_logged_in

    # Función que verifica si los datos de login son correctos
    def verificar_login():
        correo = entry_correo.get()  # Obtenemos el correo del usuario desde el campo de texto
        password = entry_password.get()  # Obtenemos la contraseña

        # Comprobamos si el usuario es 'admin'
        if correo == "admin" and password == "admin":
            admin_logged_in = True  # Indicamos que el admin ha iniciado sesión
            messagebox.showinfo("Éxito", "Inicio de sesión como admin.")  # Mostramos un mensaje
            # Cerramos la ventana de login
            ventana_login.destroy()
            mostrar_admin() 
            
        else:
            # Si no es admin, verificamos en la base de datos si el correo y la contraseña son correctos
            if verificar_usuario(correo, password):
                admin_logged_in = False  # Indicamos que el usuario ha iniciado sesión como usuario normal
                correo_usuario = correo  # Guardamos el correo del usuario
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")  # Mostramos mensaje de éxito
                # Cerramos la ventana de login
                ventana_login.destroy()
                elegir_vacaciones(correo)  # Mostramos la pantalla de vacaciones para el usuario
            else:
                messagebox.showerror("Error", "Correo o contraseña incorrectos.")  # Error si no existe el usuario

    # Creamos la ventana de login
    ventana_login = tk.Tk()
    ventana_login.title("Iniciar sesión")  # Título de la ventana
    ventana_login.geometry("500x400")  # Tamaño de la ventana

    # Campo para introducir el correo
    tk.Label(ventana_login, text="Correo:").pack(pady=5)
    entry_correo = tk.Entry(ventana_login)
    entry_correo.pack(pady=5)

    # Campo para introducir la contraseña
    tk.Label(ventana_login, text="Contraseña:").pack(pady=5)
    entry_password = tk.Entry(ventana_login, show="*")  # Contraseña oculta
    entry_password.pack(pady=5)

    # Botón para iniciar sesión
    btn_login = tk.Button(ventana_login, text="Iniciar sesión", command=verificar_login)
    btn_login.pack(pady=10)

    ventana_login.mainloop()  # Iniciamos el bucle principal de la ventana

if __name__ == "__main__":
    login_screen()  # Ejecutamos la función de login al iniciar el script
