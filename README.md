# 🏥 Sistema Distribuido de Citas Médicas
## Laboratorio de Sistemas Distribuidos

---

## Información del servicio

| Campo | Detalle |
|-------|---------|
| **Microservicio** | Sistema completo de citas médicas |
| **Integrante** | Grupo 5 |
| **IP del servidor** | 172.20.87.41 |
| **Puerto** | 8001 |
| **Base de datos** | MySQL/MariaDB - citas_medicas |

---

## Endpoints implementados

### 1. Registrar paciente
- **Método:** `POST`
- **Ruta:** `/pacientes`
- **Parámetros:**
  - `nombre` (string) - Nombre del paciente
  - `email` (string) - Correo del paciente
- **Ejemplo request:**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@email.com"
}
```
- **Ejemplo response:**
```json
{
  "mensaje": "Paciente registrado exitosamente",
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@email.com"
}
```

---

### 2. Consultar paciente por ID
- **Método:** `GET`
- **Ruta:** `/pacientes/{id}`
- **Parámetros:**
  - `id` (int) - ID del paciente
- **Ejemplo request:**
```
GET http://172.20.87.41:8001/pacientes/1
```
- **Ejemplo response:**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@email.com"
}
```

---

### 3. Crear cita
- **Método:** `POST`
- **Ruta:** `/citas`
- **Parámetros:**
  - `paciente_id` (int) - ID del paciente
  - `fecha` (string) - Fecha en formato `YYYY-MM-DD HH:MM:SS`
- **Ejemplo request:**
```json
{
  "paciente_id": 1,
  "fecha": "2026-03-20 10:00:00"
}
```
- **Ejemplo response:**
```json
{
  "mensaje": "Cita creada exitosamente",
  "id": 1,
  "paciente_id": 1,
  "paciente_nombre": "Juan Pérez",
  "fecha": "2026-03-20 10:00:00",
  "estado": "activa"
}
```

---

### 4. Consultar citas de un paciente
- **Método:** `GET`
- **Ruta:** `/citas/{paciente_id}`
- **Parámetros:**
  - `paciente_id` (int) - ID del paciente
- **Ejemplo request:**
```
GET http://172.20.87.41:8001/citas/1
```
- **Ejemplo response:**
```json
{
  "paciente_id": 1,
  "paciente_nombre": "Juan Pérez",
  "total_citas": 1,
  "citas": [
    {
      "id": 1,
      "paciente_id": 1,
      "fecha": "2026-03-20 10:00:00",
      "estado": "activa"
    }
  ]
}
```

---

### 5. Cancelar cita
- **Método:** `DELETE`
- **Ruta:** `/citas/{id}`
- **Parámetros:**
  - `id` (int) - ID de la cita
- **Ejemplo request:**
```
DELETE http://172.20.87.41:8001/citas/1
```
- **Ejemplo response:**
```json
{
  "mensaje": "Cita cancelada exitosamente",
  "id": 1,
  "paciente_id": 1,
  "estado_anterior": "activa",
  "estado_nuevo": "cancelada"
}
```

---

### 6. Reservar cita (API Gateway)
- **Método:** `POST`
- **Ruta:** `/reservar-cita`
- **Parámetros:**
  - `paciente_id` (int) - ID del paciente
  - `fecha` (string) - Fecha en formato `YYYY-MM-DD HH:MM:SS`
- **Ejemplo request:**
```json
{
  "paciente_id": 1,
  "fecha": "2026-03-20 11:00:00"
}
```
- **Ejemplo response:**
```json
{
  "mensaje": "Reserva completada exitosamente",
  "paciente": {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@email.com"
  },
  "cita": {
    "id": 2,
    "fecha": "2026-03-20 11:00:00",
    "estado": "activa"
  }
}
```

---

## Cómo ejecutar

### 1. Instalar dependencias
```bash
pip install fastapi uvicorn mysql-connector-python
```

### 2. Ejecutar el servidor
```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Ver documentación interactiva
```
http://172.20.87.41:8001/docs
```

---

## Prueba de concurrencia

Se simulo un cliente creando una cita.

**¿Qué ocurrió?**
El cliente se creo Nicolas se creo exitosamente y se guardo en la base de datos. Lo mismo en la cita, el INSERT se ejecuto y quedo creada en la base de datos


```

---

## Repositorio

🔗 Enlace del repositorio: `https://github.com/nicolasgarciae/clase5`
