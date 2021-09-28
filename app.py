from flask import Flask, render_template,request,url_for
from flask_bootstrap import Bootstrap 
from textblob import TextBlob,Word

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/analyse',methods=['POST'])
def analyse():
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		blob = TextBlob(rawtext)
		received_text2 = blob
		blob_sentiment,blob_subjectivity = blob.sentiment.polarity ,blob.sentiment.subjectivity
		
	return render_template('index.html',received_text = received_text2,blob_sentiment=blob_sentiment,blob_subjectivity=blob_subjectivity)

if __name__ == '__main__':
	app.run(debug=True)