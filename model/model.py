from pymongo import MongoClient

class ChildModel:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['childTrace']
        self.collection = self.db['members']

    def add_child(self, child_data):
        try:
            db_response = self.collection.insert_one(child_data)
            return db_response
        except Exception as ex:
            print(ex)
            return None

    def edit_child(self, child_id, updated_data):
        try:
            update_query = {'u_id': child_id}
            new_values = {
                '$set': updated_data
            }
            update = self.collection.update_one(update_query, new_values)
            return update
        except Exception as ex:
            print(ex)
            return None

    def delete_child(self, child_id):
        try:
            delete_query = {'u_id': child_id}
            delete_child = self.collection.delete_one(delete_query)
            return delete_child
        except Exception as ex:
            print(ex)
            return None
