from sqlalchemy import select
from models import Settings, User

async def get_setting(session, key, default="0"):
    result = await session.execute(select(Settings).where(Settings.key == key))
    obj = result.scalar()
    return obj.value if obj else default

async def set_setting(session, key, value):
    obj = await session.get(Settings, key)
    if obj:
        obj.value = value
    else:
        session.add(Settings(key=key, value=value))
    await session.commit()

async def calc_price(session, service_type, count):
    price = int(await get_setting(session, f"{service_type}_price", "0"))
    discount = int(await get_setting(session, "discount", "0"))
    total = price * count
    if discount > 0:
        total = total - (total * discount // 100)
    return total

async def add_success_invite(session, inviter_id):
    inviter = await session.get(User, inviter_id)
    if inviter:
        inviter.successful_invites += 1
        if inviter.successful_invites >= 10:
            inviter.balance += 1
            inviter.successful_invites = 0
        await session.commit()
