from flask import Flask, render_template, request, url_for

from textblob import TextBlob,Word
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hellooo, World!</p>"

if __name__=='__main__':
    app.run(debug=True)
