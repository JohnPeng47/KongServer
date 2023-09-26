from pymongo import MongoClient
from typing import Dict

class DBConnection:
    def __init__(self, host='localhost', port=8081, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.db = None
        self.connected = False

        DATABASE = "kongbot"
        self.connect(DATABASE)

    def connect(self, database):
        try:
            self.client = MongoClient(self.host, self.port)
            self.db = self.client[database]

            if self.username and self.password:
                self.db.authenticate(self.username, self.password)
            
            self.connected = True
            print(f"Connected to database '{database}'")
        except Exception as e:
            print(f"Failed to connect to database: {e}")

    def disconnect(self):
        try:
            self.client.close()
            print("Disconnected from database")
        except Exception as e:
            print(f"Failed to disconnect from database: {e}")

    def get_collection(self, collection):
        if self.connected:
            return self.db[collection]
        else:
            print("Not connected to any database")

    # does it make sense to store this on graph in separate collection?
    # thinking is, we may not want to load the full graph in mem if we just 
    # want to grab the metadata
    def insert_graph_metadata(self, graph_id: str, metadata: Dict):
        return db_conn.get_collection("graph_metadata").update_one(
            {
                "id": graph_id,
            }, {
                "$set": {
                    "metadata": metadata,
                }
            },
        upsert=True)
    
    def get_graph_metadata(self, pagination=10):
        return db_conn.get_collection("graph_metadata").find({}).sort("timestamp", -1).limit(pagination)

    def get_graph(self, graph_id: str):
        return db_conn.get_collection("graphs").find_one({
            "id": graph_id,
        })

db_conn = DBConnection()