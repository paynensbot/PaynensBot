import telebot
from telebot import types
import time
import sqlite3

# --- TOKENS ---
MAIN_TOKEN = "8274131187:AAGKOqCoxRVHBDE1Dbs_8JayZjqUqbvB2Ek"
ADMIN_BOT_TOKEN = "8545462700:AAGY-mbK2_ZbbNORIJjRmUdQ5H4UG8Rwn4M"
MY_ID = "8487366702"

bot = telebot.TeleBot(MAIN_TOKEN)
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('paynens_final.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (user_id TEXT PRIMARY KEY, name TEXT, balance REAL, tasks_count INTEGER, 
                  referrals INTEGER, last_task_time REAL, lang TEXT)''')
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('paynens_final.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def update_db(query, params):
    conn = sqlite3.connect('paynens_final.db')
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

init_db()

# --- LINKS ---
LINKS = [
    "https://t.me/gamee/start?startapp=eyJyZWYiOjg0ODczNjY3MDJ9",
    "https://shrinkme.click/7p09BcsN",
    "https://shrinkme.click/Da1ql2OX",
    "https://shrinkme.click/ybJYLh",
    "https://shrinkme.click/fa80KpHG",
    "https://shrinkme.click/trWsrG",
    "https://shrinkme.click/LxlIbK",
    "https://shrinkme.click/2lVK",
    "https://omg10.com/4/10492994",
    "https://omg10.com/4/10493013",
    "https://omg10.com/4/10493006",
    "https://omg10.com/4/10493007",
    "https://omg10.com/4/10492991",
    "https://omg10.com/4/10493005",
    "https://omg10.com/4/10492993",
    "https://omg10.com/4/10493004",
    "https://omg10.com/4/10492936",
    "https://omg10.com/4/10492999",
    "https://youtube.com/@inistaofficiell?si=KQpfsjEZhEIc_SoL",
    "https://youtu.be/0dmFAt5e1Kw?si=DwNnZ26hA-olA482",
    "https://www.instagram.com/inistaofficiell?igsh=a3V3OGEzZGh3Y3Bj",
    "http://t.me/StarsMakeBot?start=cKXmNrX0Y",
    "https://www.effectivegatecpm.com/jyspkti4p?key=02360198cbc2c2a4d9d2c7080d9222fc",
    "https://t.me/dz1xbet_2",
    "https://www.effectivegatecpm.com/jgn8ye2pv?key=bb923e278557fb9b5e9a2613cf0dac7f",
    "https://www.effectivegatecpm.com/vz6cvs2518?key=a5bc3af46bac80482b8d4e36a0001e88",
    "https://reward-me.eu/ae0ace42-07f5-11f1-8a73-129a1c289511",
    "https://www.effectivegatecpm.com/rgudphv5?key=a31db716ac8d5da42a64a1a6625fa7ab",
    "https://www.effectivegatecpm.com/v41im7s8?key=71cf533d5cc0a76e55e9a9545d527f49",
    "https://www.effectivegatecpm.com/njze4eg1xg?key=159eb9bfcd4ae292e143bc346e6aa518"
]

# --- KEYBOARDS ---
def main_kb(lang):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ar':
        kb.add("💰 اكسب المال")
        kb.add("🏦 سحب الأرباح")
        kb.row("👥 دعوة الأصدقاء", "📽 لإعلاناتكم")
        kb.row("👤 الملف الشخصي", "📊 الإحصائيات")
    else:
        kb.add("💰 Earn Money")
        kb.add("🏦 Withdraw Profits")
        kb.row("👥 Invite Friends", "📽 Advertise")
        kb.row("👤 Profile", "📊 Statistics")
    return kb

def back_kb(lang):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🔙 العودة للقائمة الرئيسية" if lang == 'ar' else "🔙 Back to Main Menu")
    return kb

# --- BOT ENGINE ---
@bot.message_handler(commands=['start'])
def start(m):
    uid = str(m.chat.id)
    ref = m.text.split()[1] if len(m.text.split()) > 1 else None
    if not get_user(uid):
        conn = sqlite3.connect('paynens_final.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (uid, m.from_user.first_name, 0.0, 0, 0, 0.0, 'none'))
        if ref and ref != uid:
            c.execute("UPDATE users SET balance = balance + 0.5, referrals = referrals + 1 WHERE user_id=?", (ref,))
            try: admin_bot.send_message(ref, "🎁 New Referral! +0.5$")
            except: pass
        conn.commit(); conn.close()
    
    ikb = types.InlineKeyboardMarkup()
    ikb.add(types.InlineKeyboardButton("العربية 🇸🇦", callback_data="l_ar"),
            types.InlineKeyboardButton("English 🇺🇸", callback_data="l_en"))
    bot.send_message(uid, "Choose Language / اختر اللغة:", reply_markup=ikb)

@bot.callback_query_handler(func=lambda call: call.data.startswith('l_'))
def set_l(call):
    lang = call.data.split('_')[1]
    update_db("UPDATE users SET lang = ? WHERE user_id = ?", (lang, str(call.message.chat.id)))
    msg = "تم تفعيل اللغة العربية 🇸🇦" if lang == 'ar' else "English Language Activated 🇺🇸"
    bot.send_message(call.message.chat.id, msg, reply_markup=main_kb(lang))

@bot.message_handler(func=lambda m: True)
def engine(m):
    u = get_user(str(m.chat.id))
    if not u or u[6] == 'none': return
    uid, lang, txt = str(m.chat.id), u[6], m.text

    if txt in ["🔙 العودة للقائمة الرئيسية", "🔙 Back to Main Menu"]:
        bot.send_message(uid, "🏠 القائمة الرئيسية" if lang == 'ar' else "Main Menu", reply_markup=main_kb(lang))

    elif txt in ["💰 اكسب المال", "💰 Earn Money"]:
        update_db("UPDATE users SET last_task_time = ? WHERE user_id = ?", (time.time(), uid))
        task_id = u[3] + 1
        link = LINKS[u[3] % len(LINKS)]
        if lang == 'ar':
            msg = f"لإتمام المهمة {task_id} يرجى زيارة الرابط و البقاء فيه لمدة 25 ثانية لكسب 0.1$ 💸🎯."
            b1, b2 = "إضغط هنا لكسب 0.1$", "➡️ المهمة التالية"
        else:
            msg = f"To complete task {task_id}, please visit the link and stay for 25 seconds to earn 0.1$ 💸🎯."
            b1, b2 = "Click here to earn 0.1$", "➡️ Next Task"
        
        ikb = types.InlineKeyboardMarkup(row_width=1)
        ikb.add(types.InlineKeyboardButton(b1, url=link), types.InlineKeyboardButton(b2, callback_data="check_t"))
        bot.send_message(uid, msg, reply_markup=ikb)

    elif txt in ["👤 الملف الشخصي", "👤 Profile"]:
        if lang == 'ar':
            msg = f"ملفك الشخصي 🧔\n\nالاسم : {u[1]}\nالرصيد 💵 : {u[2]:.2f} USD\nعدد المهام المنفذة : {u[3]}\nالأصدقاء المدعوون: {u[4]}"
        else:
            msg = f"Your Profile 🧔\n\nName: {u[1]}\nBalance 💵: {u[2]:.2f} USD\nCompleted Tasks: {u[3]}\nInvited Friends: {u[4]}"
        bot.send_message(uid, msg)

    elif txt in ["👥 دعوة الأصدقاء", "👥 Invite Friends"]:
        link = f"https://t.me/Paynens_Bot?start={uid}"
        if lang == 'ar':
            msg = f"احصل على مكافآت بدعوة أصدقائك 👨‍👩‍👧‍👦🎁\nأرسل رابطًا إلى الأصدقاء 🖇📩\n{link}\n\nلكل صديق تمت دعوته ستربح أنت 0.5$ 💸🎊\n\nلقد دعوت: {u[4]} شخصًا 👤."
        else:
            msg = f"Get rewards by inviting your friends 👨‍👩‍👧‍👦🎁\nSend link to friends 🖇📩\n{link}\n\nFor each friend invited, you will earn 0.5$ 💸🎊\n\nYou invited: {u[4]} people 👤."
        bot.send_message(uid, msg)

    elif txt in ["📽 لإعلاناتكم", "📽 Advertise"]:
        if lang == 'ar':
            msg = ("هل لديك صفحة أو أي نشاط على منصات التواصل الإجتماعي لكن ليس لديك متابعين؟ \n \n"
                   "أنت فالمكان الصحيح 📢\n🤖 لأن بوت Paynens سيوفر لك متابعين حقيقيين و مشاهدات و زيارات حقيقية و ذالك من طريقة عملنا 👷🏻‍♂️: \n"
                   "لدينا أكثر من 67 ألف شخص حول العالم يربحون مبالغ مالية يوميا فقط من مشاهداتهم للإعلانات و الإشتراك في صفحات المعلنين 🌏💸\n"
                   "هل تعلم أن 67 ألف شخص يمكن لهم مشاهدة إعلانك و الإشتراك في منصتك؟ \n"
                   "لا تتردد فالإنضمام الى فريق المعلنين لدينا و كن واحد منهم 🎯😊. \n\n"
                   "عروضنا للزيارات و المشاهدات: \n"
                   "🎯 ألف زيارة / مشاهدة = 2.5$ 🔎💸\n"
                   "🎯 5 ألاف زيارة / مشاهدة = 5$ 🔎💸\n"
                   "🎯 10 ألاف زيارة / مشاهدة = 7.5$ 🔎💸\n"
                   "🎯 20 ألف زيارة / مشاهدة = 12$ 🔎💸\n"
                   "🎯 40 ألف زيارة / مشاهدة = 20$ 🔎💸\n"
                   "🎯 60 ألف زيارة / مشاهدة = 35$ 🔎💸\n\n"
                   "📍لا تتردد فالتواصل مع الأدمن لطلب العرض اللذي تريد..! \nللتواصل مع الأدمن: @i5pyc")
        else:
            msg = ("Do you have a page or any activity on social media platforms but don't have followers?\n\n"
                   "You are in the right place 📢\n🤖 Because the Paynens bot will provide you with real followers, views, and visits through our working method 👷🏻‍♂️:\n"
                   "We have more than 67,000 people around the world who earn money daily just by watching ads and subscribing to advertisers' pages 🌏💸\n"
                   "Did you know that 67,000 people can watch your ad and subscribe to your platform?\n"
                   "Don't hesitate to join our advertising team and be one of them 🎯😊.\n\n"
                   "Our offers for visits and views:\n"
                   "🎯 1,000 visits/views = 2.5$ 🔎💸\n"
                   "🎯 5,000 visits/views = 5$ 🔎💸\n"
                   "🎯 10,000 visits/views = 7.5$ 🔎💸\n"
                   "🎯 20,000 visits/views = 12$ 🔎💸\n"
                   "🎯 40,000 visits/views = 20$ 🔎💸\n"
                   "🎯 60,000 visits/views = 35$ 🔎💸\n\n"
                   "📍 Don't hesitate to contact the admin to request the offer you want..!\nContact Admin: @i5pyc")
        bot.send_message(uid, msg, reply_markup=back_kb(lang))

    elif txt in ["📊 الإحصائيات", "📊 Statistics"]:
        if lang == 'ar':
            msg = "إحصائيات البوت 📊\n\nالمستخدمون في البوت 👥: 67586\nالمبلغ المكتسب من قبل المستخدمين 💰: 278036 USD\nالعدد الإجمالي للزيارات و المشاهدات 🎯 : 7.442.654"
        else:
            msg = "Bot Statistics 📊\n\nUsers in Bot 👥: 67586\nTotal Earned by Users 💰: 278036 USD\nTotal Visits and Views 🎯: 7,442,654"
        bot.send_message(uid, msg)

    elif txt in ["🏦 سحب الأرباح", "🏦 Withdraw Profits"]:
        if lang == 'ar':
            msg_pay = f"💰 الرصيد: {u[2]:.2f} USD\n\nاختر طريقة الدفع ⬇️"
        else:
            msg_pay = f"💰 Balance: {u[2]:.2f} USD\n\nChoose payment method ⬇️"
        ikb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("USDT", callback_data="w_u"))
        bot.send_message(uid, msg_pay, reply_markup=ikb)

@bot.callback_query_handler(func=lambda call: call.data == "check_t")
def check_t(call):
    uid = str(call.message.chat.id); u = get_user(uid)
    if time.time() - u[5] >= 25:
        update_db("UPDATE users SET balance = balance + 0.1, tasks_count = tasks_count + 1 WHERE user_id = ?", (uid,))
        bot.answer_callback_query(call.id, "✅ +0.1$")
        u = get_user(uid)
        task_id = u[3] + 1
        link = LINKS[u[3] % len(LINKS)]
        if u[6] == 'ar':
            msg = f"لإتمام المهمة {task_id} يرجى زيارة الرابط و البقاء فيه لمدة 25 ثانية لكسب 0.1$ 💸🎯."
            b1, b2 = "إضغط هنا لكسب 0.1$", "➡️ المهمة التالية"
        else:
            msg = f"To complete task {task_id}, please visit the link and stay for 25 seconds to earn 0.1$ 💸🎯."
            b1, b2 = "Click here to earn 0.1$", "➡️ Next Task"
        ikb = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(b1, url=link), types.InlineKeyboardButton(b2, callback_data="check_t"))
        bot.send_message(uid, msg, reply_markup=ikb)
    else:
        err = "لم تكتمل المهمة الاولى 🚩❌" if u[6]=='ar' else "Task not completed yet 🚩❌"
        bot.answer_callback_query(call.id, err, show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "w_u")
def w_u(call):
    u = get_user(str(call.message.chat.id))
    if u[2] < 10.0: 
        err_msg = "الحد الأدنى للسحب هو 10$" if u[6]=='ar' else "Minimum withdrawal is 10$"
        bot.answer_callback_query(call.id, err_msg, show_alert=True)
    else:
        prompt = "يرجى إدخال عنوان محفظتك 💸💰." if u[6]=='ar' else "Please enter your wallet address 💸💰."
        m = bot.send_message(call.message.chat.id, prompt)
        bot.register_next_step_handler(m, process_final_withdrawal, u[6])

def process_final_withdrawal(m, lang):
    admin_bot.send_message(MY_ID, f"Withdraw Request!\nUID: {m.chat.id}\nWallet: {m.text}")
    confirm = "لقد تلقينا طلبك ستصل لك أموالك في غضون 24 ساعة بعدها مراجعة الطلب ⏳💸." if lang=='ar' else "We have received your request, your money will arrive within 24 hours after reviewing the request ⏳💸."
    bot.send_message(m.chat.id, confirm)

bot.polling(none_stop=True)
bot.infinity_polling(timeout=10, long_polling_timeout=5)
