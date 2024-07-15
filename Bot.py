from telethon import TelegramClient, events, functions
import re

api_id = '22309313'
api_hash = 'b05c07695a3974762a6cf9dd0244a2f5'

client = TelegramClient('user', api_id, api_hash).start()

admin_mod = ____
user_ids = set(5093051866)
keywords = ['يكتب', 'يرسل', 'يبعت', 'يقول', 'اول']
cut_off_words = {
    'ࢪ': 'ر', '؏': 'ع', 'آ': 'ا', 'ٱ': 'ا', 'ے': '', 'ـ': '', 'اول ': '', 'اسم': '',
    'ۅ': 'و', 'حركات': '', '()': '', 'وبالايموجي': '', 'بالايموجي': '', 'يكتب ': '',
    'واحد ': '', ' خليت حركات حته محد ينسخ': '', 'الشات': '', 'بلشات': '', 'فلشات': '',
    'بدون ': '', 'شخص': '', 'اقواس': '', 'بلاقواس': '', 'فالتعليقات': '', 'التعليقات': '', 'بالتعليقات': '',
    'أول ': '', 'فلبوت': '', 'اقواص': '', 'ايموجي': '', 'ݪ': 'ل', 'ݛ': 'ر', 'حرڪات': '',
    'مع ': '', 'ڪ': 'ك', 'گ': 'ك', 'بل ': '', 'مفعل لا تشارك': '', 'أ': 'ا', 'شات ': '',
    'gbfjcfbknkgfbot': '', 'كلمه': '', 'First': '', 'first': '', 'FIRST': '', 'ټ': 'ت',
    'ډ': 'د', 'ﺂ': 'ا', 'ﺑ': 'ب', 'خاص': '', 'ڝ': 'ص', 'ﻣ': 'م', 'ט': 'ن', 'ڼ': 'ن',
    'נ': 'د', 'ﺣ': 'ح', 'ہ': 'ه', 'J_KO_Lbot': '', 'الشات': '', 'بلتعليقات': '', 'في ': '', 'بلا ': '', 'نقاط ': '', 'في ': '', 'بل ': '', 'شات': '', 'في ': '', 'كلمة ': '', 'كلمه ': '',
    'يقول ': '', 'يكتب ': '', 'مناقشه ': '', 'كومنت ': '', 'كمنت ': '', 'l_v_0bot': '', 'ک': 'ك', 'او ل': '', 'ا ول': '', 'ا و ل': '', 'ا و  ل': '', 'يحط': '', 'يرسل': '',
    'ف ': '', 'بالتشكيل': '', 'الحركات': '', 'تشكيل': ''
}
activated_channels = set()

async def can_comment_in_channel(channel_id):
    try:
        result = await client(functions.channels.GetParticipantRequest(channel=channel_id, participant='me'))
        return result.participant.can_send_messages
    except:
        return False

def get_clean_response(text):
    for word, replacement in cut_off_words.items():
        text = text.replace(word, replacement)
    return text.strip()

def extract_text_in_parentheses(text):
    return re.findall(r'\(([^()]*)\)', text)

async def get_user_info(user_id):
    try:
        user = await client.get_entity(user_id)
        return f"[{user.first_name}](tg://user?id={user_id})"
    except:
        return f"[غير معروف](tg://user?id={user_id})"

@client.on(events.NewMessage())
async def handler(event):
    sender_id = (await event.get_sender()).id
    message = event.raw_text.strip()

    if sender_id == admin_mod:
        if message.lower().startswith('/set '):
            user_id = int(message.split()[1])
            if len(user_ids) < 10:
                user_ids.add(user_id)
                await event.reply(f"تمت إضافة {user_id}.")
            else:
                await event.reply("لا يمكنك إضافة أكثر من 10 مستخدمين.")
            return

        if message.lower() == "/ls":
            if user_ids:
                user_list = [f"{user_id} - {await get_user_info(user_id)}" for user_id in user_ids]
                await event.reply("المستخدمين الحاليين:\n" + "\n".join(user_list))
            else:
                await event.reply("لا يوجد مستخدمين حاليين.")
            return

        if message.lower().startswith('/r '):
            index = int(message.split()[1])
            if 1 <= index <= len(user_ids):
                user_id = list(user_ids)[index - 1]
                user_ids.remove(user_id)
                await event.reply(f"تم حذف {user_id}.")
            else:
                await event.reply("الرقم غير صحيح.")
            return

        if message.lower() == "/help":
            help_text = (
                "/set [user_id] - تعيين مستخدم لمراقبته.\n"
                "/ls - عرض قائمة المستخدمين المراقبين مع أسمائهم وروابطهم.\n"
                "/r [index] - حذف مستخدم من قائمة المراقبين حسب الرقم.\n"
                "ايرور - تفعيل القناة.\n"
                "404 - إلغاء تفعيل القناة.\n"
            )
            await event.reply(help_text)
            return

        if message.lower() == "ايرور":
            activated_channels.add(event.chat_id)
            await event.reply(".")
            return

        if message.lower() == "404":
            activated_channels.discard(event.chat_id)
            await event.reply(".")
            return

    if sender_id in user_ids:
        if event.chat_id in activated_channels:
            matches = extract_text_in_parentheses(message)
            keyword_match = re.search(r'\b(?:' + '|'.join(keywords[:-1]) + r')\b\s*(.*)', message)
            if not keyword_match:
                keyword_match = re.search(r'\bاول\b\s*(.*)', message)
            username_match = re.search(r'@(\w+)', message)

            if matches:
                response = matches[0]
                if response:  
                    if username_match:
                        username = username_match.group(1)
                        await client.send_message(f'@{username}', response)
                    else:
                        if event.is_channel:
                            can_comment = await can_comment_in_channel(event.chat_id)
                            if can_comment:
                                await event.reply(response)
                            else:
                                await client.send_message(event.chat_id, response, comment=True)
                        else:
                            await event.reply(response)
            elif username_match and keyword_match:
                response = get_clean_response(keyword_match.group(1))
                if response:  
                    username = username_match.group(1)
                    await client.send_message(f'@{username}', response)
            elif keyword_match:
                response = get_clean_response(keyword_match.group(1))
                if response: 
                    await event.reply(response)
            else:
                matches = re.findall(r'(\d+(?:\.\d+)?[\+\-\*/]\d+(?:\.\d+)?)', message)
                if matches:
                    for expr in matches:
                        try:
                            result = eval(expr)
                            await event.reply(f" {result}")
                        except:
                            await event.reply(f"Error in evaluating '{expr}'")

client.run_until_disconnected()

# t.me/JJ7AA
# t.me/JJ7AA
# t.me/JJ7AA
# t.me/JJ7AA
