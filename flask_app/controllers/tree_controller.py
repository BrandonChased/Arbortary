from flask import session,redirect,render_template,flash,request
from flask_app.models.tree_model import Tree
from flask_app import app
from flask_app.models.visitor_model import Visitor

@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        flash("ACCESS DENIED", "login")
        return redirect("/")

    trees = Tree.get_all_trees_with_user()
    return render_template("dashboard.html", trees = trees)

#*********************My trees PAGE**********************
@app.route("/user/account")
def my_trees():
    
    if "email" not in session:
        flash("ACCESS DENIED", "login")
        return redirect("/")

    trees = Tree.get_all_user_trees({"id" : session["uid"]})

    return render_template("my_trees.html",trees = trees)


#*********************CREATE Tree PAGE**********************

@app.route("/create_tree")
def create_Tree_page():
    if "email" not in session:
        flash("ACCESS DENIED", "login")
        return redirect("/")

    return render_template("new.html")


#*********************VIEW Tree PAGE**********************

@app.route("/view_tree/<int:id>")
def view_Tree(id):
    if "email" not in session:
        return redirect("/")
    
    tree = Tree.get_user_with_tree({"id" : id})

    visitors = Visitor.get_all_tree_visitors(id)
    print(visitors)

    return render_template("view.html", tree = tree,visitors = visitors)

#*********************CREATE A NEW Tree**********************

@app.route("/add/tree", methods=["POST"])
def create_Tree():
    if "email" not in session:
        flash("ACCESS DENIED", "login")
        return redirect("/")
    
    if not Tree.form_validations(request.form):
        return redirect("/create_tree")

    data = {
        **request.form,
        "user_id" : session["uid"]
    }

    Tree.create_tree(data)
    return redirect("/dashboard")

    #*********************EDIT Tree PAGE**********************

@app.route("/edit/tree/<int:id>")
def edit_tree_page(id):
    if "email" not in session:
        flash("ACCESS DENIED","login")
        return redirect("/")

    tree = Tree.get_tree({"id" : id})

    return render_template('edit.html',tree= tree)


#*********************EDIT Tree**********************

@app.route("/edit_tree/<int:id>",methods=["POST"])
def edit_tree(id):
    if "email" not in session:
        flash("ACCESS DENIED","login")
        return redirect("/")

    if not Tree.form_validations(request.form):
        return redirect(f"/edit/tree/{id}")

    data = {
        **request.form,
        "id" : id
    }

    Tree.update_tree(data)

    return redirect("/dashboard")

#*********************DELETE tree**********************

@app.route("/del/tree/<int:id>")
def delete_tree(id):
    if "email" not in session:
        flash("ACCESS DENIED","login")
        return redirect("/")
    
    Visitor.delete_visitors(id)

    Tree.delete_tree(id)

    return redirect("/dashboard")