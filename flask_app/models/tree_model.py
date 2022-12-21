from flask_app import DATABASE
from flask_app.config.mysqlconnections import connectToMySQL
from flask_app.models import user_model
from flask import flash
from flask_app.models.visitor_model import Visitor

class Tree:
    def __init__(self,data):
        self.id = data["id"]
        self.species = data["species"]
        self.location = data["location"]
        self.date_planted = data["date_planted"]
        self.reason = data["reason"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

#********************CREATE METHODS*****************

#******** create a tree********
    @classmethod
    def create_tree(cls,data):
        query = """
            INSERT INTO trees(species,location,date_planted,reason,user_id)
            VALUES(%(species)s,%(location)s,%(date_planted)s,%(reason)s,%(user_id)s);
        """

        return connectToMySQL(DATABASE).query_db(query,data)

#********************READ METHODS*****************

#**** get one tree****

    @classmethod
    def get_tree(cls,data):

        query = """
            SELECT * FROM trees
            WHERE id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query,data)

        if results:
            return cls(results[0])


#********get all users trees**********

    @classmethod
    def get_all_user_trees(cls,data):
        query = """
            SELECT * FROM trees
            WHERE user_id = %(id)s;
        """
        
        trees = []

        results = connectToMySQL(DATABASE).query_db(query,data)

        if results: 
            for row in results:
                this_tree = cls(row)
                trees.append(this_tree)

            return trees
        return[]

#******* get all tree**********
    @classmethod
    def get_all_trees(cls):
        query = """
            SELECT * FROM trees;
        """
        
        trees = []

        results = connectToMySQL(DATABASE).query_db(query)

        if results: 
            for row in results:
                this_tree = cls(row)
                trees.append(this_tree)

            return trees
        return[]


#****** get all trees with user and total visitors*****

    @classmethod
    def get_all_trees_with_user(cls):

        query = """
            SELECT * FROM trees
            JOIN users ON trees.user_id = users.id;
        """

        trees = []

        results = connectToMySQL(DATABASE).query_db(query)

        if results:
            for result in results:
                # print(result)
                tree = cls(result)
                data = {
                    **result,
                    "id" : result["users.id"],
                    "created_at" : result["users.created_at"],
                    "updated_at" : result["users.updated_at"]
                }

                tree.visitors = Visitor.get_all_tree_visitors(tree.id)
                tree.user = user_model.User(data)
                trees.append(tree)
            return trees
        return []

#********** get user with tree

    @classmethod
    def get_user_with_tree(cls,data):
        query = """
            SELECT * FROM trees
            JOIN users ON trees.user_id = users.id
            WHERE trees.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query,data)

        result = results[0]
        if result:
            tree = cls(results[0])
            
            data = {
                **result,
                "id" : result["user_id"],
                "created_at" : result["users.created_at"],
                "updated_at" : result["users.updated_at"]
            }


            Tree.user = user_model.User(data)

            # Tree.likes = Like.get_all_tree_likes(tree.id)


            return tree

#********************UPDATE METHODS*****************


    @classmethod
    def update_tree(cls,data):

        query = """
            UPDATE trees
            SET species  =  %(species)s,
            location = %(location)s,
            date_planted = %(date_planted)s,
            reason = %(reason)s
            WHERE id = %(id)s;
        """

        return connectToMySQL(DATABASE).query_db(query,data)

#********************DELETE METHODS*****************

#******** delete a tree********

    @classmethod
    def delete_tree(cls,id):
        
        data = {
            "id" : id
        }

        query="""
            DELETE FROM trees 
            WHERE id = %(id)s;
        """

        return connectToMySQL(DATABASE).query_db(query,data)


#*******************VALIDATIONS******************

    @staticmethod
    def form_validations(data):
        is_valid = True
        if len(data["species"]) < 4:
            flash("Species must be at least 5 characters","form")
            is_valid = False
        if len(data["location"]) < 1:
            flash("Location must be at least 2 character.","form")
            is_valid = False
        if len(data["date_planted"]) != 10:
            flash("Must enter a valid date","form")
            is_valid = False
        if len(data["reason"]) > 50:
            flash("Reason must be less than 50 characters","form")
            is_valid = False

        return is_valid
