import requests
import json
from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # --- CONFIGURACIÓN CON TU API KEY ---
        API_KEY = '513e52c6e279d11e0c5c2e8e93dd1c91' 
        URL_TARGET = 'https://www.metal.com/es/niobium-tantalum#NiobioTantalio'

        # Parámetros optimizados para ScraperAPI
        params = {
            'api_key': API_KEY,
            'url': URL_TARGET,
            'render': 'true',      # Necesario para procesar el JS de Metal.com
            'country_code': 'us'
        }

        try:
            # 1. Petición al proxy de ScraperAPI
            response = requests.get('http://api.scraperapi.com', params=params, timeout=60)
            
            if response.status_code == 200:
                # 2. Parseo del HTML con BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Usamos una función para encontrar las clases dinámicas que contienen '__value' y '__unit'
                # Esto es lo que permite capturar el 55.52 aunque el código de la clase cambie
                precio_tag = soup.find('span', class_=lambda x: x and '__value' in x)
                unidad_tag = soup.find('span', class_=lambda x: x and '__unit' in x)

                # Extraemos el texto limpio
                precio_valor = precio_tag.get_text(strip=True) if precio_tag else "No encontrado"
                unidad_valor = unidad_tag.get_text(strip=True) if unidad_tag else ""

                resultado = {
                    "mineral": "Niobio / Tantalio",
                    "precio": precio_valor,
                    "unidad": unidad_valor,
                    "status": "OK",
                    "timestamp": "2026-04-09" # Fecha actual
                }
                status_code = 200
            else:
                resultado = {
                    "error": "Error en ScraperAPI",
                    "codigo_error": response.status_code,
                    "mensaje": "Revisa tus créditos o la URL"
                }
                status_code = response.status_code

        except Exception as e:
            resultado = {
                "error": "Error crítico en el script",
                "detalle": str(e)
            }
            status_code = 500

        # 3. Respuesta final en formato JSON
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        # CORS habilitado para que tu frontend pueda consultar la API sin bloqueos
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()
        self.wfile.write(json.dumps(resultado).encode('utf-8'))