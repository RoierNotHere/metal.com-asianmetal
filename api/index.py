import requests
import json
from http.server import BaseHTTPRequestHandler

# Credenciales de Oxylabs
USER_OXY = 'RoierWasHere_6fepU'
PASS_OXY = 'w+HJwa9qinURST0'

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # 1. Configuración de la petición a Oxylabs
        payload = {
            'source': 'universal',
            'url': 'https://www.metal.com/es/niobium-tantalum#NiobioTantalio',
            'parse': True,
            'parser_preset': 'MineralColtan',
            'render': 'html'
        }

        try:
            # 2. Llamada a Oxylabs
            response = requests.post(
                'https://realtime.oxylabs.io/v1/queries',
                auth=(USER_OXY, PASS_OXY),
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()
                resultado = data['results'][0]['content']
                status = 200
            else:
                resultado = {"error": f"Oxylabs status {response.status_code}"}
                status = response.status_code

        except Exception as e:
            resultado = {"error": str(e)}
            status = 500

        # 3. Respuesta HTTP
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        # Habilitar CORS para que puedas leerlo desde cualquier web
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()
        
        # Enviamos el JSON
        self.wfile.write(json.dumps(resultado).encode('utf-8'))
        return