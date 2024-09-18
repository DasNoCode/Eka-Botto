from Structures.Command.BaseCommand import BaseCommand
from pyrogram.types import ChatPermissions
from Structures.Message import Message
from Handler.EventHandler import EventHandler
from captcha.image import ImageCaptcha
import random
import string
import os


class Command(BaseCommand):
    captcha_code = ""

    def __init__(self, client, handler):
        super().__init__(client, handler, {
            'command': 'captcha',
            'category': 'core',
            'description': {
                'content': 'Privents from bots'
            },
            'exp': 1
        })


    async def exec(self, M: Message, contex):
        keys = list(contex[2].keys())
        member_user_id = EventHandler.member_user_id
        if M.sender.user_id == member_user_id:
         if keys[0] == "code":
          if contex[2][keys[0]] == self.captcha_code:
              return await self.__client.restrict_chat_member(
                  M.chat_id,
                  M.sender.user_id,
                  ChatPermissions(
                      can_send_messages=True, can_send_media_messages=True
                  ),
              )
          else:
              return await self.__client.ban_chat_member(
                  EventHandler.chat_id, EventHandler.member_user_id
              )         
         if contex[2][keys[0]] == "captcha":
             captcha_image = ImageCaptcha(
                 fonts=[
                     f
                     for f in os.listdir("src/CaptchaFonts")
                     if os.path.isfile(os.path.join("src/CaptchaFonts", f))
                 ]
             )
             random_text = lambda: "".join(
                 random.choices(string.ascii_letters + string.digits, k=5)
             )
             self.captcha_code = random_text()
             captcha_image.write(self.captcha_code, "Captcha.png")
             code1 = code2 = code3 = None
             selected_var = random.choice(["code1", "code2", "code3"])
             code1 = None
             code2 = None
             code3 = None
             for var in ["code1", "code2", "code3"]:
                 setattr(self, var, getattr(self, var) or random_text())
     
             setattr(self, selected_var, self.captcha_code) if selected_var in [
                 "code1",
                 "code2",
             ] else setattr(self, "code3", self.captcha_code)
         
             keybord = [
                 {"text": code1, "callback_data": f"/captcha --code={code1}"},
                 {"text": code2, "callback_data": f"/cpatcha --code={code2}"},
                 {"text": code3, "callback_data": f"/cpatcha --code={code3}"},
             ]
             await self.__client.send_photo(
                 M.chat_id,
                 "Captcha.png",
                 caption=f"Here is your captcha @{EventHandler.member_username}! Slove this with in 1min or you be banned.",
                 button=keybord,
             )
        else:
            return await self.__client.answer_callback_query(
                callback_query_id=M.id,
                text="This Captcha isn't for you!",
                show_alert=True,
            )



























#from Structures.Command.BaseCommand import BaseCommand
#from pyrogram.types import ChatPermissions
#from Structures.Message import Message
#from Handler.EventHandler import EventHandler
#from captcha.image import ImageCaptcha
#import random
#import string
#import os
#
#class Command(BaseCommand):
#    captcha_code = ""
#    member_user_id = None
#
#    def __init__(self, client, handler):
#        super().__init__(client, handler, {
#            'command': 'captcha',
#            'category': 'core',
#            'description': {
#                'content': 'Check the captcha'
#            },
#            'exp': 1
#        })
#
#    async def exec(self, M: Message, contex):
#        captcha_image = ImageCaptcha(fonts=[f for f in os.listdir("src/CaptchaFonts") if os.path.isfile(os.path.join("src/CaptchaFonts", f))])
#        random_text = lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=5))
#        captcha_code = random_text()
#        captcha_image.write(captcha_code,"Captcha.png")
#        keys = list(contex[2].keys())
#        member_user_id = EventHandler.member_user_id
#        code1 = code2 = code3 = None
#        selected_var = random.choice(['code1', 'code2', 'code3'])
#        setattr(self, selected_var, captcha_code) if selected_var in ['code1', 'code2'] else setattr(self, 'code3', captcha_code)
#        code1 = random_text()
#        code2 = random_text()
#        code3 = random_text()
#        if M.sender.user_id == member_user_id:
#         if len(keys) == 3:
#             keybord = [{
#                 "text": code1,
#                 "callback_data": f"/captcha --code={code1}"
#             }, {
#                 "text": code2,
#                 "callback_data": f"/cpatcha --code={code2}"
#             }, {
#                 "text": code3,
#                 "callback_data": f"/cpatcha --code={code3}"
#             }
#             ]        
#             return await self.__client.send_photo(M.chat_id,"Captcha.png", caption= "Here is your captcha! Slove this with in 1min or you be banned.", button= keybord)
#         
#         if contex[2][keys[0]] == EventHandler.captcha_code:
#             return await self.__client.restrict_chat_member(M.chat_id, M.sender.user_id,ChatPermissions(can_send_messages=True,can_send_media_messages=True))
#        else:
#            return await self.__client.answer_callback_query(callback_query_id= M.id ,text="This Captcha is not you!", show_alert=True)