from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__,static_url_path='')
connection=sqlite3.connect("./NotesDatabase.db")

variable = 0
array = []
@app.route("/")
def mano_funkcija():
    return ("Labas")

@app.route("/test")
def test_route():
    return render_template('./index.html', var=plus_one)



@app.route("/debug")
def plus_one():
    global variable
    variable = variable + 1
    return str(variable)

@app.route("/notes", methods=["GET","POST"])
def notes():
    if(request.method == "POST"):
        global array
        args = request.form.get("note2")
        if (args):
            array.append(args)
            insert_into_db(args)
            print(array)
        return render_template('./notes.html', note = select_from_db() )
    else:
        return render_template('./notes.html', note= select_from_db())
    

def createDB():
        connection=sqlite3.connect("./NotesDatabase.db")
        cursor=connection.cursor()

        createTableString = """CREATE TABLE IF NOT EXISTS Sheets (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL
        )"""

        createNotesTableString = """CREATE TABLE IF NOT EXISTS Notes (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            SheetId ,
            Header TEXT,
            Text TEXT,
            FOREIGN KEY (SheetId) REFERENCES Sheets(ID)
        )"""

        cursor.execute(createTableString)
        cursor.execute(createNotesTableString)

def insert_into_db(note):
    conn=sqlite3.connect("./NotesDatabase.db")
    queryString="""
        INSERT INTO Sheets (Name) VALUES (?) 
    """
    cur = conn.cursor()
    cur.execute(queryString,(note,))
    conn.commit()

def select_from_db():
    conn=sqlite3.connect("./NotesDatabase.db")
    queryString="""
        SELECT name from Sheets
    """
    cur = conn.cursor()
    array = cur.execute(queryString).fetchall()
    return array



if __name__ == "__main__":
    createDB()
    app.run(debug="true")