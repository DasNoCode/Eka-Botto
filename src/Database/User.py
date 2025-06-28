from collections.abc import MutableMapping
from datetime import datetime


class User:
    def __init__(self, db, query):
        self.__db = db
        self.query = query
        if not self.__db.contains(self.query.users.exists()):
            self.__db.insert({"users": []})

    def get_all_users(self):
        users_data = self.__db.get(self.query.users.exists())
        return users_data["users"]
    
    def add_user(self, user_data):

        users_list = self.get_all_users()
        if any(user["user_id"] == user_data["user_id"] for user in users_list):
            return

        default_user_data = {
            "user_id": user_data["user_id"],
            "afk": {
                "is_afk": user_data.get("afk", {}).get("is_afk", False),
                "afk_reason": user_data.get("afk", {}).get("afk_reason", None),
                "time": user_data.get("afk", {}).get("time", None),
            },
            "lvl": user_data.get("lvl", 1),
            "last_lvl": user_data.get("last_lvl", 1),
            "xp": user_data.get("xp", 0),
            "tic_tac_toe": {
                "win": user_data.get("tic_tac_toe", {}).get("win", 0),
                "total_game_played": user_data.get("tic_tac_toe", {}).get("total_game_played", 0)
            },
            "rps": { 
                "win": user_data.get("rps", {}).get("win", 0),
                "total_game_played": user_data.get("rps", {}).get("total_game_played", 0)
            },
            "ban": {
                "no_of": user_data.get("ban", {}).get("no_of", 0),
                "is_ban": user_data.get("ban", {}).get("is_ban", False),
                "reason": user_data.get("ban", {}).get("reason", None),
                "time": user_data.get("ban", {}).get("time", None),
            },
        }

        users_list.append(default_user_data)
        self.__db.update({"users": users_list}, self.query.users.exists())
    
    def get_user(self, user_id):
        users_list = self.get_all_users()
        user = next((u for u in users_list if u["user_id"] == user_id), None)
        if user:
            return user
        else:
            self.add_user({"user_id": user_id})
            return self.get_user(user_id)
        
    def update_user(self, user_id, updates):
        users_list = self.get_all_users()
        user = self.get_user(user_id)
        if not user:
            return

        listt_without_theuser = [
            user for user in users_list if user["user_id"] != user_id
        ]

        def recursive_update(d, u):
            for k, v in u.items():
                if isinstance(v, MutableMapping) and k in d:
                    d[k] = recursive_update(d.get(k, {}), v)
                else:
                    d[k] = v
            return d

        listt_without_theuser.append(recursive_update(user, updates))
        self.__db.update({"users": listt_without_theuser}, self.query.users.exists())
    
    def lvl_garined(self, user_id, xp, last_lvl, lvl):
        user = self.get_user(user_id)
        if not user:
            return
        user["xp"] = xp
        user["last_lvl"] = last_lvl
        user["lvl"] = lvl
        self.update_user(user_id, user)

    def increment_tic_tac_toe(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return
        user["tic_tac_toe"] += 1
        self.update_user(user_id, user)

    def increment_rps(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return
        user["rps"] += 1
        self.update_user(user_id, user)

    def update_ban(self, user_id, is_ban, time, reason=None):
        user = self.get_user(user_id)
        if not user:
            return
        user["ban"] = {"is_ban": is_ban, "reason": reason, "time": time}
        self.update_user(user_id, user)

    def set_afk(self, user_id, is_afk, afk_reason="", time=None):
        user = self.get_user(user_id)
        if not user:
            return

        afk_reason = afk_reason if afk_reason is not None else ""
        time = time if time is not None else datetime.now().time()

        user["afk"] = {"is_afk": is_afk, "afk_reason": afk_reason, "time": time}
        self.update_user(user_id, user)

