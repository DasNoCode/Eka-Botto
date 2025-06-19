import random
from threading import Timer

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "ttt",
                "category": "game",
                "xp": True,
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {"content": "Play Tic-Tac-Toe with the bot"},
            },
        )
        self.user_id = None
        self.user_points = 0
        self.bot_points = 0
        self.player_mark = "❌"
        self.bot_mark = "⭕️"
        self.board = {i: "⬜️" for i in range(1, 10)}

    def update_board(self, letter, position):
        self.board[position] = letter

    def reset_board(self):
        self.user_id = None
        self.user_points = 0
        self.bot_points = 0

        for key in self.board.keys():
            self.board[key] = "⬜️"

    def is_draw(self):
        return all(space != "⬜️" for space in self.board.values())

    def is_space_free(self, position):
        return self.board[position] == "⬜️"

    def is_winner(self, mark):
        winning_combinations = [
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
            (1, 4, 7),
            (2, 5, 8),
            (3, 6, 9),
            (1, 5, 9),
            (7, 5, 3),
        ]
        return any(
            self.board[a] == self.board[b] == self.board[c] == mark
            for a, b, c in winning_combinations
        )

    def best_move(self):
        best_score = -float("inf")
        move = None
        for key in self.board:
            if self.is_space_free(key):
                self.board[key] = self.bot_mark
                score = self.minimax(0, False)
                self.board[key] = "⬜️"
                if score > best_score:
                    best_score, move = score, key
        return move

    def minimax(self, depth, is_maximizing):
        if self.is_winner(self.bot_mark):
            return 1
        if self.is_winner(self.player_mark):
            return -1
        if self.is_draw():
            return 0

        best_score = float("-inf") if is_maximizing else float("inf")
        for key in self.board:
            if self.is_space_free(key):
                self.board[key] = self.bot_mark if is_maximizing else self.player_mark
                score = self.minimax(depth + 1, not is_maximizing)
                self.board[key] = "⬜️"
                best_score = (
                    max(best_score, score) if is_maximizing else min(best_score, score)
                )
        return best_score

    def generate_keyboard(self):
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        self.board[i], callback_data=f"/ttt --type=game --data={i}"
                    )
                    for i in range(row, row + 3)
                ]
                for row in (1, 4, 7)
            ]
        )

    async def exec(self, M: Message, context):
        self.text = (
            f"@{M.sender.user_name}  **VS**  @{M.bot_username} \n• **Type** =  __Tic-Tac-Toe__ \n"
            f"• **Score** = 👤 -  **{self.user_points}** | 🤖 -  **{self.bot_points}**"
        )

        if self.user_id is None:
            self.user_id = M.sender.user_id
            self.msg = await self.client.send_message(
                chat_id=M.chat_id, text=self.text, reply_markup=self.generate_keyboard()
            )
            return

        if not M.is_callback:
            return

        if M.sender.user_id != self.user_id:
            return await self.client.answer_callback_query(
                callback_query_id=M.query_id,
                text="__This is not your game!🎮\n Use /ttt to play__",
                show_alert=True,
            )

        pos = int(context[2].get("data"))
        if not self.is_space_free(pos):
            return

        self.update_board(self.player_mark, pos)
        if self.is_winner(self.player_mark):
            self.user_points += 1
            result_text = f"{self.text}\n• **Game** = __User Win__"
            await self.client.edit_message_text(
                chat_id=M.chat_id, message_id=M.message_id, text=result_text
            )
            self.reset_board()
            return

        if self.is_draw():
            result_text = f"{self.text}\n• **Game** = __Tie Game__"
            await self.client.edit_message_text(
                chat_id=M.chat_id, message_id=M.message_id, text=result_text
            )
            self.reset_board()
            return

        bot_move = self.best_move()
        self.update_board(self.bot_mark, bot_move)

        if self.is_winner(self.bot_mark):
            self.bot_points += 1
            result_text = f"{self.text}\n• **Game** = __Bot Win__"
            await self.client.edit_message_text(
                chat_id=M.chat_id, message_id=M.message_id, text=result_text
            )
            self.reset_board()
            return

        await self.client.edit_message_text(
            chat_id=M.chat_id,
            message_id=M.message_id,
            text=self.text,
            reply_markup=self.generate_keyboard(),
        )
