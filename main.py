from flask import Flask, render_template, request, send_file, url_for, redirect
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
import random, string, os

with open('key', 'r') as dire:
    read = dire.read()
key = Fernet(read)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/encrypt', methods=['POST', 'GET'])
def encrypt():
    if request.method == 'POST':
        return redirect(url_for('download', filename=key.encrypt(str.encode(request.form['code']))))
    return render_template('encrypt.html')
@app.route('/download/<filename>')
def download(filename):
    letters = ''.join(random.choice(string.ascii_letters) for i in range(10))
    a = open('./files/' + letters + '.txt', 'w')
    a.write(filename)
    a.close()
    return send_file('./files/' + letters + '.txt', mimetype='application/x-csv', attachment_filename=letters + '.txt', as_attachment=True)
@app.route('/decrypt', methods=['POST', 'GET'])
def decrypt():
    return render_template('decrypt.html')
@app.route('/upload/', methods=['POST', 'GET'])
def uplaod():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        a = open(f.filename, 'r').read()
        return key.decrypt(str.encode(a))
    return 'sa'
app.run('localhost', 3000, debug=True)