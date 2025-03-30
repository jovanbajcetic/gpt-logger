from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import requests

app = Flask(__name__)

# URL del endpoint de Sheety (reemplaza con la tuya si cambia)
SHEETY_URL = "https://api.sheety.co/4ff35523befe0e1a8c6a211fa940964a/registroGptWtw/registroGpt"

@app.route('/registro-uso', methods=['POST'])
def registrar_uso():
    data = request.json
    entrada = {
        "registroGpt": {
            "usuarioId": data.get("usuario_id", "anonimo"),
            "tipoSolicitud": data.get("tipo_solicitud", "desconocida"),
            "mensajeUsuario": data.get("mensaje_usuario", ""),
            "fecha": datetime.now().isoformat()
        }
    }

    response = requests.post(SHEETY_URL, json=entrada)

    if response.status_code in [200, 201]:
        print("✅ Uso registrado correctamente en Sheety.")
        return jsonify({"status": "ok"}), 200
    else:
        print("❌ Error al registrar en Sheety:", response.text)
        return jsonify({"status": "error", "detail": response.text}), 500

@app.route('/ver-logs-html', methods=['GET'])
def ver_logs_html():
    try:
        response = requests.get(SHEETY_URL)
        if response.status_code == 200:
            log_data = response.json().get("registroGpt", [])
        else:
            log_data = []
    except Exception as e:
        print("❌ Error al obtener los registros:", e)
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
                    <td>{{ entrada['usuarioId'] }}</td>
                    <td>{{ entrada['tipoSolicitud'] }}</td>
                    <td>{{ entrada['mensajeUsuario'] }}</td>
                    <td>{{ entrada['fecha'] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """
    return render_template_string(html_template, log_data=log_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
