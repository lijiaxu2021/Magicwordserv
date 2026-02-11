from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = 'magicword_secret_key_change_me'

# Configuration
CONFIG_FILE = 'config.json'
DEFAULT_CONFIG = {
    'api_key': '',
    'model_name': 'Qwen/Qwen2.5-7B-Instruct',
    'default_library_content': [] # Store JSON content directly or path
}

# Admin Credentials
ADMIN_USER = 'upxuu'
ADMIN_PASS = 'lijiaxu2011'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('admin'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    config = load_config()
    
    if request.method == 'POST':
        config['api_key'] = request.form.get('api_key')
        config['model_name'] = request.form.get('model_name')
        
        # Handle Library Upload
        library_file = request.files.get('library_file')
        if library_file and library_file.filename != '':
            try:
                content = json.load(library_file)
                config['default_library_content'] = content
            except Exception as e:
                return render_template('admin.html', config=config, error=f"Invalid JSON file: {e}")
        
        save_config(config)
        return render_template('admin.html', config=config, message="Configuration saved successfully!")
        
    return render_template('admin.html', config=config)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/api/init-config', methods=['GET'])
def get_init_config():
    config = load_config()
    lib_content = config.get('default_library_content', [])
    
    # Ensure default_library is a list
    if isinstance(lib_content, dict):
        # Heuristic: return the first list found in values, or empty
        found = False
        for val in lib_content.values():
            if isinstance(val, list):
                lib_content = val
                found = True
                break
        if not found:
            lib_content = []
            
    return jsonify({
        'api_key': config.get('api_key', ''),
        'model_name': config.get('model_name', ''),
        'default_library': lib_content
    })

if __name__ == '__main__':
    # Ensure templates directory exists
    os.makedirs('templates', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
