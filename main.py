from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

@app.route('/registro-uso', methods=['POST'])
def registrar_uso():
    data = request.json
    entrada = {
        "usuario_id": data.get("usuario_id", "anonimo"),
        "tipo_solicitud": data.get("tipo_solicitud", "desconocida"),
        "mensaje_usuario": data.get("mensaje_usuario"),
        "fecha": datetime.now().isoformat()
    }

    # Leer logs anteriores si existen
    if os.path.exists("logs.json"):
        with open("logs.json", "r") as f:
            log_data = json.load(f)
    else:
        log_data = []

    # Agregar nueva entrada
    log_data.append(entrada)

    # Guardar todos los logs en archivo
    with open("logs.json", "w") as f:
        json.dump(log_data, f, indent=2)

    print(f"Uso registrado: {entrada}")
    return jsonify({"status": "ok"})

@app.route('/ver-logs', methods=['GET'])
def ver_logs():
    if os.path.exists("logs.json"):
        with open("logs.json", "r") as f:
            log_data = json.load(f)
    else:
        log_data = []
    return jsonify(log_data)

app.run(host="0.0.0.0", port=3000)
