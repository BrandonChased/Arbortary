from flask_app import app

from flask_app.controllers import user_controller,tree_controller,visitor_controller


if __name__ == "__main__":
    app.run(debug=True)