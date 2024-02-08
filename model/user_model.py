import mysql.connector
import json
import jwt
from flask import make_response
from datetime import datetime,timedelta
class user_model():
    def __init__(self):
        #connection establish code ->create constructor
        try:
            self.con=mysql.connector.connect(host="localhost",user="root",password="",database="flask_rest")
            #commit in sql db
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("Connection Established !!")
        except:
            print("Connection Error !")
    def user_getall_model(self):
        #Query execution code
        self.cur.execute("SELECT * FROM users")
        result=self.cur.fetchall()
        if len(result)>0:
            # return json.dumps(result)
            # return make_response({"payload":result},200)
            res=make_response({"payload":result},200) 
            res.headers['Access-Control-Allow-Origin']="*"
            return res
        else:
            return make_response({"message":"No Data found"},204)
        
    def user_addone_model(self,data):
        #Query execution code
        self.cur.execute(f"INSERT INTO users(name,email,phone,role,password) VALUES ('{data['name']}', '{data['email']}', '{data['phone']}','{data['role']}','{data['password']}')")
        #print(data['name'])
        print(data)
        return make_response({"message":"User Created Successfully"},201)
    
    def user_update_model(self,data):
        #Query execution code
        self.cur.execute(f"UPDATE users SET name='{data['name']}',email='{data['email']}',phone='{data['phone']}',role='{data['role']}',password='{data['password']}' WHERE id= {data['id']}")
        if self.cur.rowcount>0:#something to be updated 
            return make_response({"message":"User updated successfully !"},201)
        else:
            return make_response({"message":"Nothing to update"},202)

    def user_delete_model(self,id):
        #Query execution code
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount>0:#something to be updated 
            return make_response({"message":"User Deleted successfully !"},200)
        else:
            return make_response({"message":"Nothing to delete"},202)

    def user_patch_model(self,data,id):#bcz passing 2 params from route func so data,id
        qry="UPDATE users SET " #update Tname set col=val,col=val where id=someid{id}
        for  key in data:
            qry += f"{key}='{data[key]}'," #append key value pairs  
        qry= qry[:-1] + f" WHERE id={id}"

        self.cur.execute(qry)
        if self.cur.rowcount>0:#something to be updated 
            return make_response({"message":"User updated successfully !"},201)
        else:
            return make_response({"message":"Nothing to update"},202)
    def user_pagination_model (self,limit ,page):
        limit=int(limit)
        page=int(page)
        start=(page*limit)-limit
        qry=f"SELECT * FROM users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result=self.cur.fetchall()
        if len(result)>0:
            res=make_response({"payload":result,"page_no":page,"limit":limit},200) 
            return res
        else:
            return make_response({"message":"No Data found"},204)
    
    def user_upload_avatar_model(self,uid,filepath):
        self.cur.execute(f"UPDATE users SET avatar='{filepath}' WHERE id={uid}")
        if self.cur.rowcount>0:#something to be updated 
            return make_response({"message":"File Uploaded successfully !"},201)
        else:
            return make_response({"message":"Nothing to update"},202)
        
    def user_login_model(self,data):
        self.cur.execute(f"SELECT id,name,email,phone,avatar,role_id FROM users WHERE email='{data['email']}' and password='{data['password']}'")
        result=self.cur.fetchall()
        userdata=result[0]
        exp_time= datetime.now() + timedelta(minutes=15)
        exp_epoch_time=int(exp_time.timestamp())
        payload={
            "payload":userdata,
            "exp": exp_epoch_time

        }
        jwtoken=jwt.encode(payload,"aman",algorithm="HS384")  #aman=encryption key
        return make_response({"token":jwtoken}, 200)
    
    

        



        
    


        


        
    

        