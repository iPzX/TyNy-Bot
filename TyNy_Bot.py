import logging
import requests
from bs4 import BeautifulSoup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from time import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2


API_TOKEN = '<enter your token here>'
logging.basicConfig(level=logging.INFO)
storage = RedisStorage2(db=5)
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    message.reply("wrote \n by ipzx \n =)")


@dp.message_handler(is_chat_admin=True, commands=['admin_check'])
async def handler3(msg: types.Message):
    await msg.answer("<b>You Are Admin</b>")


@dp.message_handler(commands='world_info')
async def world_info(msg: types.Message):
    r = requests.post("https://www.worldometers.info/coronavirus/")
    content = BeautifulSoup(r.text)
    for i in content.findAll('span', {'style': 'color:#aaa'}):
        corona_cases = i.text

    for j in content.findAll('div', {'class': 'maincounter-number'}):
        corona_death = j.text

    resp = requests.get('https://api.coinbase.com/v2/prices/buy?currency=USD',
                        proxies={'http': 'socks5://207.97.174.134:1080'})
    bitcoin_price = float(resp.json()['data']['amount'])

    await msg.reply(
        f'<b>Corona Cases: \n {corona_cases} \n\nCorona Deaths : {corona_death} \n\n BTC Price : \n {bitcoin_price} </b>')


@dp.message_handler(content_types=["new_chat_members"])
async def on_user_join(message: types.Message):
    a = message.new_chat_members
    for i in a:
        if i.mention.endswith("bot"):

            await bot.kick_chat_member(chat_id=message.chat.id, user_id=i.id)
            await message.reply("<b>Hey You cannot add bots here</b>")
        else:

            await message.reply(f'<b>salam {i.mention} jende khoshomadi</b>')

    await message.delete()


@dp.message_handler(is_chat_admin=True, commands=["ban"])
async def kick_(message: types.Message):
    user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if not message.reply_to_message:
        return await message.reply("<b> Please Specify some one to kick bitch</b>")

    if user.is_chat_admin():
        await message.reply("<b>Are You serious ?</b>")
        return

    await bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
    await message.reply("Sucssesfully removed {}".format(message.reply_to_message.from_user.first_name))


@dp.message_handler(text_contains=['delete'], is_chat_admin=True)
async def delete_message(message: types.Message):
    await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
    await bot.delete_message(message_id=message.reply_to_message.message_id, chat_id=message.chat.id)


@dp.message_handler(commands='pin', is_chat_admin=True)
async def pin_smth(message: types.Message):
    await bot.pin_chat_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)


@dp.message_handler(commands='mute', is_chat_admin=True)
async def Mute(message: types.Message):
    user = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
    if not message.reply_to_message:
        return await message.reply("<b> Please Specify some one to kick bitch</b>")

    if user.is_chat_admin():
        await message.reply("<b>Are You serious ?</b>")
        return
    if len(message.text.split()) == 2:

        timee = message.text.split()[1]

        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                       permissions=types.ChatPermissions(can_send_message=False, can_pin_messages=False,
                                                                         can_send_other_messages=False,
                                                                         can_invite_users=False),
                                       until_date=int(time()) + int(timee))
        hours = int(timee) / 3600
        await message.reply(f'{message.reply_to_message.from_user.first_name} is Muted for {str(hours)} hours')
    else:

        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                       permissions=types.ChatPermissions(can_send_message=False, can_pin_messages=False,
                                                                         can_send_other_messages=False,
                                                                         can_invite_users=False),
                                       until_date=int(time()) + 7200)
        await message.reply(f'{message.reply_to_message.from_user.first_name} is Muted for 2 hours !!!')


@dp.message_handler(text_contains='unmute', is_chat_admin=True)
async def Unmute(message: types.Message):
    user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                   permissions=types.ChatPermissions(can_send_message=True, can_pin_messages=True,
                                                                     can_send_other_messages=True,
                                                                     can_invite_users=True),
                                   )
    if not message.reply_to_message:
        return await message.reply("<b> Please Specify some one to kick bitch</b>")

    if user.is_chat_admin():
        await message.reply("<b>Are You serious ?</b>")
        return
    await message.reply(f'{message.reply_to_message.from_user.first_name} is Now UnMuted !!!')


@dp.message_handler(text_contains='unpin', is_chat_admin=True)
async def unpin(message: types.Message):
    await bot.unpin_chat_message(chat_id=message.chat.id)
    await message.reply("<b>UnPinned Chat message !!! </b>")


@dp.message_handler(content_types=["left_chat_member"])
async def left_chat(message: types.Message):
    await message.delete()


@dp.message_handler(text_contains=["promote"], is_chat_admin=True)
async def promote_admin(message: types.Message):
    if not message.reply_to_message:
        return await message.reply("<b> Please Specify some one to kick bitch</b>")

    await bot.promote_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                  can_change_info=False,
                                  can_post_messages=True,
                                  can_edit_messages=True,
                                  can_restrict_members=True,
                                  can_pin_messages=True,
                                  )
    await message.reply(f'{message.reply_to_message.from_user.first_name} is Now Admin :)')


@dp.message_handler(text_contains=['dice'])
async def send_dice(message: types.Message):
    await bot.send_dice(chat_id=message.chat.id)


@dp.message_handler(text_contains="lock on", is_chat_admin=True)
async def lock_gp(message: types.Message):
    await bot.set_chat_permissions(chat_id=message.chat.id,
                                   permissions=types.ChatPermissions(
                                       can_send_messages=False,
                                       can_send_media_messages=False,
                                       can_send_other_messages=False,
                                       can_pin_messages=False,
                                       can_change_info=False,
                                       can_invite_users=False,
                                       can_add_web_page_previews=False,

                                   ))
    await message.reply("Sucssesfuly Locked Group")


@dp.message_handler(text_contains=["lock off"], is_chat_admin=True)
async def unlock_gp(message: types.Message):
    await bot.set_chat_permissions(chat_id=message.chat.id,
                                   permissions=types.ChatPermissions(
                                       can_send_messages=True,
                                       can_send_media_messages=True,
                                       can_send_other_messages=True,
                                       can_pin_messages=False,
                                       can_change_info=True,
                                       can_invite_users=True,
                                       can_add_web_page_previews=True,

                                   ))
    await message.reply("Sucssesfuly UnLocked Group")


@dp.message_handler(text_contains='Link')
async def send_link(message: types.Message):
    LinK = await bot.export_chat_invite_link(message.chat.id)
    await message.reply(f'Link \n\n {LinK}')


@dp.message_handler(text_contains='group_info')
async def get_gp_info(message: types.Message):
    a = await bot.get_chat_administrators(message.chat.id)
    admin_User_name_list = []

    for i in a:
        admin_User_name_list.append(f'@{i.user.username}')
    admins = str(admin_User_name_list)
    admins = admins.replace('[', '')
    admins = admins.replace(']', '')
    admins = admins.replace("'", "")

    count = await bot.get_chat_members_count(message.chat.id)
    await message.reply(f'<b>Group Members = {count} \n\n Group Admins = {admins}</b>')


@dp.message_handler(text_contains='admins')
async def get_admins(message: types.Message):
    a = await bot.get_chat_administrators(message.chat.id)
    admin_User_name_list = []

    for i in a:
        admin_User_name_list.append(f'@{i.user.username}')
    admins = str(admin_User_name_list)
    admins = admins.replace('[', '')
    admins = admins.replace(']', '')
    admins = admins.replace("'", "")

    await message.reply(f'<b>Group admins \n\t{admins}</b>')


@dp.message_handler(text_contains='unban')
async def unban(message: types.Message):
    user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if not message.reply_to_message:
        return await message.reply("<b> Please Specify some one to kick bitch</b>")

    if user.is_chat_admin():
        await message.reply("<b>Are You serious ?</b>")
        return

    await bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
    await message.reply("Sucssesfully unbanned {}".format(message.reply_to_message.from_user.first_name))






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
