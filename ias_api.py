### imports 
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import pyodbc

### initializations
app = Flask(__name__)
api = Api(app)
global conn
conn = pyodbc.connect('Driver={SQL Server};'
                    'Server=76S-ZEPHYRUS;'
                    'Database=db;'
                    'UID=ias_py_server_user;'
                    'PWD=admin1234;'
                    'Trusted_Connection=no;')
global cursor
cursor = conn.cursor()

### classes
class InventoryList(Resource):
    def get(self):
        query = "SELECT * FROM inventoryList"
        data = pd.read_sql(query,conn)                  
        data = data.to_dict()                           
        return {'data': data}, 200                      

    def post(self):
        parser = reqparse.RequestParser()  
        parser.add_argument('itemName', required=True)  
        parser.add_argument('quantity', required=True)
        args = parser.parse_args()  

        # read data
        query = "SELECT * FROM inventoryList"
        data = pd.read_sql(query,conn) 
        
        if args['itemName'] in list(data['itemName']):
            return {
                'message': f"'{args['itemName']}' already exists."
            }, 409
        else:
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'itemName': [args['itemName']],
                'quantity': [args['quantity']]
            })
            
            # add the newly provided values
            
            cursor.execute("INSERT INTO inventoryList VALUES (?,?)", args['itemName'], args['quantity'])
            conn.commit()
            return {'data': new_data.to_dict()}, 200  # return data with 200 OK

    def patch(self):
        parser = reqparse.RequestParser()  
        parser.add_argument('itemName', required=True)  
        parser.add_argument('quantity', required=True)
        args = parser.parse_args()  

        # read data
        query = "SELECT * FROM inventoryList"
        data = pd.read_sql(query,conn) 
        
        if args['itemName'] in list(data['itemName']):
            cursor.execute("UPDATE inventoryList SET quantity = ? WHERE itemName = ? ", args['quantity'],  args['itemName'])
            conn.commit()
              
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'itemName': [args['itemName']],
                'quantity': [args['quantity']]
            })
            return {'data': new_data.to_dict()}, 200

        else:
            # otherwise the itemName does not exist
            return {
                'message': f"'{args['itemName']}' user not found."
            }, 404

    def delete(self):
        parser = reqparse.RequestParser()  
        parser.add_argument('itemName', required=True)  
        args = parser.parse_args()  

        # read data
        query = "SELECT * FROM inventoryList"
        data = pd.read_sql(query,conn) 
                
        if args['itemName'] in list(data['itemName']):
            # remove data entry matching given itemName
            cursor.execute("DELETE FROM inventoryList WHERE itemName = (?)", args['itemName'])
            conn.commit()

            # return data and 200 OK
            new_data = pd.DataFrame({
                'itemName': [args['itemName']]
            })
            return {'data': new_data.to_dict()}, 200

        else:
            # otherwise we return 404 because userId does not exist
            return {
                'message': f"'{args['itemName']}' user not found."
            }, 404



class ShoppingList(Resource):
    def get(self):
        query = "SELECT * FROM shoppingList"
        data = pd.read_sql(query,conn)                  
        data = data.to_dict()                           
        return {'data': data}, 200                      

    def post(self):
        parser = reqparse.RequestParser()  
        parser.add_argument('itemName', required=True)  
        parser.add_argument('quantity', store_missing=False)
        args = parser.parse_args()  

        # read data
        query = "SELECT * FROM shoppingList"
        data = pd.read_sql(query,conn) 
        
        if args['itemName'] in list(data['itemName']):
            return {
                'message': f"'{args['itemName']}' already exists."
            }, 409
        else:
            # add the newly provided values
            if 'quantity' in args:
                cursor.execute("INSERT INTO shoppingList (itemName, quantity) VALUES (?,?)", args['itemName'], args['quantity'])
            else:
                cursor.execute("INSERT INTO shoppingList (itemName) VALUES (?)", args['itemName'])
            conn.commit()

            # return data with 200 OK
            new_data = pd.DataFrame({
                'itemName': [args['itemName']]
            })
            return {'data': new_data.to_dict()}, 200  

    def patch(self):
        parser = reqparse.RequestParser()  
        parser.add_argument('itemName', required=True)  
        parser.add_argument('quantity', store_missing=False)
        parser.add_argument('purchased', store_missing=False)
        args = parser.parse_args()  

        # read data
        query = "SELECT * FROM shoppingList"
        data = pd.read_sql(query,conn) 
        
        if args['itemName'] in list(data['itemName']):
            if 'quantity' in args:
                cursor.execute("UPDATE shoppingList SET quantity = ? WHERE itemName = ? ", args['quantity'],  args['itemName'])
            if 'puchased' in args:
                cursor.execute("UPDATE shoppingList SET purchased = 1 WHERE itemName = ? ", args['itemName'])
            conn.commit()

            # return data with 200 OK
            new_data = pd.DataFrame({
                'itemName': [args['itemName']]
            })
            return {'data': new_data.to_dict()}, 200

        else:
            # otherwise the itemName does not exist
            return {
                'message': f"'{args['itemName']}' user not found."
            }, 404

    def delete(self):
        parser = reqparse.RequestParser()  
        parser.add_argument('itemName', required=True)  
        args = parser.parse_args()  

        # read data
        query = "SELECT * FROM shoppingList"
        data = pd.read_sql(query,conn) 
                
        if args['itemName'] in list(data['itemName']):
            # remove data entry matching given itemName
            cursor.execute("DELETE FROM shoppingList WHERE itemName = (?)", args['itemName'])
            conn.commit()
            
            # return data and 200 OK
            new_data = pd.DataFrame({
                'itemName': [args['itemName']]
            })
            return {'data': new_data.to_dict()}, 200

        else:
            # otherwise we return 404 because userId does not exist
            return {
                'message': f"'{args['itemName']}' user not found."
            }, 404


api.add_resource(InventoryList, '/inventorylist')  # add endpoints
api.add_resource(ShoppingList, '/shoppinglist')

if __name__ == '__main__':
    app.run()  # run our Flask app