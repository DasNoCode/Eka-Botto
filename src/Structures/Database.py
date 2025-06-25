from tinydb import Query, TinyDB
from Database.Chat import Chat
from Database.User import User


class Database:
    def __init__(self, filepath):
        self.__db1, self.__db2 = filepath
        self.__userdb = TinyDB(self.__db1)
        self.__chatdb = TinyDB(self.__db2)
        self.query = Query()

    @property
    def User(self):
        return User(self.__userdb, self.query)

    @property
    def Chat(self):
        return Chat(self.__chatdb, self.query)


