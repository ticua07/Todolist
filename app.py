from flask import Flask , render_template, request, redirect
import sqlite3
from gevent.pywsgi import WSGIServer
"""
TODO deploy to heroku
"""
conn = sqlite3.connect("TODO.db")
c = conn.cursor()

try:
    c.execute("CREATE TABLE todo (note text)")
except Exception:
    pass


app = Flask(__name__)
@app.route('/')
def main():
    return render_template('index.html', todo=c.execute("SELECT note FROM todo"), name=True)

@app.route("/add_note/", methods=["GET","POST"])
def add_note():
    if request.method == "POST":
        req = request.form
        note = req.get("add_note")
        if note.strip() == "":
            return render_template("index.html", name=False, todo=c.execute("SELECT note FROM todo"))
        c.execute(f"INSERT INTO todo VALUES ('{note}')")
        conn.commit()
        return redirect("/")
    return redirect("/")


@app.route("/delete/", methods=["POST"])
def delete():
    if request.method == "POST":
        req = request.form
        c.execute("DELETE FROM todo WHERE note = '" + req["delete"] + "';")
        conn.commit()
    return redirect("/")

@app.route("/edit/<nota>", methods=["GET","POST"])
def edit(nota):
    for i in c.execute("SELECT note FROM todo"):
        if i[0] == nota:
            return render_template("edit.html", value=nota)
        else:
            return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>.
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.bundle.min.js" integrity="sha384-LtrjvnR4Twt/qOuYxE721u19sVFLVSA4hf/rRt6PrZTmiPltdZcI7q7PXQBYTKyf" crossorigin="anonymous"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nota no encontrada :(</title>
</head>
<body>
    <div class="container-fluid">
        <div class="jumbotron" style="padding-bottom: 0.8%;">
            <h1>La nota que estabas buscando <strong>no existe</strong></h1>
            <h5>Este error no deberia ocurrir a menos que cambies el codigo fuente.</h5>
            <h5>Porfavor no hagas eso</h5>
            <br>
            <br>
            <p>Atentamente el creador: Ticua07</p>
            <form action="/" method="get"><button class="btn btn-success" type="submit">Volver</button></form>
            
        </div>
    </div>
</body>
</html>
"""

@app.route("/finaledit/<nota>", methods=["GET","POST"])
def finaledit(nota):
    if request.method == "POST":
        req = request.form
        note = req.get("edit")
        c.execute(f"""
        UPDATE todo
        SET note = '{note}'
        WHERE note = '{nota}'
        """)
        conn.commit()
        return redirect("/")
    return redirect("/")

@app.route("/search/", methods=["POST","GET"])
def search():
    """
    note == the keyword to seach
    notes == all notes to search with the keyword {note}
    notas == all the notes that has the keyword
    """
    notas = []
    notes = []
    if request.method == "POST":
        req = request.form
        note = req.get("search")
    for i in c.execute("SELECT note FROM todo"):
        notes.append(i[0])
    for i in notes:
        if note in i:
            notas.append(i)
    return render_template("search.html", notas=notas, note=note)






if __name__ == "__main__":
    """
    Ejecuta el servidor, linea 3 para ver la importacion
    ! usar solo para tests
    """
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
    conn.commit()
    conn.close()

