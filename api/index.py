import requests
import json
import time
from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup

# VARIABLES DE CACHÉ (Viven en la memoria del servidor de Vercel)
# Se mantienen vivas mientras la función no se "congele" por inactividad
cache_data = {
    "precio": None,
    "unidad": None,
    "timestamp": 0  # Guardamos la hora exacta de la última petición
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global cache_data
        
        # --- CONFIGURACIÓN ---
        API_KEY = '513e52c6e279d11e0c5c2e8e93dd1c91'
        URL_TARGET = 'https://www.metal.com/es/niobium-tantalum#NiobioTantalio'
        
        # 2 horas en segundos (60 seg * 60 min * 2) = 7200 segundos
        TIEMPO_LIMITE = 7200 
        ahora = time.time()

        # 1. VERIFICACIÓN DEL TIMER
        # Si tenemos un precio y no han pasado 2 horas, NO llamamos a la API
        if cache_data["precio"] and (ahora - cache_data["timestamp"] < TIEMPO_LIMITE):
            tiempo_transcurrido = int(ahora - cache_data["timestamp"])
            print(f"--- MODO AHORRO ACTIVO ---")
            print(f"Usando datos de hace {tiempo_transcurrido} segundos. Créditos ahorrados.")
            
            resultado = {
                "mineral": "Niobio / Tantalio",
                "precio": cache_data["precio"],
                "unidad": cache_data["unidad"],
                "info": "Datos recuperados de caché (Menos de 2 horas)",
                "segundos_desde_actualizacion": tiempo_transcurrido
            }
            status_code = 200
        else:
            # 2. SI PASÓ EL TIEMPO O ES LA PRIMERA VEZ, LLAMAMOS A SCRAPERAPI
            print("--- ACTUALIZANDO DATOS ---")
            print("El timer expiró o es la primera petición. Llamando a ScraperAPI...")
            
            params = {
                'api_key': API_KEY,
                'url': URL_TARGET,
                'render': 'true',
                'country_code': 'us'
            }

            try:
                response = requests.get('http://api.scraperapi.com', params=params, timeout=60)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Buscamos el valor con el selector dinámico que ya probamos
                    precio_tag = soup.find('span', class_=lambda x: x and '__value' in x)
                    unidad_tag = soup.find('span', class_=lambda x: x and '__unit' in x)

                    if precio_tag:
                        val = precio_tag.get_text(strip=True)
                        uni = unidad_tag.get_text(strip=True) if unidad_tag else ""

                        # ACTUALIZAMOS EL TIMER Y LA CACHÉ
                        cache_data["precio"] = val
                        cache_data["unidad"] = uni
                        cache_data["timestamp"] = ahora

                        print(f"VALOR EXTRAÍDO Y GUARDADO: {val}")
                        
                        resultado = {
                            "mineral": "Niobio / Tantalio",
                            "precio": val,
                            "unidad": uni,
                            "info": "Datos actualizados de ScraperAPI"
                        }
                        status_code = 200
                    else:
                        resultado = {"error": "No se encontró el tag value en el HTML"}
                        status_code = 500
                else:
                    resultado = {"error": "Error de ScraperAPI", "code": response.status_code}
                    status_code = response.status_code

            except Exception as e:
                print(f"ERROR: {str(e)}")
                resultado = {"error": "Error interno", "detalle": str(e)}
                status_code = 500

        # 3. RESPUESTA JSON FINAL
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(resultado).encode('utf-8'))