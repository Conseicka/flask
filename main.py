from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__,template_folder='templates')

todos = ["Comprar cafe", "Enviar solicitud de compra", "Entregar un video"]

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
    context = {
        "user_ip": user_ip,
        "todos": todos,
    }

    #the "**" is used to expand all the content of context and make easier to handled it in jinja2
    return render_template("hello.html", **context)
    