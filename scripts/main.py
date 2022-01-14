from flask import Flask, request, make_response, redirect

app = Flask(__name__)

@app.route("/")
def index():
    #getting user ip
    user_ip = request.remote_addr

    #redirecting from index to hello
    response = make_response(redirect("/hello"))
    #seting user_ip as cookie variable
    response.set_cookie("user_ip", user_ip)

    return response

@app.route("/hello")
def hello():
    user_ip = request.cookies.get("user_ip")

    return f"Hello World Flask {user_ip}"