from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultPhoto
import json
from Waifu import waifu, prefix
from Waifu.Database.main import get_users_list, add_waifu_to_db, get_user_waifus

@waifu.on_message(filters.command("harem", prefix))
async def harem_command(_, message):
    user_id = message.from_user.id

    # Check if the user is in the database and add them if not (you'll need to implement these functions)
    if user_id not in await get_users_list():
        await add_users_to_db(user_id)

    # Create an inline keyboard with a button to view waifus
    inline_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("View My Waifus", switch_inline_query_current_chat="view_waifus"),
            ]
        ]
    )

    # Send a message with the inline keyboard
    await message.reply(
        "Manage your harem:",
        reply_markup=inline_keyboard
    )

# Handle inline queries for viewing waifus
@waifu.on_inline_query(filters.regex("^view_waifus$"))
async def view_waifus_inline_query(_, inline_query):
    user_waifus = await get_user_waifus(inline_query.from_user.id)
    results = []

    for waifu_data in user_waifus:
        results.append(
            InlineQueryResultPhoto(
                title=waifu_data['name'],
                photo_url=waifu_data['image_url'],
                thumb_url=waifu_data['image_url'],
                caption=waifu_data['data']
            )
        )

    await inline_query.answer(results, cache_time=0)
