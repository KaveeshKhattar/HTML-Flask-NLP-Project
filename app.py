from flask import Flask, render_template, request, redirect
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle5 as pickle
import sqlite3 as sql

app = Flask(__name__)

conn = sql.connect('database.db')
# print("Opened database successfully")

# conn.execute('CREATE TABLE sentiment (id INTEGER NOT NULL PRIMARY KEY, query TEXT, sentiment TEXT)')
# print("Table created successfully")

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":

        query = "Your query"
        sentiment = "Positive"


        query = request.form.get("name", "I am HAPPY")

        loaded_vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))        
        loaded_model = pickle.load(open('classification.model', 'rb'))
        sentiment = loaded_model.predict(loaded_vectorizer.transform([query]))[0]        

        try:
            with sql.connect("database.db") as con:
                # print("OK1")
                cur = con.cursor()
                # print("OK2")
                cur.execute("INSERT INTO sentiment (query, sentiment) VALUES (?,?)", (query, sentiment))
                # print("OK3")
                con.commit()
                con.close()
                # print("PASS")

        except:
            con.rollback()
            # print("FAIL")
        
        finally:
            # print("HERE WE COME")
            return redirect('/history')
    

        # return render_template('emotion.html', name=sentiment)
        


@app.route('/history')
def history():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    history = cur.execute("select * from sentiment")    

    # print(history)
    
    return render_template("history.html", history=history)


@app.route('/delete', methods=["POST"])
def delete():
    con = sql.connect("database.db")
    cur = con.cursor()

    id = request.form.get("id")
    # print("ID:", id)
    if id:
        cur.execute("DELETE FROM sentiment WHERE id = ?", [id])
        con.commit()
        con.close()

    return redirect('/history')

@app.route('/update', methods=["POST"])
def update():

    con = sql.connect("database.db")
    cur = con.cursor()

    query = request.form.get("query", "I am HAPPY")
    id = request.form.get("id", "1")
    # print("Updating ID:", id)

    if query and id:
        
        loaded_vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))        
        loaded_model = pickle.load(open('classification.model', 'rb'))
        sentiment = loaded_model.predict(loaded_vectorizer.transform([query]))[0]        

        cur.execute("UPDATE sentiment SET query = ?, sentiment = ? WHERE id = ?", (query, sentiment, id))
        con.commit()
        con.close()

    return redirect('/history')


if __name__ == '__main__':    
    app.run(debug=True)