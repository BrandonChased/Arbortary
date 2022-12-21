from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import DATABASE
from flask import flash,session
from flask_app.models import user_model

class Visitor:
    def __init__(self,data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.tree_id = data["tree_id"]

    #********************CREATED METHODS*****************
    @classmethod
    def new_visitor(cls,data):
        query = """
            INSERT INTO visitors(user_id,tree_id)
            VALUES(%(user_id)s,%(tree_id)s);
        """

        return connectToMySQL(DATABASE).query_db(query,data)

#********************READ METHODS********************
    @classmethod
    def get_all_tree_visitors(cls,id):
        
        data = {
            "id" : id
        }

        query = """
            SELECT * FROM visitors
            JOIN users ON visitors.user_id = users.id
            WHERE tree_id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query,data)

        visitors = []

        if results:
            for result in results:
                visitor = cls(result)
                data = {
                    **result,
                    "id" : result["users.id"],
                    "created_at" : result["users.created_at"],
                    "updated_at" : result["users.updated_at"]
                }

                visitor.user = user_model.User(data)


                visitors.append(visitor)
        
        return visitors

#********************DELETE METHODS******************

#********************DELETE ONE Visitor******************
    @classmethod
    def delete_visitor(cls,id):
        
        data = {
            "user_id" : session["uid"],
            "tree_id" : id
        }

        query="""
            DELETE FROM visitors 
            WHERE user_id = %(user_id)s AND tree_id = %(tree_id)s;
        """

        return connectToMySQL(DATABASE).query_db(query,data)

#********************DELETE ALL Visitor METHODS*****************

    @classmethod
    def delete_visitors(cls,id):
        
        data = {
            "id" : id
        }

        query="""
            DELETE FROM visitors 
            WHERE tree_id = %(id)s;
        """

        return connectToMySQL(DATABASE).query_db(query,data)