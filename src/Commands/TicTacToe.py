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
            }
        )
        self.userId = None
        self.userPoints = 0
        self.botPoints = 0
        self.playerMark = "❌"
        self.botMark = "⭕️"
        self.board = {i: "⬜️" for i in range(1, 10)}

    def updateBoard(self, letter, position):
        self.board[position] = letter

    def resetBoard(self):
        self.userId = None
        self.userPoints = 0
        self.botPoints = 0
        for key in self.board.keys():
            self.board[key] = "⬜️"

    def isDraw(self):
        return all(space != "⬜️" for space in self.board.values())

    def isSpaceFree(self, position):
        return self.board[position] == "⬜️"

    def isWinner(self, mark):
        winningCombinations = [
            (1, 2, 3), (4, 5, 6), (7, 8, 9),
            (1, 4, 7), (2, 5, 8), (3, 6, 9),
            (1, 5, 9), (7, 5, 3)
        ]
        return any(
            self.board[a] == self.board[b] == self.board[c] == mark
            for a, b, c in winningCombinations
        )

    def bestMove(self):
        bestScore = -float("inf")
        move = None
        for key in self.board:
            if self.isSpaceFree(key):
                self.board[key] = self.botMark
                score = self.minimax(0, False)
                self.board[key] = "⬜️"
                if score > bestScore:
                    bestScore, move = score, key
        return move

    def minimax(self, depth, isMaximizing):
        if self.isWinner(self.botMark):
            return 1
        if self.isWinner(self.playerMark):
            return -1
        if self.isDraw():
            return 0

        bestScore = float("-inf") if isMaximizing else float("inf")
        for key in self.board:
            if self.isSpaceFree(key):
                self.board[key] = self.botMark if isMaximizing else self.playerMark
                score = self.minimax(depth + 1, not isMaximizing)
                self.board[key] = "⬜️"
                if isMaximizing:
                    bestScore = max(bestScore, score)
                else:
                    bestScore = min(bestScore, score)
        return bestScore

    def generateKeyboard(self):
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

    async def exec(self, message: Message, context):
        self.text = "🎮  **Tic-Tac-Toe** \n\n **[** 👤 You  **|**  Bot 🤖  **]**"

        if self.userId is None:
            self.userId = message.sender.user_id
            self.msg = await self.client.send_message(
                chat_id=message.chat_id, text=self.text, reply_markup=self.generateKeyboard()
            )
            return

        if not message.is_callback:
            return

        if message.sender.user_id != self.userId:
            return await self.client.answer_callback_query(
                callback_query_id=message.query_id,
                text="**This is not your game!**\n\n**Use /ttt to play**",
                show_alert=True
            )

        pos = int(context[2].get("data"))
        if not self.isSpaceFree(pos):
            return

        self.updateBoard(self.playerMark, pos)
        if self.isWinner(self.playerMark):
            userStats = self.client.db.User.get_user(user_id=self.userId)
            currentWin = userStats.get("tic_tac_toe", {}).get("win", 0)
            xpGained = random.randint(3, 5)
            await self.client.xp_lvl(message, xp_gained=xpGained)
            self.client.db.User.update_user(self.userId, {"tic_tac_toe": {"win": currentWin + 1}})
            totalRoundsPlayed = self.client.db.User.get_user(user_id=message.sender.user_id).get("tic_tac_toe").get("total_game_played")
            self.client.db.User.update_user(message.sender.user_id, {"tic_tac_toe": {"total_game_played": totalRoundsPlayed + 1}})
            resultText = f"{self.text}\n\n**Winner:**  @{message.sender.user_name} Win!\n\n**XP:**  {xpGained}"
            await self.client.edit_message_text(
                chat_id=message.chat_id, message_id=message.message_id, text=resultText
            )
            self.resetBoard()
            return

        if self.isDraw():
            xpGained = random.randint(1, 2)
            await self.client.xp_lvl(message, xp_gained=xpGained)
            totalRoundsPlayed = self.client.db.User.get_user(user_id=message.sender.user_id).get("tic_tac_toe").get("total_game_played")
            self.client.db.User.update_user(message.sender.user_id, {"tic_tac_toe": {"total_game_played": totalRoundsPlayed + 1}})
            resultText = f"{self.text}\n\n**Winner:** Bot | User\n\n**XP:**  {xpGained}"
            await self.client.edit_message_text(
                chat_id=message.chat_id, message_id=message.message_id, text=resultText
            )
            self.resetBoard()
            return

        botMove = self.bestMove()
        self.updateBoard(self.botMark, botMove)

        if self.isWinner(self.botMark):
            xpGained = random.randint(1, 2)
            await self.client.xp_lvl(message, xp_gained=xpGained)
            totalRoundsPlayed = self.client.db.User.get_user(user_id=message.sender.user_id).get("tic_tac_toe").get("total_game_played")
            self.client.db.User.update_user(message.sender.user_id, {"tic_tac_toe": {"total_game_played": totalRoundsPlayed + 1}})
            resultText = f"{self.text}\n\n**Winner:** Bot Win!\n\n**XP:**  {xpGained}"
            await self.client.edit_message_text(
                chat_id=message.chat_id, message_id=message.message_id, text=resultText
            )
            self.resetBoard()
            return

        await self.client.edit_message_text(
            chat_id=message.chat_id,
            message_id=message.message_id,
            text=self.text,
            reply_markup=self.generateKeyboard()
        )