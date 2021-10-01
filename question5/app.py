from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import pandas as pd
from pandas import DataFrame
import re


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/getfile", methods=['POST', 'GET'])
def getfile():
    if request.method == 'POST':
        textfile = request.files["textfile"]
        csvfile = request.files["csvfile"]
        csvfilename = secure_filename(csvfile.filename)
        textfilename = secure_filename(textfile.filename)

        textfile.save(os.path.join(textfilename))
        csvfile.save(os.path.join(csvfilename))

        f = open("attendance.txt", 'r')
        arrayOfRollNos = []
        arrayOfNames = []
       

        df = pd.read_csv('reference.csv')
        df['Attendance'] = 0


        first = 1
        nameInAttendance=""
        rollno=""
        while True:
            line1 = f.readline()
            line2 = f.readline()
            if not  line1:
                break
            arrayOfNames.append(re.split('\d+',line1)[0])
            nameInAttendance=arrayOfNames[-1].split(" ")[0]
            if first == 1:
                nameInAttendance=nameInAttendance[3:]
                first = first + 1
            arrayOfRollNos.append(line2.split(" ")[0])
            rollno=arrayOfRollNos[-1]

            present = False
            for j in list(df['RollNo.']):
                if j == int(rollno):
                    present = True
                    break
            if present == True:

                name = df[df['RollNo.'] == int(rollno)]['Name'].values[0] 
                SNo = df[df['RollNo.'] == int(rollno)]['S.No.'].values[0] 
                
                
                proxyNAME = []   
                if bool(nameInAttendance.upper()==str(name.split(" ")[0])):
                    if df[df['RollNo.'] == int(rollno)]['Attendance'].values[0] != -10:
                        df.iloc[SNo-1,-1]=1
                    
                else:
                    proxyName = ""
                    flag = False
                    for i in list((df['Name'])):
                        if str(i).split(" ")[0] == str(nameInAttendance.upper()):
                            proxyName = i
                            proxyNAME.append(i)
                            flag = True

                    if flag == True:
                        proxyRollNo = df[df['Name'] == str(proxyName)]['RollNo.'].values[0]
                        SNo1 = df[df['RollNo.'] == int(proxyRollNo)]['S.No.'].values[0]
                        df.iloc[SNo1-1,-1]=-10

        outputfinal = df.to_csv('final-attendance.csv', index=None,header=True)
        return send_file("final-attendance.csv", mimetype="text/csv",attachment_filename="final-attendance.csv", as_attachment=True)
        

if __name__ == "__main__":
    app.run(debug=True)
