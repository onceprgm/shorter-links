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


@router.message(Command("stats"))
async def stats(message: Message, command: CommandObject) -> None:
    if not command.args:
        await message.answer("Usage: /stats <slug>")
        return

    slug = command.args.split()[0]
    async with session_factory() as session:
        link = await storage.get_link(session, slug)

    if link is None or link.user_id != message.from_user.id:
        await message.answer("Link not found.")
        return

    created = link.created_at.strftime("%Y-%m-%d %H:%M")
    await message.answer(
        f"Slug: {link.slug}\n"
        f"URL: {link.original_url}\n"
        f"Clicks: {link.clicks}\n"
        f"Created: {created}"
    )


@router.message(Command("list"))
async def list_links(message: Message) -> None:
    async with session_factory() as session:
        items = await storage.list_links(session, message.from_user.id)

    if not items:
        await message.answer("No links yet. Create one with /shorten <url>.")
        return

    lines = [f"{link.slug}: {link.original_url} - {link.clicks} clicks" for link in items]
    await message.answer("\n".join(lines))


@router.message(Command("delete"))
async def delete_link(message: Message, command: CommandObject) -> None:
    if not command.args:
        await message.answer("Usage: /delete <slug>")
        return

    slug = command.args.split()[0]
    async with session_factory() as session:
        removed = await storage.delete_link(session, message.from_user.id, slug)

    await message.answer("Deleted." if removed else "Link not found.")
