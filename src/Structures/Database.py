from tinydb import Query, TinyDB

from Database.Botdb import Botdb
from Database.Chat import Chat
from Database.User import User


class Database:
    def __init__(self, filepath):
        self.__db = TinyDB(filepath)
        self.query = Query()

    @property
    def User(self):
        return User(self.__db, self.query)

    @property
    def Chat(self):
        return Chat(self.__db, self.query)

    @property
    def Botdb(self):
        return Botdb(self.__db, self.query)
