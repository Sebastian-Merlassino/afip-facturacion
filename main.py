from flask import Flask, request, jsonify
from app.wsaa import obtener_token
from app.wsfe import emitir_factura

app = Flask(__name__)

@app.route('/emitir', methods=['POST'])
def emitir():
    datos = request.json
    try:
        ta = obtener_token()
        resultado = emitir_factura(datos, ta)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)