from flask import Flask, render_template, request, redirect
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle5 as pickle
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentmient.db'  # Replace with your database file path
db = SQLAlchemy(app)

app.app_context().push()

class Query_Sentiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(200), unique=True, nullable=False)
    sentiment = db.Column(db.String(40), unique=True, nullable=False)

    def __init__(self, query, sentiment):
        self.query = query
        self.sentiment = sentiment

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        query = request.form.get("name", "I am HAPPY")

        loaded_vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))        
        loaded_model = pickle.load(open('classification.model', 'rb'))
        sentiment = loaded_model.predict(loaded_vectorizer.transform([query]))[0]

        new_query_sentiment = Query_Sentiment(query=query, sentiment=sentiment)

        
        db.session.add(new_query_sentiment)
        db.session.commit()
        return redirect('/history')
    

        # return render_template('emotion.html', name=sentiment)
        


@app.route('/history')
def history():
    histories = Query_Sentiment.query.order_by(Query_Sentiment.id)
    return render_template("history.html", history=histories)

if __name__ == '__main__':    
    app.run(debug=True)