from flask import Flask , jsonify, request
from flask_restful import Api , Resource
from pymongo import MongoClient
import bcrypt
import spacy


app = Flask(__name__)
api = Api (app)
client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["users"]

def UserExists(username):
    if users.find({"username":username}).count() == 0:
        return False
    else:
        return True


class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        if UserExists(username):
            retJson = {
            "status":301,
            "msg":"Invalid Username"
            }

            return jsonify(retJSON)
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        users.insert({
        "username":username,
        "password":hashed_pw,
        "tokens":6
        })

        retJson = {
        "status":200,
        "msg":"Signed Up succesfully"
        }

        return jsonify(retJson)

def verifyPw(username, password):
    if not UserExists(username):
        return False

    hashed_pw = users.find({"username":username})[0]['password']

    if bcrypt.hashpw(password.encode('utf-8'), hashed_pw) ==hashed_pw:
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find({"username":username})[0]["tokens"]
    return tokens


class Detect(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if not UserExists(username):
            retJson = {
            "status":"301",
            "msg":"Invalid Username"
            }
            return jsonify(retJson)

        correct_pw = verifyPw(username, password)

        if not correct_pw :
            retJson = {
            "status":"302",
            "msg":"Invalid Password"
            }
        num_tokens = countTokens(username)

        if int(num_tokens) <= 0:
            retJson = {
            "status":303,
            "msg":"Out of Tokens, Please Refil"
            }
            return jsonify(retJson)

        #Calculate the Match
        nlp = spacy.load("en_core_web_sm")
        text1 = nlp(text1)
        text2 = nlp(text2)

        ratio = text1.similarity(text2)

        retJson = {
        "status":200,
        "similarity":ratio,
        "msg":"Similarity score calculated succesfully"
        }
        current_tokens = countTokens(username)
        users.update({
        "username":username
        },{"$set":{
        "tokens":int(current_tokens) - 1
        }})

        return jsonify(retJson)



class Refil(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["admin_pw"]
        refil_amount = postedData["refill"]


        if not UserExists(username):
            retJson = {
            "status":301,
            "msg":"Invalid username"
            }
            return jsonify(retJson)

        correct_pw = "abcd123"

        if not password == correct_pw:
            retjson = {
            "status":304,
            "msg":"Invalid admin Password"
            }

        current_tokens = countTokens(username)
        users.update({"username":username},{
        "$set":{
        "tokens":refil_amount
        }
        })

        retJson = {
        "status":"200",
        "msg":"Refilled"
        }
        return jsonify(retJson)


api.add_resource(Register , "/register")
api.add_resource(Detect , "/detect")
api.add_resource(Refil , "/refill")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
