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
    await message.reply(f"Welcome {message.from_user.id} \n \
    Well This is a helper bot that manage your groups =) Hope you enjoy This :)")


@dp.message_handler(commands="help")
async def help_(message: types.Message):
    await message.reply("""well hi {} iam TyNy bot Im here to manage your groups \n\n Notice : DO NOT FORGET TO MAKE ME ADMIN
                        My Commands = 
                            /ban => use this to kick someone from your group
                            /mute [time] => use this to mute someone
                            pin => use this to pin a message 
                            unpin => use this to unpin your group message
                            unban => use this to unban a banned member :|
                            dice => Fun command 
                            group info => shows your group info
                            admins => shows admin groups :/
                            lock on => it will lock your group ( No one can send message until you unlock it)
                            lock off => it will unlock your group
                            lock content => it will lock the media messages :/
                            unlock content => it will unlock your contents 
                            Link => it will show you your group link 
                            world info => shows some information about corona virus and BTC Price 

                            and .....
                            HOPE YOU ENJOY =) 
    """
                        )


@dp.message_handler(is_chat_admin=True, commands=['admin_check'])
async def handler3(msg: types.Message):
    try:
        await msg.answer("<b>You Are Admin</b>")
    except:
        await msg.reply("<b> You're Not Admin :( </b>")


@dp.message_handler(commands='world info')
async def world_info(msg: types.Message):
    global corona_death, corona_cases
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
        f'<b>Corona Cases: \n {corona_cases} \n\nCorona Deaths : \
        {corona_death} \n\n BTC Price : \n {bitcoin_price} </b>'
    )


@dp.message_handler(content_types=["new_chat_members"])
async def on_user_join(message: types.Message):
    try:
        a = message.new_chat_members
        for i in a:
            if i.mention.endswith("bot"):
                await bot.kick_chat_member(chat_id=message.chat.id, user_id=i.id)
                await message.reply("<b>Hey You cannot add bots here</b>")
            else:

                await message.reply(f'<b>salam {i.mention} jende khoshomadi</b>')

        await message.delete()
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


@dp.message_handler(is_chat_admin=True, commands=["ban"])
async def kick_(message: types.Message):
    try:
        user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        if not message.reply_to_message:
            return await message.reply("<b> SPECIFY SOMEONE !!!!</b>")

        if user.is_chat_admin():
            await message.reply("<b>funny joke lol </b>")
            return

        await bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        await message.reply("Successfully removed {}".format(message.reply_to_message.from_user.first_name))
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


@dp.message_handler(text_contains=['delete'], is_chat_admin=True)
async def delete_message(message: types.Message):
    try:
        await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
        await bot.delete_message(message_id=message.reply_to_message.message_id, chat_id=message.chat.id)
    except:
        pass


@dp.message_handler(commands='pin', is_chat_admin=True)
async def pin_something(message: types.Message):
    try:
        await bot.pin_chat_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


@dp.message_handler(commands='mute', is_chat_admin=True)
async def mute(message: types.Message):
    try:
        user = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        if not message.reply_to_message:
            return await message.reply("<b> SPECIFY SOMEONE TO MUTE PLEASE !!!</b>")

        if user.is_chat_admin():
            await message.reply("<b> IT WASN'T FUNNY </b>")
            return
        if len(message.text.split()) == 2:

            until_mute = int(message.text.split()[1])
            # Converting seconds to minute :|
            until_mute = until_mute * 60

            await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                           permissions=types.ChatPermissions(can_send_message=False,
                                                                             can_pin_messages=False,
                                                                             can_send_other_messages=False,
                                                                             can_invite_users=False),
                                           until_date=int(time()) + int(until_mute))
            hours = int(until_mute) / 3600
            await message.reply(f'{message.reply_to_message.from_user.first_name} is Muted for {str(hours)} hours')
        else:

            await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                           permissions=types.ChatPermissions(can_send_message=False,
                                                                             can_pin_messages=False,
                                                                             can_send_other_messages=False,
                                                                             can_invite_users=False),
                                           until_date=int(time()) + 7200)
            await message.reply(f'{message.reply_to_message.from_user.first_name} is Muted for 2 hours !!!')
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


@dp.message_handler(text_contains='unmute', is_chat_admin=True)
async def unmute(message: types.Message):
    try:
        user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                       permissions=types.ChatPermissions(can_send_message=True, can_pin_messages=True,
                                                                         can_send_other_messages=True,
                                                                         can_invite_users=True),
                                       )
        if not message.reply_to_message:
            return await message.reply("<b> :| YOU DIDN'T SPECIFY SOME ONE !!</b>")

        if user.is_chat_admin():
            await message.reply("<b>lol it wasn't funny </b>")
            return
        await message.reply(f'{message.reply_to_message.from_user.first_name} is Now Unmuted !!!')
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


@dp.message_handler(text_contains='unpin', is_chat_admin=True)
async def unpin(message: types.Message):
    try:
        await bot.unpin_chat_message(chat_id=message.chat.id)
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


@dp.message_handler(content_types=["left_chat_member"])
async def left_chat(message: types.Message):
    await message.reply(f"i will remember you {message.from_user.username} =(")
    try:
        await message.delete()
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


@dp.message_handler(text_contains=["promote"], is_chat_admin=True)
async def promote_admin(message: types.Message):
    try:
        if not message.reply_to_message:
            return await message.reply("<b> :|</b>")

        await bot.promote_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                      can_change_info=False,
                                      can_post_messages=True,
                                      can_edit_messages=True,
                                      can_restrict_members=True,
                                      can_pin_messages=True,
                                      )
        await message.reply(f'{message.reply_to_message.from_user.first_name} is Now Admin :)')
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


@dp.message_handler(text_contains=['dice'])
async def send_dice(message: types.Message):
    await bot.send_dice(chat_id=message.chat.id)


@dp.message_handler(text_contains="lock on", is_chat_admin=True)
async def lock_gp(message: types.Message):
    try:
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
        await message.reply("Successfully Locked Group")
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


@dp.message_handler(text_contains=["lock off"], is_chat_admin=True)
async def unlock_gp(message: types.Message):
    try:
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
        await message.reply("Successfully UnLocked Group")
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


@dp.message_handler(text_contains='Link')
async def send_link(message: types.Message):
    try:
        LinK = await bot.export_chat_invite_link(message.chat.id)
        await message.reply(f'Link \n\n {LinK}')
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


@dp.message_handler(text_contains='group info')
async def get_gp_info(message: types.Message):
    a = await bot.get_chat_administrators(message.chat.id)
    admin_user_name_list = []

    for i in a:
        admin_user_name_list.append(f'@{i.user.username}')
    admins = str(admin_user_name_list)
    # i know this is kinda weird :| but when i tried to edit a message i get some bullshit error from telegram sorry :(
    admins = admins.replace('[', '')
    admins = admins.replace(']', '')
    admins = admins.replace("'", "")

    count = await bot.get_chat_members_count(message.chat.id)
    await message.reply(f'<b>Group Members = {count} \n\n Group Admins = {admins}</b>')


@dp.message_handler(text_contains='admins')
async def get_admins(message: types.Message):
    a = await bot.get_chat_administrators(message.chat.id)
    admin_user_name_list = []

    for i in a:
        admin_user_name_list.append(f'@{i.user.username}')
    admins = str(admin_user_name_list)
    admins = admins.replace('[', '')
    admins = admins.replace(']', '')
    admins = admins.replace("'", "")

    await message.reply(f'<b>Group admins \n\t{admins}</b>')


@dp.message_handler(text_contains='unban', is_chat_admin=True)
async def unban(message: types.Message):
    try:
        user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        if not message.reply_to_message:
            return await message.reply("<b>IT WASN'T FUNNY BRO</b>")

        if user.is_chat_admin():
            await message.reply("<b>Are You serious ?</b>")
            return

        await bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        await message.reply("Successfully unbanned {}".format(message.reply_to_message.from_user.first_name))
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


@dp.message_handler(text_contains="lock contents", is_chat_admin=True)
async def lock_contents(message: types.Message):
    try:
        await bot.set_chat_permissions(chat_id=message.chat.id,
                                       permissions=types.ChatPermissions(
                                           can_send_media_messages=False,
                                           can_send_other_messages=False,
                                           can_pin_messages=False,
                                           can_change_info=False,
                                           can_invite_users=False,
                                           can_add_web_page_previews=False

                                       ))
        await message.reply("Successfully Locked Media ")
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


@dp.message_handler(text_contatins="unlock contents", is_chat_admin=True)
async def unlock_contents(message: types.Message):
    try:
        await bot.set_chat_permissions(chat_id=message.chat.id,
                                       permissions=types.ChatPermissions(
                                           can_send_media_messages=True,
                                           can_send_other_messages=True,
                                           can_pin_messages=False,
                                           can_change_info=False,
                                           can_invite_users=True,
                                           can_add_web_page_previews=False

                                       ))
        await message.reply("Successfully unlocked Media ")
    except:
        await message.reply("Error Do I have Enough permissions to do this ? ")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)