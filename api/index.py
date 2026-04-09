import requests
import json
from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # --- CONFIGURACIÓN ---
        API_KEY = '513e52c6e279d11e0c5c2e8e93dd1c91'
        URL_TARGET = 'https://www.metal.com/es/niobium-tantalum#NiobioTantalio'

        params = {
            'api_key': API_KEY,
            'url': URL_TARGET,
            'render': 'true',
            'country_code': 'us'
        }

        try:
            # 1. Petición a ScraperAPI
            response = requests.get('http://api.scraperapi.com', params=params, timeout=60)
            
            if response.status_code == 200:
                # 2. Parseo del HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Buscamos las clases que contienen '__value' y '__unit'
                precio_tag = soup.find('span', class_=lambda x: x and '__value' in x)
                unidad_tag = soup.find('span', class_=lambda x: x and '__unit' in x)

                precio_valor = precio_tag.get_text(strip=True) if precio_tag else "No encontrado"
                unidad_valor = unidad_tag.get_text(strip=True) if unidad_tag else ""

                # --- EL PRINT PARA LA CONSOLA ---
                print(f"--- SCRAPEADO EXITOSO ---")
                print(f"Mineral: Niobio / Tantalio")
                print(f"Valor extraído: {precio_valor} {unidad_valor}")
                print(f"--------------------------")

                resultado = {
                    "mineral": "Niobio / Tantalio",
                    "precio": precio_valor,
                    "unidad": unidad_valor,
                    "status": "OK"
                }
                status_code = 200
            else:
                print(f"Error en ScraperAPI: {response.status_code}")
                resultado = {"error": "Error en ScraperAPI", "codigo": response.status_code}
                status_code = response.status_code

        except Exception as e:
            print(f"Error crítico: {str(e)}")
            resultado = {"error": "Error interno", "detalle": str(e)}
            status_code = 500

        # 3. Respuesta JSON para la web
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(resultado).encode('utf-8'))