import asyncio
import random
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

def choice_to_emoji(choice: str) -> str:
    """Map RPS choice to emoji."""
    return {
        "rock": "🪨",
        "paper": "📄",
        "scissors": "✂️"
    }.get(choice.lower(), "❓")

def outcome_to_emoji(outcome: str) -> str:
    """Map outcome to emoji color."""
    if outcome == "Tie Game":
        return "🟡"
    elif "Win" in outcome:
        return "🟢" if "Win" in outcome and "@" in outcome else "🔴"
    return "❓"

MOTIVATIONAL_MESSAGES = [
    "Nice move! Keep it up! 💪",
    "Don't give up, you can do it! 🚀",
    "That was close! Try your best! 🎯",
    "You're on fire! 🔥",
    "The game is heating up! 😎",
    "Every round counts, stay sharp! 🧠",
    "Is the bot getting smarter? 😉",
    "You got this! 👏"
]

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "rps",
                "category": "game",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {
                    "content": "Play Rock-Paper-Scissors with the bot."
                },
            },
        )
        self.reset_game()

    def reset_game(self):
        self.user_points = 0
        self.bot_points = 0
        self.played_rounds = 0
        self.target_rounds = 0
        self.user_id = 0


    def is_user_winner(self):
        return self.user_points > self.bot_points

    async def exec(self, M: Message, context):
        if context[2].get("type") == "rounds":
            try:
                self.target_rounds = int(context[2].get("data"))
                self.user_id = M.sender.user_id

                reply_markup = InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("Rock 🪨", callback_data=f"/rps --type=game --data=Rock --user_id={self.user_id}"),
                        InlineKeyboardButton("Paper 📄", callback_data=f"/rps --type=game --data=Paper --user_id={self.user_id}"),
                        InlineKeyboardButton("Scissors ✂️", callback_data=f"/rps --type=game --data=Scissors --user_id={self.user_id}")
                    ]]
                )

                text = (
                    f"🎮 **Rock-Paper-Scissors**\n\n"
                    f"👤 @{M.sender.user_name} (❓)  vs  🤖 @{M.bot_username} (❓)\n\n"
                    f"**Round**: {min(self.played_rounds, self.target_rounds)} / {self.target_rounds} | **Score**: 👤 {self.user_points} - {self.bot_points} 🤖\n\n"
                    "🔔 Game started! Make your move.\n"
                )

                return await self.client.edit_message_text(
                    chat_id=M.chat_id,
                    message_id=M.message_id,
                    text=text,
                    reply_markup=reply_markup
                )

            except ValueError:
                self.target_rounds = 0

        if self.target_rounds == 0:
            buttons = [[
                InlineKeyboardButton(
                    text="4️⃣",
                    callback_data=f"/rps --type=rounds --data=4 --user_id={M.sender.user_id}"
                ),
                InlineKeyboardButton(
                    text="6️⃣",
                    callback_data=f"/rps --type=rounds --data=6 --user_id={M.sender.user_id}"
                )
            ]]

            return await self.client.send_message(
                M.chat_id,
                "How many rounds do you want to play?",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

        if not M.is_callback:
            return

        if M.sender.user_id != int(context[2].get("user_id")):
            return await self.client.answer_callback_query(
                callback_query_id=M.query_id,
                text="This is not your game! 🎮\nUse /rps to start your own.",
                show_alert=True,
            )

        if context[2].get("type") == "game":
            user_choice = context[2].get("data").lower()
            bot_choice = random.choice(["rock", "paper", "scissors"])

            if user_choice not in {"rock", "paper", "scissors"}:
                return await self.client.answer_callback_query(
                    callback_query_id=M.query_id,
                    text="Invalid choice! Please choose Rock, Paper, or Scissors.",
                    show_alert=True,
                )

            if user_choice == bot_choice:
                outcome = "Tie Game"
            elif (user_choice, bot_choice) in [
                ("rock", "scissors"),
                ("paper", "rock"),
                ("scissors", "paper")
            ]:
                self.user_points += 1
                outcome = f"@{M.sender.user_name} Win"
            else:
                self.bot_points += 1
                outcome = f"@{M.bot_username} Win"

            self.played_rounds += 1

            user_choice_emoji = choice_to_emoji(user_choice)
            bot_choice_emoji = choice_to_emoji(bot_choice)
            outcome_emoji = (
                "🟡" if outcome == "Tie Game"
                else "🟢" if outcome.startswith("@"+M.sender.user_name)
                else "🔴"
            )
            outcome_message = (
                "It's a tie!"
                if outcome == "Tie Game"
                else "You win this round!"
                if outcome.startswith("@"+M.sender.user_name)
                else "Bot wins this round!"
            )
            motivational_message = random.choice(MOTIVATIONAL_MESSAGES)

            text = (
                f"🎮 **Rock-Paper-Scissors**\n\n"
                f"👤 @{M.sender.user_name} ({user_choice_emoji})  vs  🤖 @{M.bot_username} ({bot_choice_emoji})\n\n"
                f"**Round**: {min(self.played_rounds, self.target_rounds)} / {self.target_rounds} | **Score**: 👤 {self.user_points} - {self.bot_points} 🤖\n\n"
                f"🔔 Last round: {outcome_emoji} {outcome_message}"
                f"\n\n{motivational_message}"
            )

            result_text = f"{text}\n\n• **Game**: __{outcome}__"

            if self.played_rounds == self.target_rounds:
                if self.user_points > self.bot_points:
                    current_win = self.client.db.User.get_user(user_id=M.sender.user_id).get("rps").get("win")
                    xp_gained = (random.randint(3, 5))
                    await self.client.xp_lvl(M, xp_gained=xp_gained)
                    self.client.db.User.update_user(M.sender.user_id,{"rps": {"win": current_win + 1}})
                    result_text = f"{text}\n\n🏆 **Winner:** @{M.sender.user_name} | **XP**: {xp_gained}\n\n👏 Congratulations, you beat the bot!"
                elif self.user_points < self.bot_points:
                    xp_gained = (random.randint(1, 2))
                    await self.client.xp_lvl(M, xp_gained=xp_gained)
                    result_text = f"{text}\n\n🏆 **Winner:** @{M.bot_username} | **XP**: {xp_gained}\n\n🤖 Better luck next time!"
                else:
                    await self.client.xp_lvl(M, xp_gained=1)
                    result_text = f"{text}\n\n🤝 **Result:** Tie Game! | **XP**: 1"
                self.reset_game()
                reply_markup = None
            else:
                reply_markup = InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("Rock 🪨", callback_data=f"/rps --type=game --data=Rock --user_id={M.sender.user_id}"),
                        InlineKeyboardButton("Paper 📄", callback_data=f"/rps --type=game --data=Paper --user_id={M.sender.user_id}"),
                        InlineKeyboardButton("Scissors ✂️", callback_data=f"/rps --type=game --data=Scissors --user_id={M.sender.user_id}")
                    ]]
                )

            msg = await self.client.edit_message_text(
                chat_id=M.chat_id,
                message_id=M.message_id,
                text=result_text,
                reply_markup=reply_markup
            )

            await self.timer(msg)

    async def timer(self, msg):
        await asyncio.sleep(60)
        self.reset_game()
        await self.client.delete_messages(msg.chat.id, msg.id)