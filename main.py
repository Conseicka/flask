from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__,template_folder='templates', static_folder='./static')
bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = "SUPER SECRETO"

todos = ["Comprar cafe", "Enviar solicitud de compra", "Entregar un video"]


class LoginForm(FlaskForm):
    username = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Enviar")


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

@app.route("/hello", methods=["GET", "POST"])
def hello():
    user_ip = session.get("user_ip")
    login_form = LoginForm()
    username = session.get("username")

    context = {
        "user_ip": user_ip,
        "todos": todos,
        "login_form": login_form,
        "username": username,
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session["username"] = username
        
        flash("Nombre de usuario registrado con exito!")

        return redirect("/hello")

    #the "**" is used to expand all the content of context and make easier to handled it in jinja2
    return render_template("hello.html", **context)
    