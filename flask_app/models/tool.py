from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user

class Tool :
    db = "finance_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.trade_date = data['trade_date']
        self.asset = data['asset']
        self.position = data['position']
        self.profitorloss = data['profitorloss']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.holder = ""

    @classmethod
    def store_asset(cls,data):
        if not cls.validate_asset(cls, data):
            return False
        query= """
        INSERT INTO tool(name, trade_date, asset, position, profitorloss, user_id)
        VALUE (%(name)s, %(trade_date)s, %(asset)s, %(position)s, %(profitorloss)s, %(user_id)s);"""
        tool_id = connectToMySQL(cls.db).query_db(query, data)
        print(tool_id)
        return tool_id

    @classmethod
    def get_asset_by_id(cls,id):
        data = {'id':id}
        query = """
        SELECT *
        FROM tool
        WHERE id = %(id)s
        ;
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        # print(result[0])
        return result[0]

    @classmethod
    def get_all_assets_by_user(cls):
        data = {'user_id': id}
        # print(data['user_id'])
        query = """
        SELECT *
        FROM tool
        LEFT JOIN user
        ON user.id = tool.user_id
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        all_fiancial_tools = []
        for row in result:
            one_tool = cls(row)
            financial_tool_user = {
                'id' : row['id'],
                'first_name': row['first_name'],
                'last_name':row['last_name'],
                'email': row['email'],
                'password':row['password'],
                'created_at':row['created_at'],
                'updated_at':row['updated_at']
            }
            holder = user.User(financial_tool_user)
            one_tool.holder = holder
            all_fiancial_tools.append(one_tool)
        return all_fiancial_tools

    @classmethod
    def edit_asset(cls, data):
        if not cls.validate_asset(data):
            return False
        query ="""
        UPDATE tool
        SET name = %(name)s, trade_date = %(trade_date)s, asset = %(asset)s, position = %(position)s, profitorloss = %(profitorloss)s
        WHERE id = %(id)s
        ;
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def remove_asset(cls,id):
        data = {"id": id}
        query = """
        DELETE FROM tool
        WHERE id = %(id)s
        ;
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        return

    @staticmethod
    def validate_asset(cls,data):
        is_valid = True
        if len(data['name']) < 2:
            flash("Financial Tool Needs to be longer than 2 characters")
            is_valid= False
        if len(data['asset']) < 2:
            flash("asset type must be longer than 2 characters")
            is_valid=False
        if len(data['position']) < 2:
            flash("Position description must be longer than 2 characters")
            is_valid= False
        if data['profitorloss'] == "":
            flash("You Must indicate a Profit or a Loss")
            is_valid= False
        return is_valid
