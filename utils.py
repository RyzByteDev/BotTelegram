from telegram import ReplyKeyboardMarkup
import time

last_msg = {}

def get_main_keyboard(is_admin=False):
    kb = [["📤 Up File", "📥 Get File"], ["📊 Stats"]]
    if is_admin: 
        kb.append(["📢 Broadcast", "🚫 Ban User"])
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def is_spam(uid):
    if time.time() - last_msg.get(uid, 0) < 1.5: return True
    last_msg[uid] = time.time()
    return False
