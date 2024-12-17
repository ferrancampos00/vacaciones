import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Inicialización de Firebase
cred = credentials.Certificate("vacaciones.firebase.json")  # Cambia la ruta si es necesario
firebase_admin.initialize_app(cred)

# Obtener la referencia a Firestore
db = firestore.client()


# Crear una colección inicial de 'vacaciones' (si no existe)
def crear_base():
    doc_ref = db.collection('vacaciones').document('vacaciones_inicial')
    doc_ref.set({
        'ejemplo': 'Esto es un documento de prueba'
    })
    print("Base de datos creada correctamente.")

# Ejecutar la creación
if __name__ == "__main__":
    crear_base()
