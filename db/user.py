import pyodbc, uuid

class UserDatabase:
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-66BPO70S;DATABASE=cafe')
        self.cursor = self.conn.cursor()

    def get_user(self, id):
        query = f"select * from users where id = '{id}'" 
        self.cursor.execute(query)
        user_dict = {}
        result = self.cursor.fetchone()
        if result is not None:
            user_dict["id"], user_dict["username"], user_dict["password"] = result
            return user_dict

    def add_user(self, username, password):
        query = f"insert into users(username, password) values('{username}', '{password}')" 
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except pyodbc.IntegrityError:
            return False

    def delete_user(self, id):
        query = f"delete from users where id = '{id}'" 
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def verify_user(self, username, password):
        query = f"select id from users where username = '{username}' and password = '{password}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]


# db = UserDatabase()
# db.add_user("mithlesh", "1234")
# print(db.get_user(4))
# print(db.delete_user(1))