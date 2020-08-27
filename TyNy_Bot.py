import logging
import random
import requests
from bs4 import BeautifulSoup
from aiogram.dispatcher.filters import BoundFilter, Text
from aiogram import Bot, Dispatcher, executor, md, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified, Throttled
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import asyncio
from colorama import Fore
from time import time
from subprocess import check_output
import re
import os
API_TOKEN = os.getenv("Telegram Token")
logging.basicConfig(level=logging.INFO)
storage = RedisStorage2(db=5)
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

def main_markup():
    markup = types.InlineKeyboardMarkup(row_width=3)
    help_markup = types.InlineKeyboardButton("Bot Commands :D", callback_data="help_cb")
    aboutDev_markup = types.InlineKeyboardButton("About Developer ", callback_data="ad_cb")
    markup.add(help_markup)
    markup.add(aboutDev_markup)
    markup.add(
        # url buttons have no callback data
        types.InlineKeyboardButton('Add me to your group :D', url='https://telegram.me/TyNy_Robot?startgroup=new'),
    )
    return markup


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(f"Welcome {message.from_user.first_name}", reply_markup=main_markup())


def back_to_first():
    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton("<< BACK", callback_data="back_to_main")
    markup.add(back)
    return markup

@dp.callback_query_handler(text="help_cb")
@dp.callback_query_handler(text="ad_cb")
async def help_(query: types.CallbackQuery):
    answer_data = query.data
    query.answer("welcome ...")
    if answer_data == "help_cb":

        await bot.send_message(query.from_user.id,"""
        well hi {} iam TyNy bot Im here to manage your groups \n\n Notice : DO NOT FORGET TO MAKE ME ADMIN
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
        """.format(query.from_user.first_name)
                            ,reply_markup=back_to_first())
    elif answer_data == "ad_cb":
        await bot.send_message(query.from_user.id,"""
            Developed by iPzX 
            
            @iPzXx
            source = https://github.com/ipzx/TyNy-bot

        """, reply_markup=back_to_first())


@dp.message_handler(commands=["help"])
async def nw_help(message: types.Message):
    await message.reply("""
        well hi iam TyNy bot Im here to manage your groups \n\n Notice : DO NOT FORGET TO MAKE ME ADMIN
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
        """)

@dp.callback_query_handler(text="back_to_main")
async def btm(query: types.CallbackQuery):
    answer_data = query.data
    if answer_data == "back_to_main":
        query.answer("....")
        await query.message.edit_text("Welcome", reply_markup=main_markup())
    else:
        query.answer("oops Error :(")



@dp.message_handler(commands='stuff')
async def world_info(msg: types.Message):
    mu = types.InlineKeyboardMarkup(row_width=3)

    r = requests.post("https://www.worldometers.info/coronavirus/")
    content = BeautifulSoup(r.text)
    for i in content.findAll('span', {'style': 'color:#aaa'}):
        corona_cases = i.text

    corona_case = types.InlineKeyboardButton(f"Corona Cases: {corona_cases}",
    callback_data='cc')

    for j in content.findAll('div', {'class': 'maincounter-number'}):
        corona_death = j.text

    corona_d = types.InlineKeyboardButton(f"Corona Deathes: {corona_death}",
    callback_data='cd')
    resp = requests.get('https://api.coinbase.com/v2/prices/buy?currency=USD',
                        proxies={'http': 'socks5://207.97.174.134:1080'})
    bitcoin_price = float(resp.json()['data']['amount'])
    btc = types.InlineKeyboardButton(f"BTC : {bitcoin_price}",
    callback_data='btc')
    mu.add(corona_case)
    mu.add(corona_d)
    mu.add(btc)

    await msg.reply(f'<b>well well... </b>', reply_markup=mu)

@dp.callback_query_handler(text='cc')
@dp.callback_query_handler(text='cd')
@dp.callback_query_handler(text='btc')
async def stuff(query: types.CallbackQuery):
    if query.answer == "cc" or "cd" or "btc":
        await query.answer("OK FUCK U")

@dp.message_handler(content_types=["new_chat_members"])
async def on_user_join(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            "Read Rules :D ",
            url="#"
        )
    )

    try:
        a = message.new_chat_members
        for i in a:
            if i.mention.endswith("bot"):
                await bot.kick_chat_member(chat_id=message.chat.id, user_id=i.id)
                await message.reply("<b>Hey You cannot add bots here</b>")

            else:

                await message.reply(f'<b>salam {i.mention} jende khoshomadi</b>', reply_markup=markup)

        await message.delete()
    except:
        pass


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
        pass

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


@dp.message_handler(commands='group_info')
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
    mu = types.InlineKeyboardMarkup(row_width=1)
    
    a = await bot.get_chat_administrators(message.chat.id)
    admin_user_name_list = []

    for i in a:
        admin_user_name_list.append(f'@{i.user.username}')
    admins = str(admin_user_name_list)
    admins = admins.replace('[', '')
    admins = admins.replace(']', '')
    admins = admins.replace("'", "")
    if "@None" in admins:
        admins = admins.replace("@None", "")
    admin_cache = types.InlineKeyboardButton(f' Admin Caches : {len(admins.split())}', callback_data='admins')
    mu.add(admin_cache)
    await message.reply(f'<b>Group admins \n\t{admins}</b>', reply_markup=mu)


@dp.message_handler(commands='admins')
async def get_admins(message: types.Message):
    mu = types.InlineKeyboardMarkup(row_width=1)
    
    a = await bot.get_chat_administrators(message.chat.id)
    admin_user_name_list = []

    for i in a:
        admin_user_name_list.append(f'@{i.user.username}')
    admins = str(admin_user_name_list)
    admins = admins.replace('[', '')
    admins = admins.replace(']', '')
    admins = admins.replace("'", "")
    if "@None" in admins:
        admins = admins.replace("@None", "")
    admin_cache = types.InlineKeyboardButton(f' Admin Caches : {len(admins.split())}', callback_data='admins')
    mu.add(admin_cache)
    await message.reply(f'<b>Group admins \n\t{admins}</b>', reply_markup=mu)

@dp.callback_query_handler(text='admins')
async def adm(query: types.CallbackQuery):
    answer_data = query.data
    if answer_data == "admins":
        await query.answer("OK FUCK U ")


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


@dp.message_handler(text_contains="unlock contents", is_chat_admin=True)
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


def get_ip(ip):
    ip = ip.strip()
    url = 'http://ip-api.com/json/%s'% ip
    answer = requests.get(url)
    data1 = answer.text
    data2 = re.sub(',','\n',data1)
    data3 = re.sub('"',' ',data2)
    data4 = data3.strip('{}')
    data5 = data4.replace('query','ip entered')
    return data5

@dp.message_handler(commands=["ip"])
async def ip(message: types.Message):
    if "/ip" in message.text:
        ip = message.text.split()[1]
        func_ip = get_ip(ip)
        await message.reply(func_ip)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
