import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
import os
import sys

def obtener_ruta_archivo():
    # Si el script está corriendo desde un ejecutable, usar la ruta del ejecutable
    if getattr(sys, 'frozen', False):
        ruta = os.path.join(sys._MEIPASS, 'vacaciones.firebase.json')
    else:
        # Si estamos en el entorno de desarrollo, la ruta es relativa al script
        ruta = 'vacaciones.firebase.json'
    return ruta

# Cargar las credenciales de Firebase
def inicializar_firebase():
    archivo_credenciales = obtener_ruta_archivo()
    cred = credentials.Certificate(archivo_credenciales)
    firebase_admin.initialize_app(cred)

# Obtener la referencia de la base de datos Firestore
def obtener_db():
    if not firebase_admin._apps:
        inicializar_firebase()
    db = firestore.client()
    return db

db = obtener_db()

def agregar_festivos():
   
    festivos_ref = db.collection('festivos').stream()
    # Comprobar si ya hay festivos en la base de datos
    if not list(festivos_ref):  # Si la lista de festivos está vacía, significa que no hay festivos en Firestore
        festivos_2025 = [
            datetime(2025, 1, 1),  # Año Nuevo
            datetime(2025, 1, 6),  # Reyes Magos
            datetime(2025, 4, 17),  # Jueves Santo
            datetime(2025, 4, 18),  # Viernes Santo
            datetime(2025, 5, 1),  # Día del Trabajo
            datetime(2025, 8, 15),  # Asunción de la Virgen
            datetime(2025, 10, 12),  # Fiesta Nacional de España
            datetime(2025, 11, 1),  # Todos los Santos
            datetime(2025, 12, 6),  # Día de la Constitución Española
            datetime(2025, 12, 8),  # Inmaculada Concepción
            datetime(2025, 12, 25),  # Navidad
            datetime(2025, 12, 26),  # San Esteban
            datetime(2025, 4, 23),  # Día de Sant Jordi
            datetime(2025, 9, 24),  # La Mercè
        ]
        
        for festivo in festivos_2025:
            try:
                # Crear un nuevo documento en la colección 'festivos'
                db.collection('festivos').add({
                    'fecha': festivo,
                    'descripcion': festivo.strftime("%d-%m-%Y")
                })
                print(f"Festivo añadido: {festivo.strftime('%d-%m-%Y')}")
            except Exception as e:
                print(f"Error al agregar festivo {festivo.strftime('%d-%m-%Y')}: {e}")
    else:
        print("Los festivos ya están en la base de datos.")

# Función para agregar un nuevo usuario a la base de datos
def agregar_usuario(correo, nombre, password):
    
    usuarios_ref = db.collection("usuarios")
    # Comprobamos si ya existe un usuario con el mismo correo
    existing_user = usuarios_ref.where("correo", "==", correo).get()
    if existing_user:
        return False  # El correo ya está registrado
    else:
        # Agregamos el nuevo usuario
        usuarios_ref.add({
            "correo": correo,
            "nombre": nombre,
            "password": password
        })
        return True  # Usuario agregado exitosamente
# Función para verificar si el usuario existe en la base de datos
def verificar_usuario(correo, password):
    usuarios_ref = db.collection("usuarios")
    usuarios = usuarios_ref.where("correo", "==", correo).where("password", "==", password).get()

    if usuarios:
        return True  # El usuario existe y la contraseña es correcta
    return False  # El usuario no existe o la contraseña es incorrecta

# Función para obtener las vacaciones de un usuario por correo
def obtener_vacaciones_usuario(correo=None):
    vacaciones_ref = db.collection("vacaciones")
    if correo:  # Si se pasa un correo, filtra por ese correo
        vacaciones = vacaciones_ref.where("correo", "==", correo).get()
    else:  # Si no se pasa un correo, obtiene todas las vacaciones
        vacaciones = vacaciones_ref.get()

    lista_vacaciones = []

    for vaca in vacaciones:
        vaca_dict = vaca.to_dict()
        vaca_dict["id"] = vaca.id
        vaca_dict["fecha_inicio"] = datetime.fromisoformat(vaca_dict["fecha_inicio"])
        vaca_dict["fecha_fin"] = datetime.fromisoformat(vaca_dict["fecha_fin"])
        lista_vacaciones.append(vaca_dict)

    return lista_vacaciones
    

# Función para guardar vacaciones
def guardar_vacaciones(correo, nombre, fecha_inicio, fecha_fin):
    vacaciones_ref = db.collection("vacaciones")
    
    # Verificar si ya existe un documento similar
    existing_vacaciones = vacaciones_ref.where(
        "correo", "==", correo).where("fecha_inicio", "==", fecha_inicio).where("fecha_fin", "==", fecha_fin).get()
    
    if not existing_vacaciones:
        # Crear un nuevo documento
        doc_data = {
            "correo": correo,
            "nombre": nombre,
            "fecha_inicio": fecha_inicio.isoformat(),  # Convertir las fechas a cadena ISO
            "fecha_fin": fecha_fin.isoformat(),
            "estado": "pendiente",  # Estado inicial
        }
        vacaciones_ref.add(doc_data)  # Añadir el documento
        print(f"Vacaciones de {correo} guardadas correctamente.")
    else:
        print(f"Vacaciones ya existen para {correo}.")

# Función para obtener las vacaciones del usuario

# Función para actualizar el estado de las vacaciones de un usuario
def actualizar_estado_vacaciones(vacacion_id, nuevo_estado):
    vacaciones_ref = db.collection("vacaciones")
    
    # Actualizar el estado de la solicitud de vacaciones
    vacaciones_ref.document(vacacion_id).update({"estado": nuevo_estado})

    print(f"Vacaciones con ID {vacacion_id} actualizadas a estado: {nuevo_estado}")

def borrar_vacaciones_db(vacacion_id):
    # Obtener la referencia a las vacaciones en la base de datos
    vacaciones_ref = db.collection("vacaciones")
    
    # Eliminar la solicitud de vacaciones
    vacaciones_ref.document(vacacion_id).delete()

    