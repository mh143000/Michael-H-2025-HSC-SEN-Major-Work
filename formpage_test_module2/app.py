from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize assetinfo database
def init_db():
    with sqlite3.connect('assetinfo.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unit TEXT NOT NULL,
                type TEXT NOT NULL,
                identifier TEXT NOT NULL
            )
        ''')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('form.html', asset=None)

@app.route('/submit', methods=['POST'])
def submit():
    unit = request.form['unit']
    asset_type = request.form['type']
    identifier = request.form['identifier']
    with sqlite3.connect('assetinfo.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO assets (unit, type, identifier) VALUES (?, ?, ?)", (unit, asset_type, identifier))
    return redirect('/data')

@app.route('/data')
def data():
    with sqlite3.connect('assetinfo.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assets")
        assets = cursor.fetchall()
    return render_template('data.html', assets=assets)

@app.route('/delete/<int:asset_id>')
def delete(asset_id):
    with sqlite3.connect('assetinfo.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
    return redirect('/data')

@app.route('/edit/<int:asset_id>', methods=['GET', 'POST'])
def edit(asset_id):
    if request.method == 'POST':
        unit = request.form['unit']
        asset_type = request.form['type']
        identifier = request.form['identifier']
        with sqlite3.connect('assetinfo.db') as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE assets SET unit = ?, type = ?, identifier = ? WHERE id = ?", (unit, asset_type, identifier, asset_id))
        return redirect('/data')
    else:
        with sqlite3.connect('assetinfo.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
            asset = cursor.fetchone()
        return render_template('form.html', asset=asset)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
