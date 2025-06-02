import os
import traceback
from flask import Flask, request, jsonify
from app.wsaa import obtener_token
from app.wsfe import emitir_factura

app = Flask(__name__)

@app.route('/emitir', methods=['POST'])
def emitir():
    datos = request.get_json(force=True)
    print("🔔 Datos recibidos en /emitir:", datos)
    try:
        ta = obtener_token()
        resultado = emitir_factura(datos, ta)
        print("✅ Resultado:", resultado)
        return jsonify(resultado)
    except Exception as e:
        print("❌ Error en el backend:", str(e))
        traceback.print_exc()  # 🔍 Esto imprime el error completo en los logs de Render
        return jsonify({"error": str(e)}), 500

@app.route('/wsaa-test', methods=['GET'])
def test_wsaa():
    try:
        ta = obtener_token()
        return jsonify({"ticket_acceso": ta})
    except Exception as e:
        print("❌ Error al obtener TA:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({"mensaje": "El endpoint /emitir funciona correctamente"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
