from flask import Flask, request, jsonify, render_template_string
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

@app.route('/ver-logs-html', methods=['GET'])
def ver_logs_html():
    if os.path.exists("logs.json"):
        with open("logs.json", "r") as f:
            log_data = json.load(f)
    else:
        log_data = []

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Registros de uso</title>
        <style>
            body { font-family: Arial; background: #f9f9f9; padding: 30px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 10px; border: 1px solid #ccc; text-align: left; }
            th { background: #eee; }
            tr:nth-child(even) { background: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>📊 Registros de uso del GPT</h1>
        <table>
            <thead>
                <tr><th>Usuario</th><th>Tipo</th><th>Mensaje</th><th>Fecha</th></tr>
            </thead>
            <tbody>
                {% for entrada in log_data %}
                <tr>
                    <td>{{ entrada['usuario_id'] }}</td>
                    <td>{{ entrada['tipo_solicitud'] }}</td>
                    <td>{{ entrada['mensaje_usuario'] }}</td>
                    <td>{{ entrada['fecha'] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """
    return render_template_string(html_template, log_data=log_data)

# Ejecutar localmente (útil solo en desarrollo)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)


