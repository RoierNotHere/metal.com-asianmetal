import cloudscraper
from bs4 import BeautifulSoup

def obtener_precios():
    # Creamos el scraper que se encarga de saltar protecciones
    scraper = cloudscraper.create_scraper()
    
    # --- 1. TITANIO (Trading Economics) ---
    url_te = "https://tradingeconomics.com/commodities"
    try:
        response_te = scraper.get(url_te)
        soup_te = BeautifulSoup(response_te.text, 'html.parser')
        
        # Buscamos la fila por el símbolo que identificamos antes
        fila_titanio = soup_te.find('tr', {'data-symbol': 'TTSG:COM'})
        if fila_titanio:
            precio_ti = fila_titanio.find('td', {'id': 'p'}).text.strip()
            print(f"✅ Titanio: {precio_ti} CNY/KG")
        else:
            print("❌ No se encontró la fila del Titanio en Trading Economics.")
    except Exception as e:
        print(f"Error en Trading Economics: {e}")

    # --- 2. COLTÁN / NIOBIO-TANTALIO (Metal.com) ---
    url_metal = "https://www.metal.com/es/niobium-tantalum"
    try:
        response_metal = scraper.get(url_metal)
        soup_metal = BeautifulSoup(response_metal.text, 'html.parser')
        
        # Usamos las clases de tu CSS
        # Nota: Estas clases suelen ser dinámicas, si fallan, busca el span por valor
        precio_coltan = soup_metal.find('span', class_='index-module-scss-module__VtpR9W__value')
        unidad_coltan = soup_metal.find('span', class_='index-module-scss-module__VtpR9W__unit')
        
        if precio_coltan:
            print(f"✅ Coltán (Niobio/Tantalio): {precio_coltan.text} {unidad_coltan.text}")
        else:
            print("❌ No se encontró el precio del Coltán en Metal.com.")
    except Exception as e:
        print(f"Error en Metal.com: {e}")

if __name__ == "__main__":
    obtener_precios()