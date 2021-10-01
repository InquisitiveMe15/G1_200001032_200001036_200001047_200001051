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
        proxyStudents = []

        #Doubt!!!!!!!!!!!!!!!!!!
        # test = list(pd.read_csv('reference.csv'))
        df = pd.read_csv('reference.csv')
        # df = pd.DataFrame(test, columns = ['S.no.','RollNo.','Name','Attendance'])
        df['Attendance'] = 0

        col = ['S.No.', 'RollNo.', 'Name', 'Attendance']
        proxydf = pd.DataFrame(columns=col)

        # i = 1
        j = 1
        nameInAttendance=""
        rollno=""
        while True:
            line1 = f.readline()
            line2 = f.readline()
            if not  line1:
                break
        # for lines in f.readlines():
            # flag = 0
            # if i % 2 != 0:
            arrayOfNames.append(re.split('\d+',line1)[0])
            nameInAttendance=arrayOfNames[-1]
            print(nameInAttendance)
                # i = i+1
            # else:
            arrayOfRollNos.append(line2.split(" ")[0])
            rollno=arrayOfRollNos[-1]
                # i = i+1
                # flag = 1
            # print("neha")
            # print(type(df['RollNo.']))
            # if flag == 1:
            print(rollno)
                # print(type(rollno))
            name = df[df['RollNo.'] == int(rollno)]['Name'].values[0] #DOUBT!!!!!!!!
            SNo = df[df['RollNo.'] == int(rollno)]['S.No.'].values[0] #DOUBT!!!!!!!!
            print(name)
            check = False
            if str(rollno) in proxyStudents:
                check = True
            
            if bool(nameInAttendance.upper()==str(name)):
                if check ==False:
                    # df[df['RollNo.'] == int(rollno)]['Attendance'].values[0]=1
                    # df.loc[j] = [df[df['RollNo.']==rollno]['S.No.'].values[0],df[df['RollNo.']==rollno]['RollNo.'].values[0],df[df['RollNo.']==rollno]['Name'].values[0],1]
                    df.loc[int(SNo)-1,'Attendance']=1
            else:
                if check ==False:
                    # df.loc[j] = [df[df['RollNo.']==rollno]['S.No.'].values[0],df[df['RollNo.']==rollno]['RollNo.'].values[0],df[df['RollNo.']==rollno]['Name'].values[0],-10]
                    # df[df['RollNo.'] == int(rollno)]['Attendance'].values[0]=-10
                    df.loc[int(SNo)-1,'Attendance']=-10
                    proxyStudents.append(rollno)
            
            j = j+1
        # outputfinal = df.to_csv('final-attendance.csv', index=None,header=True)
        proxydf = df[df['Attendance']==-10]
        filtereddf = proxydf
        # return render_template("filteredtable.html",filtereddf = filtereddf)
        return send_file("final-attendance.csv", mimetype="text/csv",attachment_filename="final-attendance.csv", as_attachment=True)
        

if __name__ == "__main__":
    app.run(debug=True)
