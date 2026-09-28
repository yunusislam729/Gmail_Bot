import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import time
import threading
import re

# ==================== CONFIG ====================
TOKEN = "8904363024:AAEjZAk7B9JL59_Nymq5OsJoPmzIzSUtm-M"
ADMIN_ID = 7244375873

bot = telebot.TeleBot(TOKEN)
user_accounts = {}
admins = [ADMIN_ID]
user_states = {}

# ==================== PREMIUM EMOJIS ====================
PEM = {
    "ok": '<tg-emoji emoji-id="5352694861990501856">✅</tg-emoji>',
    "no": '<tg-emoji emoji-id="5420130255174145507">❌</tg-emoji>',
    "warn": '<tg-emoji emoji-id="5336944168944047463">⚠️</tg-emoji>',
    "admin": '<tg-emoji emoji-id="5353032893096567467">📊</tg-emoji>',
    "user": '<tg-emoji emoji-id="5352861489541714456">👤</tg-emoji>',
    "file": '<tg-emoji emoji-id="5352721946054268944">📁</tg-emoji>',
    "rocket": '<tg-emoji emoji-id="5352597830089347330">🚀</tg-emoji>',
    "graph": '<tg-emoji emoji-id="5352877703043258544">📊</tg-emoji>',
    "money": '<tg-emoji emoji-id="5348469219761626211">💸</tg-emoji>',
    "gift": '<tg-emoji emoji-id="5420396762189831222">🎁</tg-emoji>',
    "msg": '<tg-emoji emoji-id="5337302974806922068">💬</tg-emoji>',
    "gear": '<tg-emoji emoji-id="5420155432272438703">⚙️</tg-emoji>',
    "link": '<tg-emoji emoji-id="5420517437885943844">🔗</tg-emoji>',
    "trash": '<tg-emoji emoji-id="5422557736330106570">🗑</tg-emoji>',
    "upload": '<tg-emoji emoji-id="5353001161878182134">📤</tg-emoji>',
    "world": '<tg-emoji emoji-id="5336972142066047577">🌐</tg-emoji>',
    "lock": '<tg-emoji emoji-id="5353022963132174959">🔐</tg-emoji>',
    "phone": '<tg-emoji emoji-id="5337132498965010628">📱</tg-emoji>',
    "num": '<tg-emoji emoji-id="5352862640592949843">🔢</tg-emoji>',
    "pin": '<tg-emoji emoji-id="5352922460897452503">📍</tg-emoji>',
    "star": '<tg-emoji emoji-id="5352552689983067014">✨</tg-emoji>',
    "hi": '<tg-emoji emoji-id="5353027129250453493">👋</tg-emoji>'
}

GLOBAL_BODY_EMOJIS = {
    "➖": "5870818207383686839", "🚫": "5334807341109908955", "😒": "5334763399299506604",
    "🖥": "5334880948259427772", "🌐": "5334590977837403844", "🌟": "5337102391244263212",
    "🕓": "5336983442125001376", "⌛": "5337172996211648018", "💬": "5337302974806922068",
    "🔐": "5337255927735163754", "🍏": "5337132498965010628", "❔": "5336850036145823599",
    "⚠️": "5336944168944047463", "🔥": "5337267511261960341", "💸": "5348469219761626211",
    "🥚": "5348390922507817684", "👨‍⚖": "5334763399299506604", "🐁": "5348494358205207761",
    "🧻": "5348486915026884464", "⚗": "5346311574221000149", "🛴": "5348075478634766440",
    "📊": "5353032893096567467", "🔢": "5352862640592949843", "👤": "5352861489541714456",
    "📁": "5352721946054268944", "🚀": "5352597830089347330", "💎": "5352838545826420397",
    "📍": "5352922460897452503", "👋": "5353027129250453493", "✅": "5352694861990501856",
    "1️⃣": "5352651766288652742", "2️⃣": "5355186458418257716", "3️⃣": "5352867219028091093",
    "4️⃣": "5352566657216714037", "5️⃣": "5353086880835474989", "6️⃣": "5354859211975071385",
    "7️⃣": "5352859127309707652", "8️⃣": "5352957533600389988", "9️⃣": "5353060913463204207",
    "🔤": "5352727417842606016", "📣": "5352980533150259581", "📤": "5353001161878182134",
    "✨": "5352552689983067014", "🔹": "5352638632278660622", "🎙": "5355102594886833928",
    "💴": "5352985330628730418", "📅": "5352585194295564660", "📴": "5352974971167611327",
    "✏️": "5395444784611480792", "📱": "5337132498965010628", "🔗": "5420517437885943844",
    "❌": "5420130255174145507", "⚙️": "5420155432272438703", "🫂": "5420145051336485498",
    "➕": "5420323438508155202", "🗑": "5422557736330106570", "🎁": "5420396762189831222",
    "➤": "5420618897898381296", "🏢": "5420156334215565595", "💳": "5190899075968441286",
    "📝": "5192739271886282680", "🛡": "5190447043545438788", "🤝": "5192805934073685937",
    "💰": "5190576863226933563", "👀": "5190645917711114179", "🕹": "5193100774988617665",
    "🟢": "5192812028632274956", "🧪": "5190781475468915802", "🎨": "5190751148704833975",
    "📂": "5257969839313526622", "🌍": "5780471598922337683", "📌": "5318986077455795572",
    "📢": "5789428375261023681", "🆔": "5352862640592949843", "📈": "5352877703043258544",
    "🔔": "5352980533150259581", "🏦": "5348469219761626211", "🧾": "5192739271886282680",
    "👨‍⚖️": "5334763399299506604", "🔍": "5463352748751753567",
    "🔑": "5197288647275071607"
}

def render_body_text(text):
    if not text:
        return str(text)
    parts = re.split(r'(<tg-emoji.*?</tg-emoji>)', str(text))
    for i in range(len(parts)):
        if not parts[i].startswith('<tg-emoji'):
            for normal_emj, prem_id in GLOBAL_BODY_EMOJIS.items():
                if normal_emj in parts[i]:
                    parts[i] = parts[i].replace(normal_emj, f'<tg-emoji emoji-id="{prem_id}">{normal_emj}</tg-emoji>')
    return "".join(parts)

def premium_header(title, icon="📧"):
    return f"╔══════════════════════════════════╗\n║   {icon}  {title}   ║\n╚══════════════════════════════════╝"

def premium_footer():
    return "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ==================== প্রিমিয়াম ইমোজি আইডি এক্সট্র্যাক্ট ====================
def get_emoji_id(emoji_tag):
    match = re.search(r'emoji-id="(\d+)"', emoji_tag)
    return match.group(1) if match else None

EMOJI_IDS = {
    "ok": get_emoji_id(PEM["ok"]),
    "no": get_emoji_id(PEM["no"]),
    "trash": get_emoji_id(PEM["trash"]),
    "user": get_emoji_id(PEM["user"]),
    "msg": get_emoji_id(PEM["msg"]),
    "link": get_emoji_id(PEM["link"]),
    "lock": get_emoji_id(PEM["lock"]),
    "phone": get_emoji_id(PEM["phone"]),
    "star": get_emoji_id(PEM["star"]),
    "gear": get_emoji_id(PEM["gear"]),
    "upload": get_emoji_id(PEM["upload"]),
    "world": get_emoji_id(PEM["world"]),
    "graph": get_emoji_id(PEM["graph"]),
    "money": get_emoji_id(PEM["money"]),
    "gift": get_emoji_id(PEM["gift"]),
    "rocket": get_emoji_id(PEM["rocket"]),
    "admin": get_emoji_id(PEM["admin"]),
    "warn": get_emoji_id(PEM["warn"]),
    "pin": get_emoji_id(PEM["pin"]),
    "num": get_emoji_id(PEM["num"]),
    "hi": get_emoji_id(PEM["hi"]),
}

# ==================== ইনলাইন কিবোর্ড বিল্ডার (স্টাইল + আইকন সহ) ====================
def build_inline_keyboard(buttons):
    """
    buttons: list of list of (text, callback_data/url, icon_key, style)
    style: "primary", "success", "danger", "secondary" (optional)
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    for row in buttons:
        row_btns = []
        for item in row:
            text = item[0]
            data = item[1]
            icon_key = item[2] if len(item) > 2 else None
            style = item[3] if len(item) > 3 else "primary"  # ডিফল্ট primary
            if data.startswith("http"):
                btn = InlineKeyboardButton(text=text, url=data)
            else:
                btn = InlineKeyboardButton(text=text, callback_data=data)
            if icon_key and icon_key in EMOJI_IDS:
                btn.icon_custom_emoji_id = EMOJI_IDS[icon_key]
            # স্টাইল যোগ করা
            btn.style = style
            row_btns.append(btn)
        keyboard.row(*row_btns)
    return keyboard

# ==================== MAIL.TM API ====================
def create_mail_tm_account(user_id):
    session = requests.Session()
    for _ in range(3):
        try:
            domains_res = session.get("https://api.mail.tm/domains", timeout=10)
            if domains_res.status_code != 200:
                continue
            domains = domains_res.json().get('hydra:member', [])
            if not domains:
                continue
            domain = domains[0]['domain']
            username = f"user{user_id}{int(time.time() * 1000)}"
            email = f"{username}@{domain}"
            password = f"Pass{user_id}123!@#"
            
            acc_res = session.post("https://api.mail.tm/accounts", json={"address": email, "password": password}, timeout=10)
            if acc_res.status_code not in [200, 201]:
                continue
                
            token_res = session.post("https://api.mail.tm/token", json={"address": email, "password": password}, timeout=10)
            if token_res.status_code == 200:
                token = token_res.json().get("token")
                user_accounts[user_id] = {"email": email, "token": token, "last_msg_id": None}
                return email
        except Exception:
            time.sleep(1)
            continue
    return None

def fetch_messages(token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        res = requests.get("https://api.mail.tm/messages", headers=headers, timeout=10)
        return res.json().get('hydra:member', [])
    except:
        return []

def fetch_message_detail(token, msg_id):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        res = requests.get(f"https://api.mail.tm/messages/{msg_id}", headers=headers, timeout=10)
        return res.json()
    except:
        return {}

def extract_otp(text):
    if not text:
        return None
    clean_text = re.sub(r'[\u200B-\u200D\uFEFF]', '', str(text))
    multi_part = re.search(r'(\d{3}[-\s]+\d{3})|(\d{2}[-\s]+\d{2}[-\s]+\d{2})', clean_text)
    if multi_part:
        return multi_part.group(0).replace(" ", "")
    otp_keywords = ['code', 'is', 'otp', 'pin', 'verification', 'auth', 'কোড', 'رمز', 'your code', 'verification code', 'activation code']
    keywords_pattern = '|'.join(otp_keywords)
    keyword_match = re.search(rf'(?:{keywords_pattern})\s*(?:is|:|-|=|of)?\s*([a-z0-9]{{4,10}})', clean_text, re.I)
    if keyword_match and keyword_match.group(1).isdigit():
        return keyword_match.group(1)
    keyword_match_rev = re.search(rf'([a-z0-9]{{4,10}})\s*(?:is your|is the|is|কোড|verification code|activation code)', clean_text, re.I)
    if keyword_match_rev and keyword_match_rev.group(1).isdigit():
        return keyword_match_rev.group(1)
    g_match = re.search(r'[Gg]-(\d{6})', clean_text)
    if g_match:
        return g_match.group(1)
    digit_matches = re.findall(r'(?<!\d)\d{4,8}(?!\d)', clean_text)
    if digit_matches:
        return max(digit_matches, key=len)
    return None

# ==================== কিবোর্ড ====================
def get_main_keyboard(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("📧 TEMP MAIL"))
    markup.row(KeyboardButton("💬 SUPPORT"))
    if user_id in admins:
        markup.row(KeyboardButton("🔒 Admin Panel"))
    return markup

def get_temp_mail_keyboard():
    return build_inline_keyboard([
        [("➕ Generate New", "gen_email", "ok", "success")],
        [("🗑 Delete", "del_email", "trash", "danger")],
        [("🔄 Refresh", "refresh_inbox", "upload", "primary")],
        [("❌ Close", "close_menu", "no", "danger")]
    ])

def get_admin_keyboard():
    return build_inline_keyboard([
        [("👥 Total Users", "admin_users", "user", "primary")],
        [("➕ Add Admin", "admin_add", "plus", "success")],
        [("📢 Broadcast", "admin_broadcast", "msg", "primary")],
        [("❌ Close", "close_menu", "no", "danger")]
    ])

def get_support_keyboard():
    return build_inline_keyboard([
        [("📩 Contact Support", "https://t.me/Himel8200", "msg", "primary")],
        [("❌ Close", "close_menu", "no", "danger")]
    ])

# ==================== BOT HANDLERS ====================
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    premium_start = (
        f"{premium_header('TEMP MAIL BOT', '📧')}\n\n"
        f"{PEM['star']} <b>Welcome to Premium Temp Mail!</b>\n\n"
        f"{PEM['phone']} Get disposable email addresses\n"
        f"{PEM['lock']} Receive OTPs instantly here\n"
        f"{PEM['ok']} 100% Safe & Anonymous\n\n"
        f"{premium_footer()}\n"
        f"👇 <b>Choose an option below</b>"
    )
    bot.reply_to(
        message,
        render_body_text(premium_start),
        reply_markup=get_main_keyboard(user_id),
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda m: m.text == "📧 TEMP MAIL")
def temp_mail_menu(message):
    user_id = message.from_user.id
    data = user_accounts.get(user_id)
    
    if not data:
        text = (
            f"{premium_header('TEMP MAIL SERVICE', '📧')}\n\n"
            f"{PEM['no']} You don't have an email address yet.\n\n"
            f"👉 Tap <b>Generate New</b> to create one."
        )
        bot.send_message(user_id, render_body_text(text), parse_mode="HTML", reply_markup=get_temp_mail_keyboard())
        return
    
    email = data['email']
    token = data['token']
    messages = fetch_messages(token)
    msg_count = len(messages)
    
    inbox_text = ""
    if messages:
        latest = messages[0]
        detail = fetch_message_detail(token, latest['id'])
        subject = detail.get('subject', 'No Subject')
        body = detail.get('text', detail.get('intro', ''))
        otp = extract_otp(body) or extract_otp(subject) or "None"
        inbox_text = f"{PEM['msg']} <b>{subject}</b>\n{PEM['lock']} <b>OTP:</b> <code>{otp}</code>\n\n📝 {body[:100]}..."
    else:
        inbox_text = f"{PEM['msg']} No messages yet."
    
    text = (
        f"{premium_header('TEMP MAIL INBOX', '📧')}\n\n"
        f"{PEM['link']} <b>Email:</b> <code>{email}</code>\n"
        f"{PEM['num']} <b>Messages:</b> {msg_count}\n\n"
        f"{premium_footer()}\n{inbox_text}"
    )
    bot.send_message(user_id, render_body_text(text), parse_mode="HTML", reply_markup=get_temp_mail_keyboard())

@bot.message_handler(func=lambda m: m.text == "💬 SUPPORT")
def support_menu(message):
    text = (
        f"{premium_header('SUPPORT CENTER', '💬')}\n\n"
        f"{PEM['msg']} <b>Contact Support</b>\n\n"
        f"{PEM['user']} @Himel8200\n"
        f"{PEM['link']} himel8200@gmail.com\n\n"
        f"{premium_footer()}\n"
        f"🕐 <i>We're here to help you 24/7!</i>"
    )
    bot.send_message(message.from_user.id, render_body_text(text), parse_mode="HTML", reply_markup=get_support_keyboard())

@bot.message_handler(func=lambda m: m.text == "🔒 Admin Panel")
def admin_panel(message):
    user_id = message.from_user.id
    if user_id not in admins:
        bot.reply_to(message, render_body_text(f"{PEM['no']} <b>Unauthorized Access!</b>\n\nYou don't have permission to view this panel."), parse_mode="HTML")
        return
    text = (
        f"{premium_header('ADMIN PANEL', '🔒')}\n\n"
        f"{PEM['user']} <b>Total Users:</b> {len(user_accounts)}\n\n"
        f"{premium_footer()}\n"
        f"⚙️ <i>Manage your bot from here.</i>"
    )
    bot.send_message(user_id, render_body_text(text), parse_mode="HTML", reply_markup=get_admin_keyboard())

# ==================== CALLBACK HANDLERS ====================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    if call.data == "gen_email":
        bot.answer_callback_query(call.id, "⏳ Creating email...")
        if user_id in user_accounts:
            del user_accounts[user_id]
        email = create_mail_tm_account(user_id)
        if email:
            bot.edit_message_text(
                render_body_text(f"{PEM['ok']} Email created successfully!\n📧 <code>{email}</code>"),
                chat_id, msg_id, parse_mode="HTML"
            )
            time.sleep(1)
            temp_mail_menu(call.message)
        else:
            bot.edit_message_text(
                render_body_text(f"{PEM['no']} Failed to create email. Please try again."),
                chat_id, msg_id
            )

    elif call.data == "del_email":
        bot.answer_callback_query(call.id, "🗑 Deleting...")
        if user_id in user_accounts:
            del user_accounts[user_id]
        bot.edit_message_text(render_body_text(f"{PEM['trash']} Email deleted successfully!"), chat_id, msg_id)
        time.sleep(1)
        temp_mail_menu(call.message)

    elif call.data == "refresh_inbox":
        bot.answer_callback_query(call.id, "🔄 Refreshing...")
        temp_mail_menu(call.message)

    elif call.data == "close_menu":
        bot.delete_message(chat_id, msg_id)

    elif call.data == "admin_users":
        if user_id not in admins:
            bot.answer_callback_query(call.id, "⛔ Unauthorized!", show_alert=True)
            return
        bot.answer_callback_query(call.id, f"👥 Total Users: {len(user_accounts)}", show_alert=True)

    elif call.data == "admin_add":
        if user_id not in admins:
            bot.answer_callback_query(call.id, "⛔ Unauthorized!", show_alert=True)
            return
        bot.answer_callback_query(call.id)
        user_states[user_id] = "waiting_for_admin_id"
        bot.send_message(
            user_id,
            "📝 Send the User ID of the new admin:\n\nExample: 123456789"
        )

    elif call.data == "admin_broadcast":
        if user_id not in admins:
            bot.answer_callback_query(call.id, "⛔ Unauthorized!", show_alert=True)
            return
        bot.answer_callback_query(call.id)
        user_states[user_id] = "waiting_for_broadcast"
        bot.send_message(
            user_id,
            "📢 Send the message you want to broadcast to all users.\n\n(You can send text, photo, video, or any file)"
        )

    else:
        bot.answer_callback_query(call.id, "Unknown action")

# ==================== STATE MESSAGES ====================
@bot.message_handler(func=lambda m: m.from_user.id in user_states)
def handle_state_messages(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if state == "waiting_for_admin_id":
        if message.text and message.text.isdigit():
            new_admin = int(message.text)
            if new_admin not in admins:
                admins.append(new_admin)
                bot.reply_to(message, f"✅ Admin added successfully!\nUser ID: {new_admin}")
            else:
                bot.reply_to(message, f"⚠️ User {new_admin} is already an admin.")
        else:
            bot.reply_to(message, "❌ Invalid User ID! Please send a numeric ID.")
        del user_states[user_id]

    elif state == "waiting_for_broadcast":
        bot.reply_to(message, "📢 Broadcasting started...")
        success = 0
        failed = 0
        for uid in list(user_accounts.keys()):
            try:
                bot.copy_message(uid, message.chat.id, message.message_id)
                success += 1
            except:
                failed += 1
            time.sleep(0.05)
        bot.reply_to(
            message,
            f"✅ Broadcast completed!\n\n✅ Success: {success}\n❌ Failed: {failed}\n👥 Total Users: {len(user_accounts)}"
        )
        del user_states[user_id]

# ==================== AUTO CHECKER ====================
def auto_checker():
    while True:
        try:
            for user_id, data in list(user_accounts.items()):
                try:
                    token = data['token']
                    messages = fetch_messages(token)
                    if messages and messages[0]['id'] != data['last_msg_id']:
                        user_accounts[user_id]['last_msg_id'] = messages[0]['id']
                        msg = messages[0]
                        detail = fetch_message_detail(token, msg['id'])
                        sender = detail.get('from', {}).get('address', 'Unknown')
                        subject = detail.get('subject', 'No Subject')
                        body = detail.get('text', detail.get('intro', ''))
                        otp = extract_otp(body) or extract_otp(subject) or "None"
                        
                        markup = build_inline_keyboard([
                            [("Open in Browser ➡️", "https://mail.tm/", "link", "primary")]
                        ])
                        
                        auto_msg = (
                            f"{premium_header('NEW EMAIL RECEIVED', '📩')}\n\n"
                            f"{PEM['link']} From: <code>{sender}</code>\n"
                            f"{PEM['pin']} Subject: <b>{subject}</b>\n"
                            f"{PEM['lock']} <b>OTP:</b> <code>{otp}</code>\n\n"
                            f"{PEM['msg']} Message:\n<code>{body[:300]}</code>\n\n"
                            f"{premium_footer()}"
                        )
                        try:
                            bot.send_message(user_id, render_body_text(auto_msg), parse_mode="HTML", reply_markup=markup)
                        except:
                            pass
                except:
                    pass
        except:
            pass
        time.sleep(5)

# ==================== START ====================
if __name__ == "__main__":
    print("🤖 Premium Temp Mail Bot started...")
    threading.Thread(target=auto_checker, daemon=True).start()
    bot.infinity_polling(skip_pending=True)