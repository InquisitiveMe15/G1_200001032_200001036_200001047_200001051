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
        arrayOfNames = []
        i = 1
        for lines in f.readlines():
          if i%2 ==0:
             arrayOfRollNos.append(lines.split(" ")[0])
             i=i+1
          else:
             arrayOfNames.append(re.split('\d+',lines)[0])
             i=i+1
             continue

        newArraySorted=sorted(arrayOfNames)
        listOfWhoputProxy=[]
        for i in newArraySorted:
          if newArraySorted.count(i)>1:
             listOfWhoputProxy.append(i)
             for c in range(newArraySorted.count(i)):
                for j in newArraySorted:
                    if i==j and newArraySorted.count(i)>1:
                        newArraySorted.remove(i)

        combinedArray=[[arrayOfNames[i],arrayOfRollNos[i]] for i in range(len(arrayOfRollNos))]
        listOfrollNoToPutzero=[]
        for i in combinedArray:
            if str(i[0]) in listOfWhoputProxy:
                listOfrollNoToPutzero.append(i[1])
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
        k=1  
        for eachrollno in df['RollNo.']:
           if str(eachrollno) in listOfrollNoToPutzero:
              outputdf.loc[k] = [df[df['RollNo.']==eachrollno]['S.No.'].values[0],df[df['RollNo.']==eachrollno]['RollNo.'].values[0],df[df['RollNo.']==eachrollno]['Name'].values[0],0]
           k=k+1
        outputfinal = outputdf.to_csv('final-attendance.csv',index=None,header=True)
        
        filtereddf = pd.DataFrame(columns=["Name","RollNo."])
        p = 1
        for eachname in listOfWhoputProxy:
           filtereddf.loc[p] = [(df[df['Name']==eachname.upper()]['Name'].values[0]),(df[df['Name']==eachname.upper()]['RollNo.'].values[0])]
           p = p+1

        #return send_file("final-attendance.csv",mimetype="text/csv",attachment_filename="final-attendance.csv", as_attachment=True)
        return render_template("filteredtable.html",filtereddf=filtereddf)




if __name__ == "__main__":
    app.run(debug=True)