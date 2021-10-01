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
        df = pd.read_csv('reference.csv')
        df['Attendance'] = 0

        col = ['S.No.', 'RollNo.', 'Name', 'Attendance']
        proxydf = pd.DataFrame(columns=col)

        
        nameInAttendance=""
        rollno=""
        while True:
            line1 = f.readline()
            line2 = f.readline()
            if not  line1:
                break
            arrayOfNames.append(re.split('\d+',line1)[0])
            nameInAttendance=arrayOfNames[-1].split(" ")[0]

            # print(nameInAttendance.upper())
            arrayOfRollNos.append(line2.split(" ")[0])
            rollno=arrayOfRollNos[-1]
            # print(type(df['RollNo.']))
            # print(rollno)
            
            name = df[df['RollNo.'] == int(rollno)]['Name'].values[0] #DOUBT!!!!!!!!
            SNo = df[df['RollNo.'] == int(rollno)]['S.No.'].values[0] #DOUBT!!!!!!!!
            # print(name)
            # print(SNo)
            # print(type(SNo))
            check = False
            if str(rollno) in proxyStudents:
                check = True
            
            if bool(nameInAttendance.upper()==str(name.split(" ")[0])):
                if check == False:
                    # df[df['RollNo.'] == int(rollno)]['Attendance'].values[0]=1
                    # df.loc[j] = [df[df['RollNo.']==rollno]['S.No.'].values[0],df[df['RollNo.']==rollno]['RollNo.'].values[0],df[df['RollNo.']==rollno]['Name'].values[0],1]
                    # df.loc[df['S.No.']==int(SNo),'Attendance']=1
                    # print("YES")
                    df.iloc[SNo-1,-1]=1
            else:
                if check == False:
                    # df.loc[j] = [df[df['RollNo.']==rollno]['S.No.'].values[0],df[df['RollNo.']==rollno]['RollNo.'].values[0],df[df['RollNo.']==rollno]['Name'].values[0],-10]
                    # df[df['RollNo.'] == int(rollno)]['Attendance'].values[0]=-10
                    # df.loc[df['S.No.']==int(SNo),'Attendance']=-10
                    # print("NO")
                    proxyRollNo = df[str(df['Name']).split(" ")[0] == str(nameInAttendance.upper())]['RollNo.'].values[0]
                    print(type(proxyRollNo))
                    SNo1 = df[df['RollNo.'] == int(proxyRollNo)]['S.No.'].values[0]
                    # df.iloc[SNo-1,-1]=-10
                    df.iloc[SNo1-1,-1]=-10
                    # proxyStudents.append(rollno)
                    proxyStudents.append(proxyRollNo)
            
        # outputfinal = df.to_csv('final-attendance.csv', index=None,header=True)
        # return send_file("final-attendance.csv", mimetype="text/csv",attachment_filename="final-attendance.csv", as_attachment=True)
        proxydf = df[df['Attendance']==-10]
        filtereddf = proxydf
        return render_template("filteredtable.html",filtereddf = filtereddf)
        

if __name__ == "__main__":
    app.run(debug=True)
