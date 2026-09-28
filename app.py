from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('tarjetas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarjetas (
            id TEXT PRIMARY KEY,
            is_active BOOLEAN,
            client_name TEXT,
            business_name TEXT,
            whatsapp TEXT,
            destination_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/c/<tarjeta_id>')
def manejar_tarjeta(tarjeta_id):
    conn = sqlite3.connect('tarjetas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT is_active, destination_url FROM tarjetas WHERE id = ?', (tarjeta_id,))
    resultado = cursor.fetchone()
    conn.close()

    if not resultado:
        conn = sqlite3.connect('tarjetas.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tarjetas (id, is_active) VALUES (?, ?)', (tarjeta_id, False))
        conn.commit()
        conn.close()
        is_active = False
    else:
        is_active, destination_url = resultado

    if is_active and destination_url:
        return redirect(destination_url)

    return render_template_string(HTML_LANDING, tarjeta_id=tarjeta_id)

@app.route('/activar/<tarjeta_id>', methods=['POST'])
def activar_tarjeta(tarjeta_id):
    client_name = request.form.get('client_name')
    business_name = request.form.get('business_name')
    whatsapp = request.form.get('whatsapp')
    destination_url = request.form.get('destination_url')

    conn = sqlite3.connect('tarjetas.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tarjetas 
        SET is_active = ?, client_name = ?, business_name = ?, whatsapp = ?, destination_url = ?
        WHERE id = ?
    ''', (True, client_name, business_name, whatsapp, destination_url, tarjeta_id))
    conn.commit()
    conn.close()

    return render_template_string(HTML_SUCCESS, destination_url=destination_url)

HTML_LANDING = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Activa tu Smart Card</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-950 text-white font-sans antialiased flex items-center justify-center min-h-screen p-4">
    <div class="max-w-md w-full bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-2xl">
        <div class="text-center mb-6">
            <span class="bg-fuchsia-600/20 text-fuchsia-400 text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wider">Smart Card Neón</span>
            <h1 class="text-2xl font-bold mt-2">¡Hola! Gracias por tu compra ⚡</h1>
            <p class="text-gray-400 text-sm mt-1">Seguinos en nuestras redes y configurá tu tarjeta inteligente para tu negocio.</p>
        </div>
        <a href="https://instagram.com/tu_usuario" target="_blank" class="block w-full text-center bg-gradient-to-r from-purple-600 to-fuchsia-600 hover:opacity-90 font-medium py-3 rounded-xl mb-6 shadow-lg transition">
            ❤️ Seguirnos en Instagram
        </a>
        <hr class="border-gray-800 my-6">
        <div class="mb-4">
            <h2 class="text-lg font-semibold">Configuración de la Tarjeta</h2>
            <p class="text-gray-400 text-xs mt-1">Completá los datos para vincular este dispositivo con tu emprendimiento.</p>
        </div>
        <form action="/activar/{{ tarjeta_id }}" method="POST" class="space-y-4">
            <div>
                <label class="block text-xs text-gray-400 mb-1">Tu Nombre</label>
                <input type="text" name="client_name" required class="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-fuchsia-500" placeholder="Ej: Juan Pérez">
            </div>
            <div>
                <label class="block text-xs text-gray-400 mb-1">Nombre de tu Negocio</label>
                <input type="text" name="business_name" required class="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-fuchsia-500" placeholder="Ej: Neón Studio">
            </div>
            <div>
                <label class="block text-xs text-gray-400 mb-1">WhatsApp de contacto</label>
                <input type="text" name="whatsapp" required class="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-fuchsia-500" placeholder="Ej: 1122334455">
            </div>
            <div>
                <label class="block text-xs text-gray-400 mb-1">Link de destino (Instagram o Google Maps)</label>
                <input type="url" name="destination_url" required class="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-fuchsia-500" placeholder="https://instagram.com/tu_negocio">
            </div>
            <button type="submit" class="w-full bg-white text-gray-950 font-bold py-3 rounded-xl hover:bg-gray-200 transition mt-2">
                🚀 Activar mi Tarjeta
            </button>
        </form>
    </div>
</body>
</html>
'''

HTML_SUCCESS = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>¡Tarjeta Activada!</title>
    <script src="https://tailwindcss.com"></script>
</head>
<body class="bg-gray-950 text-white font-sans antialiased flex items-center justify-center min-h-screen p-4">
    <div class="max-w-md w-full bg-gray-900 border border-gray-800 rounded-2xl p-8 text-center shadow-2xl">
        <div class="w-16 h-16 bg-green-500/20 text-green-400 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">✓</div>
        <h1 class="text-2xl font-bold">¡Listo! Tarjeta Configurada</h1>
        <p class="text-gray-400 text-sm mt-2">A partir de ahora, cada escaneo redirigirá automáticamente a:</p>
        <div class="bg-gray-800 p-3 rounded-xl my-4 text-xs text-fuchsia-400 truncate">{{ destination_url }}</div>
        <p class="text-gray-500 text-xs">Ya podés cerrar esta ventana.</p>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
