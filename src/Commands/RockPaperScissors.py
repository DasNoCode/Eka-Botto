import asyncio
import random

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "rps",
                "category": "game",
                "xp": True,
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {"content": "Play Rock-Paper-Scissors with the bot."},
            },
        )
        self.reset_game()

    def is_winner(self):
        return self.user_points > self.bot_points

    def reset_game(self):
        self.bot_points = 0
        self.user_points = 0
        self.targetRounds = 0
        self.user_id = 0
        self.playedRounds = 0

    async def exec(self, M: Message, context):
        self.text = (
            f"@{M.sender.user_name}  **VS**  @{M.bot_username} \n• **Type** =  __Rock-Paper-Scissors__ \n"
            f"• **Score** = 👤 -  **{self.user_points}** | 🤖 -  **{self.bot_points}**"
        )

        if context[2].get("type") == "rounds":
            try:
                self.targetRounds = int(context[2].get("data"))
            except ValueError:
                self.targetRounds = 0

        if self.targetRounds == 0:
            btn = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=str(i),
                            callback_data=f"/rps --type=rounds --data={i} --user_id={M.sender.user_id}",
                        )
                        for i in [4, 8, 12]
                    ]
                ]
            )
            return await self.client.send_message(
                M.chat_id, "How many rounds do you want to play?", reply_markup=btn
            )

        if not M.is_callback:
            return

        if M.sender.user_id != int(context[2].get("user_id")):
            return await self.client.answer_callback_query(
                callback_query_id=M.query_id,
                text="This is not your game!🎮\n Use /rps to play!",
                show_alert=True,
            )

        user_choice = context[2].get("data").lower()
        bot_choice = random.choice(["rock", "paper", "scissors"])

        if user_choice == bot_choice:
            self.playedRounds += 1
            result_text = f"{self.text}\n• **Game** = __Tie Game__"
        elif (user_choice, bot_choice) in [
            ("rock", "scissors"),
            ("paper", "rock"),
            ("scissors", "paper"),
        ]:
            self.user_points += 1
            self.playedRounds += 1
            result_text = f"{self.text}\n• **Game** = __@{M.sender.user_name} Win__"
        else:
            self.bot_points += 1
            self.playedRounds += 1
            print("++")
            result_text = f"{self.text}\n• **Game** = __@{M.bot_username} Win__"

        if self.playedRounds == self.targetRounds:
            game_result = (
                f"{self.text}\n• **Game** = __@{M.sender.user_name} Wins the game! 🏆__"
                if self.is_winner()
                else f"{self.text}\n• **Game** = __@{M.sender.user_name} lost the game 😢\n/rps - Try your luck again!__"
            )
            self.reset_game()
            btn = None
            result_text = game_result
        else:
            btn = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Rock 🪨",
                            callback_data=f"/rps --type=game --data=Rock --user_id={M.sender.user_id}",
                        ),
                        InlineKeyboardButton(
                            "Paper 📄",
                            callback_data=f"/rps --type=game --data=Paper --user_id={M.sender.user_id}",
                        ),
                        InlineKeyboardButton(
                            "Scissors ✂️",
                            callback_data=f"/rps --type=game --data=Scissors --user_id={M.sender.user_id}",
                        ),
                    ]
                ]
            )

        msg = await self.client.edit_message_text(
            chat_id=M.chat_id,
            message_id=M.message_id,
            text=result_text,
            reply_markup=btn,
        )

        await self.timer(msg)

    async def timer(self, msg):
        await asyncio.sleep(60)
        self.reset_game()
        await self.client.delete_messages(msg.chat.id, msg.id)
