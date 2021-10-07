import os
import sqlite3

from flask import Flask, request, jsonify, send_from_directory
from utils import allowed_file
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = "photos"

@app.route('/photos/<path:path>')
def send_js(path):
    return send_from_directory('photos', path)


@app.route("/contacts", methods=["GET"])
def contact_read():
    search = request.args.get('search')

    con = sqlite3.connect('example.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    sql = '''
       SELECT * FROM Contacts;
    '''

    if search is not None:
        sql = f'''
                SELECT * 
                FROM Contacts 
                WHERE Name LIKE '%{search}%' 
                    OR  Surname LIKE '%{search}%'
                ;
            '''

    cur.execute(sql)
    rows = cur.fetchall()
    result = [dict(row) for row in rows]
    con.commit()
    con.close()
    return jsonify(result)

@app.route("/contacts", methods=["POST"])
def contact_create():
    name = request.form.get("name")
    surname = request.form.get("surname")
    phone = request.form.get("phone")
    address = request.form.get("address")
    url = request.form.get("url")
    country = request.form.get("country")
    town = request.form.get("town")
    street = request.form.get("street")

    if name is None or surname is None or phone is None:
        return "Вы не ввели достаточно информации, повторите попытку"
    else:
        filename = ""
        if phone[0] != "+":
            phone = "+" + phone

        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        con = sqlite3.connect('example.db')
        cur = con.cursor()

        sql = f'''
        INSERT INTO Contacts (Name, Surname, Phone, Address, Url, Photo, Country, Town, Street) VALUES
        ("{name}", "{surname}", "{phone}", "{address}", "{url}", "{filename}", "{country}", "{town}", "{street}");
        '''

        cur.execute(sql)
        con.commit()
        con.close()
        return 'contact_create'

@app.route("/contacts/<id>", methods=["PUT"])
def contact_update(id):
    name = request.form.get("name")
    surname = request.form.get("surname")
    phone = request.form.get("phone")
    address = request.form.get("address")
    url = request.form.get("url")
    country = request.form.get("country")
    town = request.form.get("town")
    street = request.form.get("street")

    con = sqlite3.connect('example.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    sql1 = f'''
            SELECT * FROM Contacts WHERE ID = {id};
        '''

    cur.execute(sql1)
    result = cur.fetchone()
    filename = ""


    if result is None:
        return "Такого ID не существует", 404
    else:
        contact = dict(result)
        if contact["Photo"] is not None and contact["Photo"] != "":
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], contact["Photo"]))

        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        sql = f'''
            UPDATE Contacts
            SET Name = '{name}', Surname = '{surname}', Phone= '{phone}',
            Address = '{address}', Url = '{url}', Photo = '{filename}', Country = '{country}',
            Town = '{town}', Street = '{street}'
            WHERE ID = {id};
            '''

        cur.execute(sql)
        con.commit()
        con.close()
        return 'contact_update'

@app.route("/contacts/<id>", methods=["DELETE"])
def contact_delete(id):
    con = sqlite3.connect('example.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    sql1 = f'''
    SELECT * FROM Contacts WHERE ID = {id};
    '''

    cur.execute(sql1)
    result = cur.fetchone()

    if result is None:
        return "Такого ID не существует", 404
    else:
        contact = dict(result)
        if contact["Photo"] is not None and contact["Photo"] != "":
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], contact["Photo"]))

        sql = f'''
            DELETE FROM Contacts 
            WHERE ID='{id}';
            '''

        cur.execute(sql)
        con.commit()
        con.close()
        return 'contact_delete'

app.run(debug=True)


