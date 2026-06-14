# shorter-links

Telegram bot for shortening links with click statistics.

Send the bot a long URL and get a short `t.me` deep link back. When someone
opens that link, Telegram launches the bot with `/start <slug>`, the bot
increments a click counter and offers a button to the original URL. No domain
and no hosting required - everything lives inside the bot.

## Stack

- **[aiogram 3.x](https://docs.aiogram.dev/)** - bot logic (async)
- **SQLite** via **SQLAlchemy 2.0 (async)** + aiosqlite
- **pydantic-settings** - config from `.env`

## How a short link works

A short link is a Telegram deep link:

```
https://t.me/<bot_username>?start=<slug>
```

```
Author ──/shorten <url>──▶ Bot ──save──▶ SQLite
                            │
                            └──reply──▶ t.me/<bot>?start=<slug>

Visitor ──open deep link──▶ Bot (/start <slug>) ──+1 click──▶ SQLite
                            │
                            └──reply──▶ button to original URL
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

cp .env.example .env   # set BOT_TOKEN and BOT_USERNAME

python -m app.bot
```

## Status

🚧 Work in progress. Built with atomic commits.
