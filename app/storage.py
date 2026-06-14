from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Link
from app.slug import generate_slug


async def _unique_slug(session: AsyncSession) -> str:
    # Retry until a free slug is generated
    while True:
        slug = generate_slug()
        if await session.get(Link, slug) is None:
            return slug


async def create_link(session: AsyncSession, user_id: int, original_url: str) -> Link:
    link = Link(slug=await _unique_slug(session), original_url=original_url, user_id=user_id)
    session.add(link)
    await session.commit()
    return link


async def get_link(session: AsyncSession, slug: str) -> Link | None:
    return await session.get(Link, slug)


async def register_click(session: AsyncSession, slug: str) -> Link | None:
    # Increment the counter and return the link, or None if it does not exist
    link = await session.get(Link, slug)
    if link is None:
        return None
    link.clicks += 1
    await session.commit()
    return link


async def list_links(session: AsyncSession, user_id: int) -> list[Link]:
    result = await session.execute(
        select(Link).where(Link.user_id == user_id).order_by(Link.created_at.desc())
    )
    return list(result.scalars().all())


async def count_links(session: AsyncSession, user_id: int) -> int:
    result = await session.execute(
        select(func.count()).select_from(Link).where(Link.user_id == user_id)
    )
    return result.scalar_one()


async def delete_link(session: AsyncSession, user_id: int, slug: str) -> bool:
    # Delete only when the slug belongs to the user; return True if a row was removed
    result = await session.execute(
        delete(Link).where(Link.slug == slug, Link.user_id == user_id)
    )
    await session.commit()
    return result.rowcount > 0
