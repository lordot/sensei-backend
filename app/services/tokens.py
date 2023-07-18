from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def reduce_balance(user: User, tokens: int, session: AsyncSession):
    """
    Reduce user's balance by tokens.
    """
    user.tokens = max(0, user.tokens - tokens)
    session.add(user)
    await session.commit()
