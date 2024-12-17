import tkinter as tk
from tkinter import messagebox
from base_datos import agregar_usuario, obtener_vacaciones_usuario, actualizar_estado_vacaciones  # Importamos las funciones necesarias

# Función para agregar un nuevo usuario (solo admin)
def agregar_usuario_gui():
           
    def agregar_usuario_bd():
        correo = entry_correo_usuario.get()  # Obtenemos el nombre de usuario desde el campo de texto
        nombre = entry_nombre_usuario.get()
        password = entry_password_usuario.get()  # Obtenemos la contraseña desde el campo de texto

        if not (correo.endswith("@gmail.com") or correo.endswith("@aradoxa.com")):
            messagebox.showerror("Error", "El correo debe ser @gmail.com o @aradoxa.com.")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres.")
            return

        # Verificamos que ambos campos estén llenos
        if correo and nombre and password:
        
            agregar_usuario(correo, nombre, password)  # Llamamos a la función para agregar el usuario en la base de datos
            messagebox.showinfo("Éxito", "Usuario agregado correctamente.")  # Mostramos un mensaje de éxito
            ventana_agregar.destroy()  # Cerramos la ventana
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")  # Mostramos error si falta algún campo

    # Creamos la ventana para agregar un usuario
    ventana_agregar = tk.Tk()
    ventana_agregar.title("Agregar Usuario")  # Título de la ventana
    ventana_agregar.geometry("500x400")  # Tamaño de la ventana

    # Campo para introducir el nombre del nuevo usuario
    tk.Label(ventana_agregar, text="Correo Usuario:").pack(pady=5)
    entry_correo_usuario = tk.Entry(ventana_agregar)
    entry_correo_usuario.pack(pady=5)

    tk.Label(ventana_agregar, text="Usuario:").pack(pady=5)
    entry_nombre_usuario = tk.Entry(ventana_agregar)
    entry_nombre_usuario.pack(pady=5)

    # Campo para introducir la contraseña del nuevo usuario
    tk.Label(ventana_agregar, text="Contraseña:").pack(pady=5)
    entry_password_usuario = tk.Entry(ventana_agregar, show="*") 
    entry_password_usuario.pack(pady=5)
    

    # Botón para agregar el usuario
    btn_agregar = tk.Button(ventana_agregar, text="Agregar Usuario", command=agregar_usuario_bd)
    btn_agregar.pack(pady=10)

    def retroceder_admin():
        ventana_agregar.destroy()
        mostrar_admin()
     # Botón para retroceder
    retroceder_btn = tk.Button(ventana_agregar, text="Retroceder", command=retroceder_admin)
    retroceder_btn.pack(pady=10)  
    
    ventana_agregar.mainloop()  # Iniciamos el bucle principal de la ventana

# Función para aceptar o rechazar vacaciones
def gestionar_vacaciones():
    
    def aceptar_vacaciones(vacacion_id):
        try:
            # Actualizamos el estado de las vacaciones a "aceptada"
            actualizar_estado_vacaciones(vacacion_id, "aceptada")
            messagebox.showinfo("Éxito", "Vacaciones aceptadas.")
            ventana_vacaciones.destroy()  # Destruimos la ventana actua
            mostrar_vacaciones()  # Refrescar la lista de solicitudes de vacaciones
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al aceptar las vacaciones: {e}")

    def rechazar_vacaciones(vacacion_id):
        try:
            # Actualizamos el estado de las vacaciones a "rechazada"
            actualizar_estado_vacaciones(vacacion_id, "rechazada")
            messagebox.showinfo("Éxito", "Vacaciones rechazadas.")
            ventana_vacaciones.destroy()  # Destruimos la ventana actua
            mostrar_vacaciones()  # Refrescar la lista de solicitudes de vacaciones
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al rechazar las vacaciones: {e}")

    def mostrar_vacaciones():
       
        from admin import mostrar_admin
        # Crear ventana para gestionar vacaciones 
        global ventana_vacaciones  
        ventana_vacaciones = tk.Tk()
        ventana_vacaciones.title("Gestionar Vacaciones")  # Título de la ventana
        ventana_vacaciones.geometry("500x400")  # Tamaño de la ventana

        # Obtener las solicitudes de vacaciones de la base de datos
        solicitudes = obtener_vacaciones_usuario()  # Obtener todas las solicitudes de vacaciones

        # Mostrar las solicitudes en la ventana
        for vaca in solicitudes:
            vacacion_id = vaca['id']  # Obtener el ID de la solicitud de vacaciones
            correo_usuario = vaca['correo']
            fecha_inicio = vaca['fecha_inicio'].strftime('%d-%m-%Y')
            fecha_fin = vaca['fecha_fin'].strftime('%d-%m-%Y')
            estado = vaca['estado']

            # Mostrar cada solicitud con los botones para aceptar/rechazar
            solicitud_texto = f"{correo_usuario} | {fecha_inicio} - {fecha_fin} | Estado: {estado}"
            tk.Label(ventana_vacaciones, text=solicitud_texto).pack(pady=5)

            # Botones para aceptar o rechazar
            if estado == 'pendiente':
                tk.Button(ventana_vacaciones, text="Aceptar", command=lambda id=vacacion_id: aceptar_vacaciones(id)).pack(pady=5)
                tk.Button(ventana_vacaciones, text="Rechazar", command=lambda id=vacacion_id: rechazar_vacaciones(id)).pack(pady=5)

        def retroceder_admin():
            ventana_vacaciones.destroy()
            mostrar_admin()
        # Botón para retroceder
        retroceder_btn = tk.Button(ventana_vacaciones, text="Retroceder", command=retroceder_admin)
        retroceder_btn.pack(pady=10)   

        ventana_vacaciones.mainloop()  # Iniciamos el bucle principal de la ventana

    mostrar_vacaciones()  # Llamar a la función que muestra las vacaciones


# Función para mostrar la pantalla de administración de usuarios y vacaciones (solo admin)
def mostrar_admin():
    ventana_admin = tk.Tk()
    ventana_admin.title("Administrar Usuarios y Vacaciones")  # Título de la ventana
    ventana_admin.geometry("500x400")  # Tamaño de la ventana

    # Bienvenida al administrador
    tk.Label(ventana_admin, text="Bienvenido Admin").pack(pady=10)

    # Botón para agregar un nuevo usuario
    def avanzar_pantalla():
        ventana_admin.destroy()
        agregar_usuario_gui()
        
    
    btn_agregar = tk.Button(ventana_admin, text="Agregar Usuario", command=avanzar_pantalla)
    btn_agregar.pack(pady=10)

    def avanzar_pantalla2():
        ventana_admin.destroy()
        gestionar_vacaciones()
       

    # Botón para gestionar solicitudes de vacaciones
    btn_vacaciones = tk.Button(ventana_admin, text="Gestionar Vacaciones", command=avanzar_pantalla2)
    btn_vacaciones.pack(pady=10)


    from login import login_screen
    def retroceder_inicio():
    # Mostrar un cuadro de confirmación para cerrar sesión
        respuesta = messagebox.askyesno("Cerrar sesión", "¿Estás seguro de que quieres cerrar sesión?")

        if respuesta:  # Si el usuario elige "Sí"
            ventana_admin.destroy()  # Cierra la ventana actual
            login_screen()  # Llama a la función para mostrar la pantalla de login
        else:
            return  # Si el usuario elige "No", no hace nada y sigue en la misma pantalla
     # Botón para retroceder

    retroceder_btn = tk.Button(ventana_admin, text="Retroceder", command=retroceder_inicio)
    retroceder_btn.pack(pady=10)

    ventana_admin.mainloop()  # Iniciamos el bucle principal de la ventana

if __name__ == "__main__":
    mostrar_admin()  # Ejecutamos la función que muestra la pantalla de administración

