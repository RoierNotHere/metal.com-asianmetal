from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Configuración de credenciales
USER_OXY = 'RoierWasHere_6fepU'
PASS_OXY = 'w+HJwa9qinURST0'

@app.route('/precio-coltan', methods=['GET'])
def obtener_coltan():
    url_realtime = 'https://realtime.oxylabs.io/v1/queries'
    
    payload = {
        'source': 'universal',
        'url': 'https://www.metal.com/es/niobium-tantalum#NiobioTantalio',
        'parse': True,
        'parser_preset': 'MineralColtan',
        'render': 'html'
    }

    try:
        response = requests.post(
            url_realtime,
            auth=(USER_OXY, PASS_OXY),
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            # Extraemos solo el contenido que definió tu preset
            resultado = data['results'][0]['content']
            
            # Devolvemos el JSON limpio para tu frontend
            return jsonify({
                "status": "success",
                "mineral": "Coltán/Niobio",
                "data": resultado
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"Error de Oxylabs: {response.status_code}"
            }), response.status_code

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Esto es para correrlo localmente
    app.run(debug=True, port=5000)