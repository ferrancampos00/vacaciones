import tkinter as tk
from tkinter import messagebox
from base_datos import guardar_vacaciones, obtener_vacaciones_usuario, borrar_vacaciones_db,agregar_festivos  # Importamos las funciones necesarias
from datetime import datetime,timedelta
from tkcalendar import DateEntry
from base_datos import db


def obtener_festivos():
    agregar_festivos()
    festivos_ref = db.collection('festivos').stream()
    
    festivos = []
    for festivo in festivos_ref:
        festivos.append(festivo.to_dict()['fecha'].date())  # Obtener solo la fecha
    
    return festivos

# Función para agregar festivos solo si no están creados previamente



def calcular_dias_ocupados(correo_usuario):
    vacaciones = obtener_vacaciones_usuario(correo_usuario)
    dias_ocupados = 0
    # Obtener los festivos desde Firebase
    festivos = obtener_festivos()

    for vaca in vacaciones:
        fecha_inicio = vaca['fecha_inicio']
        fecha_fin = vaca['fecha_fin']
        # Calcular los días naturales ocupados por la solicitud
        # Iterar sobre cada día entre fecha_inicio y fecha_fin
        dia_actual = fecha_inicio
        while dia_actual <= fecha_fin:
            # Si el día no es festivo, contar como día ocupado
            if dia_actual.date() not in festivos:
                dias_ocupados += 1
            dia_actual += timedelta(days=1)  # Avanzar al siguiente día

    return dias_ocupados

def comprobar_fechas_existentes(correo_usuario, fecha_inicio, fecha_fin):
    # Obtener las solicitudes de vacaciones del usuario
    vacaciones = obtener_vacaciones_usuario(correo_usuario)

    # Comprobar si alguna solicitud tiene las mismas fechas
    for vaca in vacaciones:
        vaca_inicio = vaca['fecha_inicio']
        vaca_fin = vaca['fecha_fin']
        if (fecha_inicio <= vaca_fin and fecha_fin >= vaca_inicio):  # Compara si las fechas se solapan
            return True  # Ya existe una solicitud con esas fechas

    return False  # No existe una solicitud con esas fechas

def obtener_nombre_usuario(correo_usuario):
    usuarios_ref = db.collection("usuarios")
    usuario = usuarios_ref.where("correo", "==", correo_usuario).get()
    if usuario:
        return usuario[0].to_dict().get("nombre", "Usuario")
    return "Usuario"

# Función para elegir vacaciones
def elegir_vacaciones(correo_usuario):
    from login import login_screen

    # Obtenemos el nombre del usuario
    nombre_usuario = obtener_nombre_usuario(correo_usuario)

    def guardar_vacaciones_gui():
        
        # Convertir las fechas a datetime.datetime
        fecha_inicio = entry_inicio.get_date()
        fecha_fin = entry_fin.get_date()

        if not (fecha_inicio and fecha_fin):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Convertir las fechas a datetime.datetime con hora 00:00:00
        try:
            fecha_inicio = datetime.combine(fecha_inicio, datetime.min.time())
            fecha_fin = datetime.combine(fecha_fin, datetime.min.time())

            # Comprobamos si las fechas ya están ocupadas por el mismo usuario
            if comprobar_fechas_existentes(correo_usuario, fecha_inicio, fecha_fin):
                messagebox.showerror("Error", "Ya tienes una solicitud entre esas fechas.")
                return

            # Llamamos a la función guardar_vacaciones desde base_datos.py
            guardar_vacaciones(correo_usuario,nombre_usuario,fecha_inicio, fecha_fin)
            messagebox.showinfo("Éxito", "Solicitud guardada correctamente.")  # Mensaje de éxito

            # Actualizar la lista de vacaciones mostradas
            actualizar_lista_vacaciones()

        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al guardar la solicitud: {e}")
        finally:
            limpiar_campos()

    def limpiar_campos():
        today = datetime.today().date()
        entry_inicio.set_date(today)  # Limpiamos el campo de fecha
        entry_fin.set_date(None)  # Limpiamos el campo de fecha

    def actualizar_lista_vacaciones():
    # Limpiar la lista antes de actualizarla
        for widget in frame_vacaciones.winfo_children():
            widget.destroy()  # Destruir los widgets previos

        # Obtener las vacaciones del usuario desde Firebase
        vacaciones = obtener_vacaciones_usuario(correo_usuario)

    # Mostrar las vacaciones en la lista
        for index, vaca in enumerate(vacaciones):
            # Asegurarnos de que 'estado' esté presente en el diccionario
            estado = vaca.get('estado', 'desconocido')  # Valor por defecto 'desconocido'

            # Crear un Frame para cada solicitud
            frame_solicitud = tk.Frame(frame_vacaciones)
            frame_solicitud.grid(row=index, column=0, padx=10, pady=5, sticky="w")

            # Mostrar las fechas y estado en el Frame
            label_solicitud = tk.Label(frame_solicitud, text=f"{vaca['fecha_inicio'].strftime('%d-%m-%Y')} - {vaca['fecha_fin'].strftime('%d-%m-%Y')} | {estado}")
            label_solicitud.grid(row=0, column=0, padx=10)

            # Crear el botón de borrar solo si el estado es 'pendiente' o 'rechazada'
            if estado in ["pendiente", "rechazada"]:
                borrar_btn = tk.Button(frame_solicitud, text="Borrar", command=lambda vaca=vaca: borrar_vacaciones(vaca))
                borrar_btn.grid(row=0, column=1, padx=10)
        # Actualizar la cantidad de días restantes después de cargar las solicitudes
        actualizar_contador_dias()

    def borrar_vacaciones(vaca):
    # Comprobar si el estado es "pendiente" o "rechazada"
        if vaca['estado'] in ["pendiente", "rechazada"]:
            try:
                # Llamamos a la función de borrar desde base_datos.py
                borrar_vacaciones_db(vaca['id'])  # Se asume que cada vaca tiene un id único
                messagebox.showinfo("Éxito", "Solicitud de vacaciones eliminada correctamente.")
                actualizar_lista_vacaciones()
             # Actualizar la lista después de borrar
                actualizar_lista_vacaciones()
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un problema al borrar la solicitud: {e}")
        else:
                messagebox.showerror("Error", "No puedes borrar una solicitud ya aceptada.")

    def actualizar_contador_dias():
        # Calcular los días ocupados
        dias_ocupados = calcular_dias_ocupados(correo_usuario)
        dias_totales = 30  # Puedes cambiar este valor a los días totales disponibles para el usuario
        dias_restantes = dias_totales - dias_ocupados

        # Actualizar la etiqueta con los días restantes
        label_dias_restantes.config(text=f"Días naturales restantes: {dias_restantes}")


    # Crear la ventana de vacaciones
    global ventana_vacaciones
    app_vacaciones = tk.Tk()
    app_vacaciones.title("Gestión de Vacaciones")
    app_vacaciones.geometry("500x400")

 # Crear el marco para el formulario de selección de fechas
    frame_formulario = tk.Frame(app_vacaciones, padx=20, pady=10, bd=2, relief="solid", borderwidth=2)
    frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Crear los widgets dentro del primer marco
    tk.Label(frame_formulario, text=f"Usuario: {nombre_usuario}", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame_formulario, text="Fecha Inicio:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_inicio = DateEntry(frame_formulario, width=12, background='darkblue', foreground='white', borderwidth=2)
    entry_inicio.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame_formulario, text="Fecha Fin:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_fin = DateEntry(frame_formulario, width=12, background='darkblue', foreground='white', borderwidth=2)
    entry_fin.grid(row=2, column=1, padx=10, pady=5)

    btn_guardar = tk.Button(frame_formulario, text="Guardar", command=guardar_vacaciones_gui)
    btn_guardar.grid(row=3, column=0, columnspan=2, pady=10)

    # Crear el marco para mostrar las solicitudes de vacaciones
    frame_vacaciones = tk.Frame(app_vacaciones, padx=20, pady=10, bd=2, relief="solid", borderwidth=2)
    frame_vacaciones.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Etiqueta para mostrar los días restantes
    label_dias_restantes = tk.Label(app_vacaciones, text="Días naturales restantes: 30")
    label_dias_restantes.grid(row=2, column=0, columnspan=2, pady=10)

    # Listbox para mostrar las solicitudes de vacaciones
    actualizar_lista_vacaciones()

    # Cargar las vacaciones al inicio
    actualizar_lista_vacaciones()

    def retroceder_inicio():
    # Mostrar un cuadro de confirmación para cerrar sesión
        respuesta = messagebox.askyesno("Cerrar sesión", "¿Estás seguro de que quieres cerrar sesión?")

        if respuesta:  # Si el usuario elige "Sí"
            app_vacaciones.destroy()  # Cierra la ventana actual
            login_screen()  # Llama a la función para mostrar la pantalla de login
        else:
            return  # Si el usuario elige "No", no hace nada y sigue en la misma pantalla
     # Botón para retroceder
    retroceder_btn = tk.Button(app_vacaciones, text="Retroceder", command=retroceder_inicio)
    retroceder_btn.grid(row=6, column=0, columnspan=2, pady=10)


    
        
    app_vacaciones.mainloop()

