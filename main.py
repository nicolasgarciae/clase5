
# ============================================================
# Ejecutar:
#   uvicorn main:app --host 0.0.0.0 --port 8001 --reload
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import asyncio

app = FastAPI(
    title="Sistema de Citas Médicas",
    description="Sistema completo con todos los microservicios integrados",
    version="1.0"
)

# ============================================================
#  CONFIGURACIÓN DE BASE DE DATOS
# ============================================================
DB_CONFIG = {
    "host": "172.20.87.41",
    "user": "clase",
    "password": "1234",
    "database": "citas_medicas"
}

def get_connection():
    """Crea y retorna una conexión a la base de datos"""
    return mysql.connector.connect(**DB_CONFIG, autocommit=True)


# ============================================================
# MODELOS DE DATOS
# ============================================================

class PacienteRequest(BaseModel):
    nombre: str
    email: str

class CitaRequest(BaseModel):
    paciente_id: int
    fecha: str  # Formato: "2025-06-15 10:00:00"

class ReservaRequest(BaseModel):
    paciente_id: int
    fecha: str


# ============================================================
# RUTA RAÍZ
# ============================================================

@app.get("/")
def root():
    return {
        "sistema": "Citas Médicas",
        "status": "activo",
        "endpoints_disponibles": {
            "POST   /pacientes":           "Registrar nuevo paciente",
            "GET    /pacientes":           "Listar todos los pacientes",
            "GET    /pacientes/{id}":      "Consultar paciente por ID",
            "POST   /citas":               "Crear una cita",
            "GET    /citas":               "Listar todas las citas",
            "GET    /citas/{paciente_id}": "Consultar citas de un paciente",
            "DELETE /citas/{id}":          "Cancelar una cita",
            "POST   /reservar-cita":       "Gateway: reservar cita completa",
            "GET    /test-db":             "Verificar conexión a la BD",
        }
    }


# ============================================================
# TEST DE BASE DE DATOS
# ============================================================

@app.get("/test-db")
def test_db():
    """Verifica que la conexión a la base de datos funciona"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pacientes")
        total_pacientes = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM citas")
        total_citas = cursor.fetchone()[0]
        conn.close()
        return {
            "status": "Conexion exitosa",
            "total_pacientes": total_pacientes,
            "total_citas": total_citas
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexion: {str(e)}")


# ============================================================
# MICROSERVICIO 1 - REGISTRO DE PACIENTES
# ============================================================

@app.post("/pacientes")
def crear_paciente(paciente: PacienteRequest):
    """Registra un nuevo paciente en la base de datos"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pacientes (nombre, email) VALUES (%s, %s)",
            (paciente.nombre, paciente.email)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        conn.close()
        return {
            "mensaje": "Paciente registrado exitosamente",
            "id": nuevo_id,
            "nombre": paciente.nombre,
            "email": paciente.email
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pacientes")
def listar_pacientes():
    """Lista todos los pacientes registrados"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pacientes")
        pacientes = cursor.fetchall()
        conn.close()
        return {"total": len(pacientes), "pacientes": pacientes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# MICROSERVICIO 2 - CONSULTA DE PACIENTES
# ============================================================

@app.get("/pacientes/{id}")
def obtener_paciente(id: int):
    """Consulta un paciente por su ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pacientes WHERE id = %s", (id,))
        paciente = cursor.fetchone()
        conn.close()

        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        return paciente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# MICROSERVICIO 3 - CREAR CITAS
# ============================================================

@app.post("/citas")
async def crear_cita(cita: CitaRequest):
    """Crea una nueva cita. Verifica primero que el paciente exista."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        
        cursor.execute("SELECT * FROM pacientes WHERE id = %s", (cita.paciente_id,))
        paciente = cursor.fetchone()

        if not paciente:
            conn.close()
            raise HTTPException(status_code=404, detail="Paciente no existe")

        
        await asyncio.sleep(2)

        
        cursor2 = conn.cursor()
        cursor2.execute(
            "INSERT INTO citas (paciente_id, fecha, estado) VALUES (%s, %s, 'activa')",
            (cita.paciente_id, cita.fecha)
        )
        conn.commit()
        nuevo_id = cursor2.lastrowid
        conn.close()

        return {
            "mensaje": "Cita creada exitosamente",
            "id": nuevo_id,
            "paciente_id": cita.paciente_id,
            "paciente_nombre": paciente["nombre"],
            "fecha": cita.fecha,
            "estado": "activa"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# MICROSERVICIO 4 - CONSULTAR CITAS
# ============================================================

@app.get("/citas/{paciente_id}")
def listar_citas(paciente_id: int):
    """Lista todas las citas de un paciente"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        
        cursor.execute("SELECT nombre FROM pacientes WHERE id = %s", (paciente_id,))
        paciente = cursor.fetchone()
        if not paciente:
            conn.close()
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

       
        cursor.execute(
            "SELECT * FROM citas WHERE paciente_id = %s ORDER BY fecha",
            (paciente_id,)
        )
        citas = cursor.fetchall()
        conn.close()

        return {
            "paciente_id": paciente_id,
            "paciente_nombre": paciente["nombre"],
            "total_citas": len(citas),
            "citas": citas if citas else []
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/citas")
def listar_todas_citas():
    """Lista todas las citas del sistema con nombre del paciente"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id, c.paciente_id, p.nombre AS paciente_nombre,
                   c.fecha, c.estado
            FROM citas c
            JOIN pacientes p ON c.paciente_id = p.id
            ORDER BY c.fecha
        """)
        citas = cursor.fetchall()
        conn.close()
        return {"total": len(citas), "citas": citas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# MICROSERVICIO 5 - CANCELAR CITAS
# ============================================================

@app.delete("/citas/{id}")
def cancelar_cita(id: int):
    """Cancela una cita por su ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        
        cursor.execute("SELECT * FROM citas WHERE id = %s", (id,))
        cita = cursor.fetchone()

        if not cita:
            conn.close()
            raise HTTPException(status_code=404, detail="Cita no encontrada")

        if cita["estado"] == "cancelada":
            conn.close()
            raise HTTPException(status_code=400, detail="La cita ya estaba cancelada")

        
        cursor.execute(
            "UPDATE citas SET estado = 'cancelada' WHERE id = %s",
            (id,)
        )
        conn.commit()
        conn.close()

        return {
            "mensaje": "Cita cancelada exitosamente",
            "id": id,
            "paciente_id": cita["paciente_id"],
            "fecha": str(cita["fecha"]),
            "estado_anterior": cita["estado"],
            "estado_nuevo": "cancelada"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# MICROSERVICIO 6 - API GATEWAY
# ============================================================

@app.post("/reservar-cita")
async def reservar_cita(reserva: ReservaRequest):
    """
    Gateway completo:
    1. Verifica que el paciente existe
    2. Crea la cita
    3. Retorna el resultado completo
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        
        cursor.execute("SELECT * FROM pacientes WHERE id = %s", (reserva.paciente_id,))
        paciente = cursor.fetchone()

        if not paciente:
            conn.close()
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        
        await asyncio.sleep(1)

        
        cursor2 = conn.cursor()
        cursor2.execute(
            "INSERT INTO citas (paciente_id, fecha, estado) VALUES (%s, %s, 'activa')",
            (reserva.paciente_id, reserva.fecha)
        )
        conn.commit()
        nueva_cita_id = cursor2.lastrowid
        conn.close()

        return {
            "mensaje": "Reserva completada exitosamente",
            "paciente": {
                "id": paciente["id"],
                "nombre": paciente["nombre"],
                "email": paciente["email"]
            },
            "cita": {
                "id": nueva_cita_id,
                "fecha": reserva.fecha,
                "estado": "activa"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
