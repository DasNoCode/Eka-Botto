import asyncio
import random

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "rps",
                "category": "core",
                "description": {"content": "Send the profile picture of the user."},
                "exp": 1,
            },
        )
        self.user_id = None
        self.UserPoints = 0
        self.BotPoints = 0
        self.Rounds = None

    async def check_points(self, M: Message):

        if self.UserPoints == self.Rounds:
            await self.client.send_message(
                M.chat_id, "Congratulations! You won this game!"
            )
            self.reset_game()
            return True

        if self.BotPoints == self.Rounds:
            await self.client.send_message(
                M.chat_id,
                "Unfortunately, you lost this game.\n __/rps <- Try your luck again__",
            )
            self.reset_game()
            return True

        return False

    def reset_game(self):
        self.BotPoints = self.UserPoints = 0
        self.user_id = self.Rounds = None

    async def exec(self, M: Message, context):

        if not M.is_callback or M.sender.user_id is not int(context[2].get("user_id")):
            return await self.client.answer_callback_query(
                callback_query_id=M.query_id,
                text="This is not your game!🎮\n Use /rps to play!",
                show_alert=True,
            )
        try:
            if context[2].get("type") is "rounds":
                self.Rounds = int(context[2].get("data"))
        except ValueError:
            pass

        if self.Rounds is None:
            btn = [
                {
                    "text": str(i),
                    "callback_data": f"/rps --type=rounds --data={i} --user_id={int(context[2].get('user_id'))}",
                }
                for i in [4, 8, 12]
            ]
            return await self.client.send_message(
                M.chat_id, "How many rounds do you want to play?", buttons=btn
            )

        btn = [
            {
                "text": "Rock",
                "callback_data": f"/rps --type=game --data=Rock --user_id={int(context[2].get('user_id'))}",
            },
            {
                "text": "Paper",
                "callback_data": f"/rps --type=game --data=Paper --user_id={int(context[2].get('user_id'))}",
            },
            {
                "text": "Scissors",
                "callback_data": f"/rps --type=game --data=Scissors --user_id={int(context[2].get('user_id'))}",
            },
        ]

        if await self.check_points(M):
            return

        user_choice = context[2].get("data").lower()
        bot_choice = random.choice(["rock", "paper", "scissors"])

        if user_choice == bot_choice:
            await self.client.edit_message_text(
                chat_id=M.chat_id,
                message_id=M.message_id,
                text=f"{M.sender.user_name} 👤  Vs   Bot 🤖\nTie Game!",
                buttons=btn,
            )
        elif (
            (user_choice == "rock" and bot_choice == "scissors")
            or (user_choice == "paper" and bot_choice == "rock")
            or (user_choice == "scissors" and bot_choice == "paper")
        ):
            self.UserPoints += 1
        else:
            self.BotPoints += 1

        await self.client.edit_message_text(
            chat_id=M.chat_id,
            message_id=M.message_id,
            text=f"{M.sender.user_name}: {self.UserPoints}\nBot: {self.BotPoints}",
            buttons=btn,
        )

    async def timer(self, chat_id):
        await asyncio.sleep(60)
        await self.delete_message(chat_id, self.captcha_message_id)

    async def delete_message(self, chat_id, message_id):
        if message_id:
            try:
                await self.client.delete_messages(
                    chat_id=chat_id, message_ids=message_id
                )
            except Exception as e:
                print(f"Failed to delete captcha message: {e}")
