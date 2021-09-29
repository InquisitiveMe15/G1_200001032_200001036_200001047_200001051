from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import pandas as pd
from pandas import DataFrame


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getfile", methods=['POST','GET'])
def getfile():
    if request.method == 'POST':
        textfile = request.files["textfile"]
        csvfile = request.files["csvfile"]
        csvfilename = secure_filename(csvfile.filename)
        textfilename = secure_filename(textfile.filename)

        textfile.save(os.path.join(textfilename))
        csvfile.save(os.path.join(csvfilename))

        f = open("attendance.txt",'r')
        arrayOfRollNos = []
        i = 1
        for lines in f.readlines():
          if i%2 ==0:
             arrayOfRollNos.append(lines.split(" ")[0])
             i=i+1
          else:
             i=i+1
             continue

        df = pd.read_csv('reference.csv')
        df['Attendance'] = 0

        col = ['S.No.','RollNo.','Name','Attendance']
        outputdf = pd.DataFrame(columns = col)

        j=1
        for eachrollno in df['RollNo.']:
           if str(eachrollno) in arrayOfRollNos:
              outputdf.loc[j] = [df[df['RollNo.']==eachrollno]['S.No.'].values[0],df[df['RollNo.']==eachrollno]['RollNo.'].values[0],df[df['RollNo.']==eachrollno]['Name'].values[0],1]
        
           else:
              outputdf.loc[j] = [df[df['RollNo.']==eachrollno]['S.No.'].values[0],df[df['RollNo.']==eachrollno]['RollNo.'].values[0],df[df['RollNo.']==eachrollno]['Name'].values[0],0]
        
           j=j+1

        outputfinal = outputdf.to_csv('final-attendance.csv',index=None,header=True)
        return send_file("final-attendance.csv",mimetype="text/csv",attachment_filename="final-attendance.csv", as_attachment=True)




if __name__ == "__main__":
    app.run(debug=True)