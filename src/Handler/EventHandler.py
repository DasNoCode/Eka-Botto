from pyrogram.types import ChatPermissions
from Structures.Client import SuperClient
from Structures.Message import Message
from captcha.image import ImageCaptcha
import random
import time 
import os



class EventHandler:

    user_id = None
    captcha_code = ""

    def __init__(self, client: SuperClient):
        self.__client = client

    def captcha(self):
        fonts = lambda folder: [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        image = ImageCaptcha(fonts=fonts)
        aplhabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M',
                     'N', 'P', 'R', 'T', 'U', 'V', 'W', 'X', 'Y']
        captcha = random.sample(aplhabets, 4)
        str = "".join(captcha)
        image.write(str, 'out.png')
        self.captcha_code = str
        return str
    
    async def captcha(self, M: Message):
        self.chat_titel = M.chat.title
        captcha = True
        if captcha: #add db
         new_members = M.new_chat_members
         for member in new_members:
          self.member = member
          self.user_id = member.id
          await self.__client.restrict_chat_member(M.chat.id, member.id,ChatPermissions())
         self.string = captcha()
         var1 = var2 = var3 = None
         selected_var = random.choice(['var1', 'var2', 'var3'])
         setattr(self, selected_var, self.string) if selected_var in ['var1', 'var2'] else setattr(self, 'var3', self.string)
         var1 = "".join(random.sample(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M', 'N', 'P', 'R', 'T', 'U', 'V', 'W', 'X', 'Y'], 4)) if var1 is None else var1
         var2 = "".join(random.sample(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M', 'N', 'P', 'R', 'T', 'U', 'V', 'W', 'X', 'Y'], 4)) if var2 is None else var2
         var3 = "".join(random.sample(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M', 'N', 'P', 'R', 'T', 'U', 'V', 'W', 'X', 'Y'], 4)) if var3 is None else var3
         keybord = [{
             "text": "Captcha",
             "callback_data": f"/captcha --var1={var1} --var2={var2} --var3{var3}"
         }]
         await self.__client.send_photo(M.chat_id,"Images/Welcome_image.jpg", caption=f"Welcome to this chat @{member.username}.We all hope you will have a great time talking here!\nSlove the captcha to message here.",buttons= keybord)
        else:
         msg = await self.__client.send_photo(M.chat_id,"Images/Welcome_image.jpg", caption=f"Welcome to this chat @{member.username}.We all hope you will have a great time talking here!")
         time.sleep(60)
         msg.delete()


