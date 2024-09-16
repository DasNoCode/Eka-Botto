from Structures.Command.BaseCommand import BaseCommand
from pyrogram.types import ChatPermissions
from Structures.Message import Message
from Handler.EventHandler import EventHandler


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(client, handler, {
            'command': 'captcha',
            'category': 'core',
            'description': {
                'content': 'Check the captcha'
            },
            'exp': 1
        })

    async def exec(self, M: Message, contex):
        keys = list(contex[2].keys())
        if M.sender.user_id == EventHandler.user_id:
         if len(keys) == 3:
             keybord = [{
                 "text": keys[0],
                 "callback_data": f"/captcha --code={keys[0]}"
             }, {
                 "text": keys[1],
                 "callback_data": f"/cpatcha --code={keys[1]}"
             }, {
                 "text": keys[2],
                 "callback_data": f"/cpatcha --code={keys[2]}"
             }
             ]        
             return await self.__client.send_photo(M.chat_id,"out.png", caption= "Here is your captcha! Slove this with in 1min or you be banned.", button= keybord)
         
         if contex[2][keys[0]] == EventHandler.captcha_code:
             return await self.__client.restrict_chat_member(M.chat_id, M.sender.user_id,ChatPermissions(can_send_messages=True,can_send_media_messages=True))
        else:
            return await self.__client.answer_callback_query(callback_query_id= M.id ,text="This Captcha is not you!", show_alert=True)
