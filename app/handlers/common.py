from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from app import storage
from app.db import session_factory

router = Router()

WELCOME = (
    "Hi! I shorten links.\n\n"
    "Send /shorten <url> and I will return a short t.me link.\n"
    "/help - all commands."
)

HELP = (
    "Commands:\n"
    "/shorten <url> - create a short link\n"
    "/stats <slug> - clicks and creation date\n"
    "/list - my links\n"
    "/delete <slug> - delete a link"
)


@router.message(CommandStart(deep_link=True))
async def start_with_payload(message: Message, command: CommandObject) -> None:
    # Visitor opened t.me/<bot>?start=<slug>: count the click and offer the link
    slug = command.args
    async with session_factory() as session:
        link = await storage.register_click(session, slug)

    if link is None:
        await message.answer("Link not found.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Open link", url=link.original_url)]]
    )
    await message.answer("Your link is ready:", reply_markup=keyboard)


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(WELCOME)


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(HELP)
