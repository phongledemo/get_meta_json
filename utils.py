"""Setup database"""
from pymongo import MongoClient
from pymongo.database import Database
from config import database

class Connect:
    """Connect database"""
    def connect():
        client = MongoClient(database)
        # get database User
        db: Database = client.get_database("dashboard")
        return db


class Collect_connection(Connect):
    def __init__(self):
        self.conn: Database = Connect.connect()

    def connect_collect_dashboard(self):
        collect = self.conn.get_collection("root")
        return collect

    def connect_collect_new_dashboard(self):
        collect = self.conn.get_collection("root_new")
        return collect

    def connect_collect_processdoc(self):
        collect = self.conn.get_collection("dnac")
        return collect

    def connect_collect_processdoc_re(self):
        collect = self.conn.get_collection("dnac_release")
        return collect

    def connect_collect_default(self):
        collect = self.conn.get_collection("default")
        return collect

    def connect_collect_ise(self):
        collect = self.conn.get_collection("ise")
        return collect

    def connect_collect_ise_re(self):
        collect = self.conn.get_collection("ise_release")
        return collect

    def connect_collect_polaris(self):
        collect = self.conn.get_collection("polaris")
        return collect

    def connect_collect_polaris_re(self):
        collect = self.conn.get_collection("polaris_release")
        return collect

    def connect_collect_record(self):
        collect = self.conn.get_collection("record")
        return collect

    def connect_collect_record_inventory(self):
        collect = self.conn.get_collection("inventory")
        return collect
