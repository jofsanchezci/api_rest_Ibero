# REST API — Conceptos Fundamentales

Este documento presenta una explicación clara el concepto **REST API**, ideal para proyectos de desarrollo web, documentación técnica o material de clase.

## ¿Qué es una REST API?

Una **REST API** (Representational State Transfer Application Programming Interface) es un estilo arquitectónico para diseñar servicios web que permiten que diferentes aplicaciones se comuniquen entre sí a través del protocolo HTTP.

REST no es un estándar, sino un **conjunto de principios** que buscan simplicidad, escalabilidad y desacoplamiento entre sistemas.

## Principios Fundamentales

### 1. Arquitectura Cliente–Servidor
La API separa completamente la lógica del servidor (backend) de la interfaz del cliente (frontend), lo que facilita el mantenimiento y escalabilidad.

### 2. Sin Estado (Stateless)
Cada solicitud enviada al servidor debe incluir **toda la información necesaria** para ser procesada.

### 3. Interfaz Uniforme
Los recursos deben exponerse de forma consistente.

### 4. Uso Estándar de los Métodos HTTP

| Método | Descripción |
|--------|-------------|
| GET | Obtener un recurso |
| POST | Crear un recurso |
| PUT | Actualizar completamente |
| PATCH | Actualizar parcialmente |
| DELETE | Eliminar |

### 5. Identificación de Recursos mediante URLs

```
GET /usuarios
GET /usuarios/10
POST /usuarios
DELETE /usuarios/10
```

### 6. Representación del Recurso

```json
{ "id": 10, "nombre": "Ana", "email": "ana@example.com" }
```

## Ventajas de REST
- Simplicidad  
- Escalabilidad  
- Flexibilidad  
- Desacoplamiento  

## REST vs Otros Estilos
- REST  
- SOAP  
- GraphQL  
- gRPC  

## 🛠 Ejemplo con Flask

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

usuarios = [
    {"id": 1, "nombre": "Carlos"},
    {"id": 2, "nombre": "Ana"}
]

@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    return jsonify(usuarios)

@app.route("/usuarios/<int:id>", methods=["GET"])
def obtener_usuario(id):
    user = next((u for u in usuarios if u["id"] == id), None)
    return jsonify(user)

@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    data = request.json
    usuarios.append(data)
    return jsonify(data), 201

if __name__ == "__main__":
    app.run(debug=True)
```

## Conclusión
Una REST API es un estándar moderno y eficiente para la comunicación entre sistemas.

