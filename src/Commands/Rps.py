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
        self.user_id = 0
        self.UserPoints = 0
        self.BotPoints = 0
        self.tergetRounds = 0
        self.playedRounds = 0

    def isWon(self):
        if self.playedRounds == 0:
            return True if self.UserPoints > self.BotPoints else False

    def reset_game(self):
        self.BotPoints = 0
        self.UserPoints = 0
        self.tergetRounds = 0
        self.user_id = 0
        self.playedRounds = 0

    async def exec(self, M: Message, context):
        if context[2].get("type") == "rounds":
            try:
                self.tergetRounds = int(context[2].get("data"))
            except ValueError:
                self.tergetRounds = 0

        if self.tergetRounds == 0:
            btn = [
                {
                    "text": str(i),
                    "callback_data": f"/rps --type=rounds --data={i} --user_id={M.sender.user_id}",
                }
                for i in [4, 8, 12]
            ]
            return await self.client.send_message(
                M.chat_id, "How many rounds do you want to play?", buttons=btn
            )

        if not M.is_callback:
            return

        if M.sender.user_id != int(context[2].get("user_id")):
            return await self.client.answer_callback_query(
                callback_query_id=M.query_id,
                text="This is not your game!🎮\n Use /rps to play!",
                show_alert=True,
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

        user_choice = context[2].get("data").lower()
        bot_choice = random.choice(["rock", "paper", "scissors"])

        text = f"**Rounds**: {self.playedRounds} of {self.tergetRounds} 🔢\n"

        if user_choice == bot_choice:
            result_text = "🤝 **It's a Tie!** 🤝"
        elif (user_choice, bot_choice) in [
            ("rock", "scissors"),
            ("paper", "rock"),
            ("scissors", "paper"),
        ]:
            self.UserPoints += 1
            result_text = "🎉 **You won this round!** 🎉"
        else:
            self.BotPoints += 1
            result_text = "🤖 **Bot won this round!** 🤖"

        if self.playedRounds == 0:
            text += f"__{M.sender.user_name} 👤  Vs   @{M.bot_username} 🤖__\n"
        elif self.playedRounds == self.tergetRounds:
            self.reset_game()
            btn = None
            text = (
                "🏆 **Congratulations! You won this game!** 🏆"
                if self.isWon()
                else "😢 **Unfortunately, you lost this game.** 😢\n__/rps <- Try your luck again!__"
            )
        else:
            text += f"__Points:__\n**@{M.sender.user_name}**: {self.UserPoints} 👤 vs **@{M.bot_username}**: {self.BotPoints} 🤖\n{result_text}"

        self.playedRounds += 1

        msg = await self.client.edit_message_text(
            chat_id=M.chat_id,
            message_id=M.message_id,
            text=text,
            buttons=btn,
        )

        await self.timer(msg)

    async def timer(self, msg):
        await asyncio.sleep(60)
        self.reset_game()
        await self.client.delete_messages(msg.chat.id, msg.id)
