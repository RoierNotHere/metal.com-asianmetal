import requests
import json
import time
from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup

# Variables globales para "caché" temporal (dura mientras la función esté activa)
cache = {
    "precio": None,
    "unidad": None,
    "last_update": 0
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # --- CONFIGURACIÓN ---
        API_KEY = '513e52c6e279d11e0c5c2e8e93dd1c91'
        # Definimos que el precio "expira" cada 3600 segundos (1 hora)
        CACHE_DURATION = 3600 
        current_time = time.time()

        # 1. ¿VALOR EN CACHÉ? Si el tiempo no ha pasado, devolvemos lo guardado
        if cache["precio"] and (current_time - cache["last_update"] < CACHE_DURATION):
            print("Caché activa: Devolviendo valor guardado para ahorrar créditos.")
            resultado = {
                "mineral": "Niobio / Tantalio",
                "precio": cache["precio"],
                "unidad": cache["unidad"],
                "fuente": "Caché interna (Vercel)",
                "proxima_actualizacion_en_seg": int(CACHE_DURATION - (current_time - cache["last_update"]))
            }
            status_code = 200
        else:
            # 2. SI NO HAY CACHÉ, LLAMAMOS A LA API
            print("Caché expirada o vacía: Llamando a ScraperAPI...")
            payload = { 
                'api_key': API_KEY, 
                'url': 'https://www.metal.com/es/niobium-tantalum#NiobioTantalio', 
                'render': 'true', 
                'country_code': 'us' 
            }
            
            try:
                r = requests.get('https://api.scraperapi.com/', params=payload, timeout=60)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    precio_tag = soup.find('span', class_=lambda x: x and '__value' in x)
                    unidad_tag = soup.find('span', class_=lambda x: x and '__unit' in x)
                    
                    val = precio_tag.get_text(strip=True) if precio_tag else "No encontrado"
                    uni = unidad_tag.get_text(strip=True) if unidad_tag else ""

                    # 3. ACTUALIZAMOS LA CACHÉ
                    cache["precio"] = val
                    cache["unidad"] = uni
                    cache["last_update"] = current_time

                    resultado = {
                        "mineral": "Niobio / Tantalio",
                        "precio": val,
                        "unidad": uni,
                        "fuente": "ScraperAPI (Créditos usados)"
                    }
                    status_code = 200
                else:
                    resultado = {"error": "Error API", "code": r.status_code}
                    status_code = r.status_code
            except Exception as e:
                resultado = {"error": str(e)}
                status_code = 500

        # 4. RESPUESTA JSON
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(resultado).encode('utf-8'))