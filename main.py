from flask import render_template_string
import os, json

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

