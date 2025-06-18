from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

#initializes db for assets called 'assetinfo.db', the table of the db named 'assets' (seen later in html Jinja2 experessions)
def init_asset_db():
    with sqlite3.connect('assetinfo.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unit TEXT NOT NULL,
                type TEXT NOT NULL,
                identifier TEXT NOT NULL
            )
        ''')

#ditto as above... 'assignments.db' database, table named 'assignments'
def init_assignment_db():
    with sqlite3.connect('assignments.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                requirements TEXT NOT NULL
            )
        ''')


def init_asset_assignment_db():
    with sqlite3.connect('asset_assignment.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS asset_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id INTEGER,
                assignment_id INTEGER
            )
        ''')



# ========== ROUTES ==========

#home page of app
@app.route('/')
def home():
    return render_template('home.html')

# --- ASSET ROUTES ---

#asset input form page
@app.route('/form')
def form():
    return render_template('form.html', asset=None)

#form submission handler (POST saves updates)
@app.route('/submit', methods=['POST'])
def submit():
    unit = request.form['unit']
    asset_type = request.form['type']
    identifier = request.form['identifier']
    with sqlite3.connect('assetinfo.db') as conn: #stores data into the asset database
        conn.execute("INSERT INTO assets (unit, type, identifier) VALUES (?, ?, ?)", (unit, asset_type, identifier))
    return redirect('/data') #opens to asset viewing page data.html

#hanlder that gets all the data from the asset db and displays it when needed on the asset info html page
@app.route('/data')
def data():
    with sqlite3.connect('assetinfo.db') as conn:
        assets = conn.execute("SELECT * FROM assets").fetchall()

    with sqlite3.connect('asset_assignment.db') as conn:
        linked_assets = {row[0] for row in conn.execute("SELECT asset_id FROM asset_assignments").fetchall()}

    asset_status = {
        a[0]: "🟢 Assigned" if a[0] in linked_assets else "🟠 Unassigned"
        for a in assets
    }

    return render_template('data.html', assets=assets, asset_status=asset_status)


#handler that deletes an asset in correspondence to the id of the asset
@app.route('/delete/<int:asset_id>')
def delete(asset_id):
    with sqlite3.connect('assetinfo.db') as conn:
        conn.execute("DELETE FROM assets WHERE id = ?", (asset_id,)) #delete execution in assetinfo.db
    return redirect('/data') #goes back to asset viewing page data.html

#hanlder that edits an asset by id where GET shows form, POST saves updates
@app.route('/edit/<int:asset_id>', methods=['GET', 'POST'])
def edit(asset_id):
    if request.method == 'POST': #POST updates the asset in the db
        unit = request.form['unit']
        asset_type = request.form['type']
        identifier = request.form['identifier']
        with sqlite3.connect('assetinfo.db') as conn:
            conn.execute("UPDATE assets SET unit = ?, type = ?, identifier = ? WHERE id = ?", (unit, asset_type, identifier, asset_id))
        return redirect('/data') #goes back to asset viewing page
    else: #load existing asset for editing
        with sqlite3.connect('assetinfo.db') as conn:
            asset = conn.execute("SELECT * FROM assets WHERE id = ?", (asset_id,)).fetchone() #fetches the asset in question according to its id
        return render_template('form.html', asset=asset) #goes back to asset viewing page

# --- ASSIGNMENT ROUTES ---

#displays the assignment input form
@app.route('/assignment_form')
def assignment_form():
    return render_template('assignment_form.html') # shows assignment viewing page

#handler for the assignment form submission and stores data (POST)
@app.route('/assignment_submit', methods=['POST']) #POST updates db
def assignment_submit():
    title = request.form['title']
    description = request.form['description']
    location = request.form['location']
    requirements = request.form['requirements']
    with sqlite3.connect('assignments.db') as conn:
        conn.execute("INSERT INTO assignments (title, description, location, requirements) VALUES (?, ?, ?, ?)",
                     (title, description, location, requirements))
    return redirect('/assignments') #opens assignment viewing page 

#handler that gets all the assignment data from its db and displays it on its viewing page
@app.route('/assignments')
def assignments():
    with sqlite3.connect('assignments.db') as conn:
        assignments = conn.execute("SELECT * FROM assignments").fetchall()

    with sqlite3.connect('asset_assignment.db') as conn:
        links = conn.execute("SELECT assignment_id FROM asset_assignments").fetchall()
        linked_assignments = {row[0] for row in links}

    assignment_status = {
        a[0]: "🟢 Asset Linked" if a[0] in linked_assignments else "🟠 No Asset"
        for a in assignments
    }

    return render_template('assignment_data.html', assignments=assignments, assignment_status=assignment_status)


#handler that edits an assignment by id where GET shows form, POST saves updates
@app.route('/assignment_edit/<int:assignment_id>', methods=['GET', 'POST'])
def assignment_edit(assignment_id):
    if request.method == 'POST': #POST saves updates to the assignments
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        requirements = request.form['requirements']
        with sqlite3.connect('assignments.db') as conn:
            conn.execute('''
                UPDATE assignments SET
                    title = ?,
                    description = ?,
                    location = ?,
                    requirements = ?
                WHERE id = ?
            ''', (title, description, location, requirements, assignment_id))
        return redirect('/assignments')
    else: #load an assignment for editing
        with sqlite3.connect('assignments.db') as conn:
            assignment = conn.execute("SELECT * FROM assignments WHERE id = ?", (assignment_id,)).fetchone()
        return render_template('assignment_form.html', assignment=assignment) #goes back to assignment viewing page

#handler that deletes an assignment in correspondence to the id of the assignment
@app.route('/assignment_delete/<int:assignment_id>')
def assignment_delete(assignment_id):
    with sqlite3.connect('assignments.db') as conn:
        conn.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))
    return redirect('/assignments') #goes back to assignment viewing page

# --- ASSET ATTACHMENT ROUTES ---

@app.route('/link_assets', methods=['GET', 'POST'])
def link_assets():
    if request.method == 'POST':
        asset_id = request.form['asset_id']
        assignment_id = request.form['assignment_id']
        with sqlite3.connect('asset_assignment.db') as conn:
            conn.execute("DELETE FROM asset_assignments WHERE asset_id = ?", (asset_id,))
            conn.execute("INSERT INTO asset_assignments (asset_id, assignment_id) VALUES (?, ?)", (asset_id, assignment_id))
        return redirect('/link_assets')
    else:
        with sqlite3.connect('assetinfo.db') as conn:
            assets = {row[0]: row for row in conn.execute("SELECT * FROM assets").fetchall()}
        with sqlite3.connect('assignments.db') as conn:
            assignments = {row[0]: row for row in conn.execute("SELECT * FROM assignments").fetchall()}
        with sqlite3.connect('asset_assignment.db') as conn:
            links = conn.execute("SELECT asset_id, assignment_id FROM asset_assignments").fetchall()

        # For display in linked table, convert to dicts for quick lookup
        assets_dict = {a[0]: a for a in assets_list}
        assignments_dict = {a[0]: a for a in assignments_list}

        return render_template(
            'link_assets.html',
            assets=assets_list,
            assignments=assignments_list,
            assets_dict=assets_dict,
            assignments_dict=assignments_dict,
            links=links
        )


@app.route('/unlink_asset', methods=['POST'])
def unlink_asset():
    asset_id = request.form['asset_id']
    with sqlite3.connect('asset_assignment.db') as conn:
        conn.execute("DELETE FROM asset_assignments WHERE asset_id = ?", (asset_id,))
    return redirect('/link_assets')


# --- INIT ---

#initialises the both db's and the whole python flask app
if __name__ == '__main__':
    init_asset_db()
    init_assignment_db()
    init_asset_assignment_db()
    app.run(debug=True)
