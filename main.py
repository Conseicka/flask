import unittest
from flask import Flask
from flask import flash
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask import make_response
from flask import render_template
from flask_bootstrap import Bootstrap
from app import create_app
from app.forms import LoginForm


app= create_app()

todos = ["Comprar cafe", "Enviar solicitud de compra", "Entregar un video"]


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner().run(tests)
    


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)

@app.route("/")
def index():
    #getting user ip
    user_ip = request.remote_addr

    #redirecting from index to hello
    response = make_response(redirect("/hello"))
    #seting user_ip as cookie variable
    #response.set_cookie("user_ip", user_ip)
    session["user_ip"] = user_ip

    return response

@app.route("/hello", methods=["GET"])
def hello():
    user_ip = session.get("user_ip")
    username = session.get("username")

    context = {
        "user_ip": user_ip,
        "todos": todos,
        "username": username,
    }

    #the "**" is used to expand all the content of context and make easier to handled it in jinja2
    return render_template("hello.html", **context)
    