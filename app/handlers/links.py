from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app import storage
from app.config import settings
from app.db import session_factory
from app.urls import normalize_url, short_link

router = Router()


@router.message(Command("shorten"))
async def shorten(message: Message, command: CommandObject) -> None:
    if not command.args:
        await message.answer("Usage: /shorten <url>")
        return

    url = normalize_url(command.args.split()[0])
    if url is None:
        await message.answer("That does not look like a valid URL.")
        return

    async with session_factory() as session:
        used = await storage.count_links(session, message.from_user.id)
        if used >= settings.max_links_per_user:
            await message.answer(
                f"Limit reached: up to {settings.max_links_per_user} links per user."
            )
            return
        link = await storage.create_link(session, message.from_user.id, url)

    await message.answer(short_link(link.slug))
