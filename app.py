from flask import Flask,render_template,request,Response,url_for
import joblib
from tensorflow.keras.preprocessing.sequence import pad_sequences
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/submit",methods=["POST"])
def submit():
    r = 2
    result = ""
    model = joblib.load("Models/Model.pkl")
    tokens = joblib.load("Models/Tokens.pkl")
    if request.method=="POST":
        review = request.form.get("review")
        if len(review) > 1:
            f = review.split(" ")
            new_st = [" ".join(f)]
            new_ts = tokens.texts_to_sequences(new_st)
            new_ts = pad_sequences(new_ts,maxlen=500,padding="post") 
            predict = model.predict(new_ts)
            if predict >= 0.4:
                  r = 1
                  result = "A POSITIVE REVIEW."
                  print(predict)
                  print("positive")

            elif predict >= 0.2 and predict <= 0.4:
                  r = 2
                  result = "A NEUTRAL REVIEW."
                  print(predict)
                  print("neutral")
            else:
                  r = -1
                  result = "A NEGATIVE REVIEW."
                  print(predict)
                  print("negative")

            return render_template("home.html",r=r,result=result)
        else:
             return render_template("home.html",result="Insufficient Data/try adding more sequences of your review.")
            
    return render_template("home.html")