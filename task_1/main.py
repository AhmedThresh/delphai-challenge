import sys
from mongo_db_client import MongoDBClient
from snapshotter import Snapshotter

if __name__ == "__main__":
    mongodb_connection_string = sys.argv[1]
    client = MongoDBClient.Instance(connection_string=mongodb_connection_string).db_client
    snapshotter = Snapshotter(mongo_client=client)
    snapshotter.snapshot_all_nodes()
    client.close()



