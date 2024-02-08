
import mysql.connector
import json
import jwt
import re #regular exp module->check if string in specific format or not
from flask import make_response,request
class auth_model():
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

    def token_auth(self,endpoint):
        def inner1(func):#func-represnts instance of particular method
            def inner2(*args):#any no. of arbtry arguments
                authorization=request.headers.get("authorization")
                if re.match("^Bearer *([^ ]+) *$",authorization,flags=0 ):
                    token=authorization.split(" ")[1]#to remove [bearer_space_]
                    try:
                        jwt_decoded=jwt.decode(token,"aman",algorithms="HS384")#aman=decryption key
                    except jwt.ExpiredSignatureError:
                        return make_response({"ERROR":"TOKEN EXPIRED "},401)
                    role_id=jwt_decoded['payload']['role_id']
                    self.cur.execute(f"SELECT roles FROM accessibility_view WHERE endpoint='{endpoint}'")
                    result=self.cur.fetchall()
                    if len(result)>0:
                        print(result)
                        # print(json.loads(result[0]['roles']))#stringified format-> arr
                        return func(*args)
                    else:
                        return make_response({"ERROR":"UNKNOWN_ENDPOINT"},404)
                else:
                    return make_response({"ERROR":"Invalid Token"},401)    
            return inner2
        return inner1 
    