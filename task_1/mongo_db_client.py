from pymongo import MongoClient
from singleton import Singleton


@Singleton
class MongoDBClient(object):
    """
    A class to represent a singleton MongoDBClient.

    Attributes
    ----------
    db_client : MongoClient
        The MongoDB client used to interact with MongoDB cluster.

    Methods
    -------
    None
    """
    db_client = None

    def __init__(self, connection_url: str):
        """
        Constructs all the necessary attributes for the MongoDBClient object.

        Parameters
        ----------
        connection_url : str
            The MongoDB connection URL string.
        """
        self.db_client = MongoClient(connection_url)

    def __str__(self):
        """
        Returns the object as a string
        """
        return "MongoDB client object"
