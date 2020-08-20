# plagiarism-checker-python-api

A python-flask-restful api to check Plagiarism in given two text, and returns the value  
between 0 and 1, Uses a Machine Learning model from Spacy.

###To Start  
####Linux and Mac
sudo docker-compose build  
sudo docker up   
#### Windows
docker-compose build
docker-compose up

default url and posrt is http://0.0.0.0:5000   

###Register
http://0.0.0.0:5000/register  
expects a json with userame and password = {"username":"name","password":"password"}  
return 200 if succesfully signed in

###Detect
http://0.0.0.0:5000/detect
expects a json with username , password , text1, text2.  
{"useranem":"name","password":"password","text1":"This is a cute dog","text2":"this is a beautiful dog"}  
returns a value between 0 and 1 and a status code.
