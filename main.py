import unittest
from flask import Flask
from flask import flash
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask import make_response
from flask import render_template
#from flask.app.firestore_service import delete_todo
from flask_bootstrap import Bootstrap
from flask_login import login_required
from flask_login import current_user
from app import create_app
from app.forms import TodoForm, DeleteTodoForm
from app.firestore_service import get_users, get_todos, put_todo, delete_todo


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

@app.route("/hello", methods=["GET","POST"])
@login_required
def hello():
    user_ip = session.get("user_ip")
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()

    context = {
        "user_ip": user_ip,
        "todos": get_todos(user_id=username),
        "username": username,
        "todo_form": todo_form,
        "delete_form": delete_form
    }
    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)

        flash("La tarea se creo con exito!")

        return redirect(url_for("hello"))

    #the "**" is used to expand all the content of context and make easier to handled it in jinja2
    return render_template("hello.html", **context)
    
@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))