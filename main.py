from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/emitir', methods=['POST'])
def emitir():
    return jsonify({"mensaje": "El endpoint /emitir funciona correctamente"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
