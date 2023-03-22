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

#komentaras, skirtas patikrinti commit 


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
        if (args): #b00l if, if (args != NULL)
            array.append(args)
            insert_into_db(args)
            print(array)
        return render_template('./notes.html', note = select_from_db() )
    else:
        return render_template('./notes.html', note= select_from_db())

@app.route("/registracija", methods=["GET", "POST"])
def registracija():
    rez = ""
    if(request.method =="POST"):
        usern = request.form.get("username")
        passw = request.form.get("password")
        if (usern and passw):
             rez = insert_into_user_db(usern, passw)
             print(usern,passw)
        
    return render_template('./reg.html', status = rez )
         
    
def createUserDB():
        connection=sqlite3.connect("./Registracija.db")
        cursor=connection.cursor()

        createTableString = """CREATE TABLE IF NOT EXISTS Users (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )"""
        cursor.execute(createTableString)

def insert_into_user_db(username, password):
    conn=sqlite3.connect("./Registracija.db")
    reg = "Registruoti vartotojo nepavyko"
    queryString="""
        INSERT INTO Users (username, password) VALUES (?,?) 
    """
    cur = conn.cursor()
    try:
         cur.execute(queryString,(username,password))
         reg = "Registracija sekminga"

    except sqlite3.IntegrityError as e:
         print(e)
         reg = "Registruoti vartotojo nepavyko"
         print(reg)

    conn.commit()
    return reg



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
    createUserDB()
    app.run(debug="true")