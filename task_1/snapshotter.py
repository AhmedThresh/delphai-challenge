import os
import subprocess
from pymongo import MongoClient

class Snapshotter:
    """
    A class to represent a snapshotter object responsible for taking snapshots
    of all nodes in a DB cluster in a consistent way.
    
    Attributes
    ----------
    mongo_client : MongoClient
        The MongoDB client used to interact with MongoDB cluster.

    Methods
    -------
    snapshot_all_nodes():
        Snapshot all nodes in a MongoDB cluster.
    snapshot_node(node_name=""):
        Snapshot a specific node in a MongoDB cluster.
    discover_nodes():
        Discover all nodes in a MongoDB cluster.
    """
    mongo_client: MongoClient

    def __init__(self, mongo_client):
        """
        Constructs all the necessary attributes for the snapshotter object.

        Parameters
        ----------
            mongo_client : MongoClient
                The MongoDB client used to interact with MongoDB cluster.
        """
        self.mongo_client = mongo_client

    def snapshot_all_nodes(self):
        """
        Snapshot all nodes in a MongoDB cluster.
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        nodes = self.discover_nodes()
        for node in nodes:
            self.snapshot_node(node_name=node)

    def snapshot_node(self, node_name: str):
        """
        Snapshot a specific node in a MongoDB cluster.
        Parameters
        ----------
        node_name : str, required

        Returns
        -------
        None
        """
        db = self.mongo_client.get_database()

        # Get lock on database
        try:
            print(f"--------- Getting lock on database {db.name} ------------\n")
            db.command("fsync", lock=True)
        except Exception as e:
            db.command("fsyncUnlock")
            raise Exception(f"Exception occured while getting lock on database {db.name}: {e}")

        # Execute snapshot
        script = os.path.join(os.getcwd(), "make-vm-snapshot.sh")
        res = subprocess.run([f'{script} {node_name}'], shell=True,
                            capture_output=True)
        print(f"{res.stdout} \n")
    
        # Release lock from database
        print(f"--------- Releasing lock on database {db.name} ------------\n")
        db.command("fsyncUnlock")
        print(f"--------- Lock on database {db.name} is released ------------\n")

    def discover_nodes(self) -> list[str]:
        """
        Discover all nodes in a MongoDB cluster.
        Parameters
        ----------
        None

        Returns
        -------
        nodes: list[str]
            List of nodes hostnames followed by ports. e.g: ["localhost:27017", "localhost:27018"]
        """
        nodes = []
        try:
            self.mongo_client.get.command('ping')
        except Exception as e:
            raise Exception(f"Exception occured while interacting with the database client: {e}")
        
        for node in self.mongo_client.nodes:
            nodes.append(f'{node[0]}:{node[1]}')
        return nodes
        
        
