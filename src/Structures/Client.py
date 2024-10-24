import hashlib
import os
import re
from datetime import datetime
from typing import BinaryIO, Callable, List, Optional, Union

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.errors import FilePartMissing
from pyrogram.file_id import FileType
from pyromod import Client

from Helpers.Logger import get_logger
from Helpers.Utils import Utils


class SuperClient(Client):
    def __init__(
        self, name: str, api_id: int, api_hash: str, bot_token: str, prefix: str
    ):
        super().__init__(
            name=name, api_id=api_id, api_hash=api_hash, bot_token=bot_token
        )
        self.prifix = prefix
        self.log = get_logger()
        self.callback_data_map = {}
        self.utils = Utils()

    async def admincheck(self, message):
        isadmin = await self.get_chat_member(message.chat.id, message.from_user.id)
        return isadmin.status in [
            enums.ChatMemberStatus.OWNER,
            enums.ChatMemberStatus.ADMINISTRATOR,
        ]

    async def send_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        text: str,
        buttons=None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
    ):

        message, entities = (
            await utils.parse_text_entities(self, text, parse_mode, entities)
        ).values()

        reply_markup = None

        if buttons:
            for button in buttons:
                original_data = button["callback_data"]
                hash_object = hashlib.sha256(original_data.encode())
                hash_key = hash_object.hexdigest()[:10]
                self.callback_data_map[hash_key] = original_data
                button["callback_data"] = hash_key

            reply_markup = types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(
                            button["text"], callback_data=button["callback_data"]
                        )
                    ]
                    for button in buttons
                ]
            )

        r = await self.invoke(
            raw.functions.messages.SendMessage(
                peer=await self.resolve_peer(chat_id),
                no_webpage=disable_web_page_preview or None,
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id,
                random_id=self.rnd_id(),
                schedule_date=utils.datetime_to_timestamp(schedule_date),
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                message=message,
                entities=entities,
                noforwards=protect_content,
            )
        )

        if isinstance(r, raw.types.UpdateShortSentMessage):
            peer = await self.resolve_peer(chat_id)

            peer_id = (
                peer.user_id
                if isinstance(peer, raw.types.InputPeerUser)
                else -peer.chat_id
            )

            return types.Message(
                id=r.id,
                chat=types.Chat(id=peer_id, type=enums.ChatType.PRIVATE, client=self),
                text=message,
                date=utils.timestamp_to_datetime(r.date),
                outgoing=r.out,
                reply_markup=reply_markup,
                entities=(
                    [
                        types.MessageEntity._parse(None, entity, {})
                        for entity in entities
                    ]
                    if entities
                    else None
                ),
                client=self,
            )

        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateNewMessage,
                    raw.types.UpdateNewChannelMessage,
                    raw.types.UpdateNewScheduledMessage,
                ),
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage),
                )

    async def send_photo(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        photo: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        ttl_seconds: int = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        buttons=None,
        progress: Callable = None,
        progress_args: tuple = (),
    ) -> Optional["types.Message"]:
        file = None

        # Initialize reply_markup to None to avoid referencing before assignment
        reply_markup = None

        # Prepare the reply markup if buttons are provided
        if buttons:
            # Process each button, assign unique callback_data, and create reply_markup
            for button in buttons:
                original_data = button["callback_data"]
                hash_object = hashlib.sha256(original_data.encode())
                hash_key = hash_object.hexdigest()[:10]
                self.callback_data_map[hash_key] = original_data
                button["callback_data"] = hash_key

            # Create InlineKeyboardMarkup for the buttons
            reply_markup = types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(
                            button["text"], callback_data=button["callback_data"]
                        )
                    ]
                    for button in buttons
                ]
            )

        try:
            # Determine the appropriate media type to send
            if isinstance(photo, str):
                if os.path.isfile(photo):
                    file = await self.save_file(
                        photo, progress=progress, progress_args=progress_args
                    )
                    media = raw.types.InputMediaUploadedPhoto(
                        file=file,
                        ttl_seconds=ttl_seconds,
                        spoiler=has_spoiler,
                    )
                elif re.match("^https?://", photo):
                    media = raw.types.InputMediaPhotoExternal(
                        url=photo, ttl_seconds=ttl_seconds, spoiler=has_spoiler
                    )
                else:
                    media = utils.get_input_media_from_file_id(
                        photo, FileType.PHOTO, ttl_seconds=ttl_seconds
                    )
            else:
                file = await self.save_file(
                    photo, progress=progress, progress_args=progress_args
                )
                media = raw.types.InputMediaUploadedPhoto(
                    file=file, ttl_seconds=ttl_seconds, spoiler=has_spoiler
                )

            # Send the media with the prepared reply_markup
            while True:
                try:
                    r = await self.invoke(
                        raw.functions.messages.SendMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=media,
                            silent=disable_notification or None,
                            reply_to_msg_id=reply_to_message_id,
                            random_id=self.rnd_id(),
                            schedule_date=utils.datetime_to_timestamp(schedule_date),
                            noforwards=protect_content,
                            reply_markup=(
                                await reply_markup.write(self) if reply_markup else None
                            ),
                            **await utils.parse_text_entities(
                                self, caption, parse_mode, caption_entities
                            )
                        )
                    )
                except FilePartMissing as e:
                    await self.save_file(photo, file_id=file.id, file_part=e.value)
                else:
                    for i in r.updates:
                        if isinstance(
                            i,
                            (
                                raw.types.UpdateNewMessage,
                                raw.types.UpdateNewChannelMessage,
                                raw.types.UpdateNewScheduledMessage,
                            ),
                        ):
                            return await types.Message._parse(
                                self,
                                i.message,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                is_scheduled=isinstance(
                                    i, raw.types.UpdateNewScheduledMessage
                                ),
                            )
        except pyrogram.StopTransmission:
            return None

    async def edit_message_text(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
        buttons=None,
    ) -> "types.Message":
        reply_markup = None

        # Prepare the reply markup if buttons are provided
        if buttons:
            # Process each button, assign unique callback_data, and create reply_markup
            for button in buttons:
                original_data = button["callback_data"]
                hash_object = hashlib.sha256(original_data.encode())
                hash_key = hash_object.hexdigest()[:10]
                self.callback_data_map[hash_key] = original_data
                button["callback_data"] = hash_key

            # Create InlineKeyboardMarkup for the buttons
            reply_markup = types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(
                            button["text"], callback_data=button["callback_data"]
                        )
                    ]
                    for button in buttons
                ]
            )

        r = await self.invoke(
            raw.functions.messages.EditMessage(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                no_webpage=disable_web_page_preview or None,
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                **await utils.parse_text_entities(self, text, parse_mode, entities)
            )
        )

        for i in r.updates:
            if isinstance(
                i, (raw.types.UpdateEditMessage, raw.types.UpdateEditChannelMessage)
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                )
