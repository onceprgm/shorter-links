# shorter-links

Telegram bot for shortening links with click statistics.

Send the bot a long URL and get a short one back. Every visit goes through the
redirect service, which increments a counter; statistics are available in the bot.

## Stack

- **[aiogram 3.x](https://docs.aiogram.dev/)** - bot logic (async)
- **[FastAPI](https://fastapi.tiangolo.com/) + uvicorn** - redirect microservice
- **SQLite** via **SQLAlchemy 2.0 (async)** + aiosqlite
- **pydantic-settings** - config from `.env`

## Architecture

```
User ──URL──▶ Bot (aiogram) ──write──▶ SQLite ◀──read── Redirect (FastAPI)
                  ▲                                          │
                  └──────────── stats ◀── +1 click ◀── HTTP 302 ── Browser
```

## Commands

| Command           | Description                  |
| ----------------- | ---------------------------- |
| `/shorten <url>`  | create a short link          |
| `/stats <slug>`   | clicks, creation date        |
| `/list`           | all links of the user        |
| `/delete <slug>`  | delete a link                |
| `/help`           | help                         |

## Database schema (table `links`)

| Field          | Type      | Description           |
| -------------- | --------- | --------------------- |
| `slug`         | TEXT PK   | random N characters   |
| `original_url` | TEXT      | full URL              |
| `user_id`      | INTEGER   | Telegram user_id      |
| `clicks`       | INTEGER   | visit counter         |
| `created_at`   | TIMESTAMP | creation date         |

## Running locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env   # set BOT_TOKEN from @BotFather

# bot
python -m app.bot

# redirect service (in a separate terminal)
python -m app.redirect
```

## Status

🚧 Work in progress. Built with atomic commits.
