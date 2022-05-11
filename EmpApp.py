from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb 

)
output = {}
table = 'student'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('AddEmp.html')


@app.route("/addemployee", methods=['GET','POST'])
def AddEmployee():
    return render_template('AddEmp.html')

@app.route("/getemployee", methods=['GET','POST'])
def GetEmployee():
    return render_template('GetEmp.html')

@app.route("/fetchdata", methods=['POST'])
def GetEmp():
    net_id = request.form['net_id']
    select_sql = "SELECT * FROM student where empid= %s"
    cursor = db_conn.cursor()
    try:
        cursor.execute(select_sql, (net_id))
        myresult = cursor.fetchall()
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        # print(myresult)
    # return ''
    # return render_template('AddEmpOutput.html', name=emp_name)
    
    return render_template('GetEmpOutput.html',name = myresult)
  
@app.route("/addemp", methods=['POST'])
def AddEmp():
    net_id = request.form['net_id']
    name = request.form['name']
    current_job = request.form['current_job']
    plan = request.form['plan']
    working = request.form['working']
    

    insert_sql = "INSERT INTO student VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    

    try:

        cursor.execute(insert_sql, (net_id, name, current_job, plan, working))
        db_conn.commit()
        emp_name = "" + name + " " 
        # Uplaod image file in S3 #
        #emp_image_file_name_in_s3 = "emp-id-" + str(net_id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            #s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket
                )

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', name=emp_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)