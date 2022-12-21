from flask_app import app
from flask import session, redirect,flash
from flask_app.models.visitor_model import Visitor


#*********************ADD A NEW visitor**********************

@app.route("/add/visitor/<int:id>")
def add_visitor(id):

    if "email" not in session:
        flash("ACCESS DENIED", "login")
        return redirect("/")

    data = {
        "user_id" : session["uid"],
        "tree_id" : id
    }
    
    Visitor.new_visitor(data)
    return redirect("/dashboard")