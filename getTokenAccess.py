from flask import Flask, request, redirect
from dotenv import load_dotenv, set_key
import requests
import os
load_dotenv()
app = Flask(__name__)

# Reemplaza con tus credenciales y la URL de callback registrada en Facebook
APP_ID = os.environ['APP_ID']
APP_SECRET = os.environ['APP_SECRET_TOKEN']
REDIRECT_URI = "http://localhost:5000/fb_callback"  # Reemplaza esto
SCOPE = 'public_profile,email,pages_manage_metadata,public_profile,pages_show_list,read_insights,pages_read_user_content,pages_read_engagement,pages_manage_posts,pages_manage_engagement'  # Define los permisos que necesitas

@app.route('/login/facebook')
def facebook_login():
    authorization_url = f"https://www.facebook.com/v19.0/dialog/oauth?" \
                        f"client_id={APP_ID}&" \
                        f"redirect_uri={REDIRECT_URI}&" \
                        f"scope={SCOPE}&" \
                        f"state=your_random_string"  # Añade un estado para seguridad
    return redirect(authorization_url)

@app.route('/fb_callback')
def facebook_callback():
    # ... (el resto de tu función callback permanece igual, usando REDIRECT_URI)
    if 'error' in request.args:
        return f"Error de autenticación: {request.args['error_description']}"

    auth_code = request.args.get('code')
    state = request.args.get('state')

    # Valida el 'state' si lo usaste

    token_url = "https://graph.facebook.com/v19.0/oauth/access_token"
    token_params = {
        'client_id': APP_ID,
        'client_secret': APP_SECRET,
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(token_url, params=token_params)
    response.raise_for_status()  # Lanza una excepción para errores HTTP
    token_data = response.json()

    access_token = token_data.get('access_token')
    token_type = token_data.get('token_type')
    expires_in = token_data.get('expires_in')

    try:
        if access_token:
            set_key('.env', "USER_ACCESS_TOKEN", access_token)
            return f"Se ha sobreescrito USER_ACCESS_TOKEN en .env . Token de acceso obtenido: {access_token} (tipo: {token_type}, expira en: {expires_in} segundos)"
        else:
            return "No se pudo obtener el token de acceso."
    except Exception as e:
        return f"Ocurrió un error al intentar escribir en .env: {e}"


    # if access_token:
    #     return f"Token de acceso obtenido: {access_token} (tipo: {token_type}, expira en: {expires_in} segundos)"
    # else:
    #     return "No se pudo obtener el token de acceso."


@app.route('/')
def html():
    return '<a href="/login/facebook">Login a Facebook</a>'

if __name__ == '__main__':
    app.run(debug=True)