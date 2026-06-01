import secrets, datetime
from telegram import ReplyKeyboardMarkup
from database import run
import admin

def get_main_keyboard():
    return ReplyKeyboardMarkup([["📤 Up File", "📥 Get File"], ["📊 Stats"]], resize_keyboard=True)

user_states = {}
user_queues = {}

async def handle_msg(u, c):
    uid = u.effective_user.id
    txt = u.message.text or ""
    
    if txt == "/start":
        await u.message.reply_text("💀 *SYSTEM ONLINE*", reply_markup=get_main_keyboard(), parse_mode="Markdown")
        user_states[uid] = None
        
    elif txt == "📊 Stats":
        await u.message.reply_text(admin.get_stats(), parse_mode="Markdown")

    elif txt == "📤 Up File":
        user_states[uid] = 'upload'
        user_queues[uid] = []
        await u.message.reply_text("📥 *UPLOAD MODE*\nKirim file, ketik /done jika selesai.")
        
    elif txt == "📥 Get File":
        user_states[uid] = 'get'
        await u.message.reply_text("📥 *GET MODE*\nMasukkan KODE.")

    elif user_states.get(uid) == 'upload':
        if txt == "/done":
            kode = secrets.token_hex(2).upper()
            now = datetime.datetime.now()
            for fid in user_queues.get(uid, []):
                run("INSERT INTO files VALUES (?, ?, ?, ?)", (kode, fid, uid, now))
            await u.message.reply_text(f"🚀 *UPLOADED*\nKode: `CyberCoreN8Bot:{kode}`", reply_markup=get_main_keyboard(), parse_mode="Markdown")
            user_queues[uid] = []
            user_states[uid] = None
        elif u.message.photo or u.message.video or u.message.document:
            fid = u.message.photo[-1].file_id if u.message.photo else (u.message.video.file_id if u.message.video else u.message.document.file_id)
            user_queues[uid].append(fid)

    elif user_states.get(uid) == 'get' or (txt and ":" in txt):
        kode = txt.split(":")[1].upper() if ":" in txt else txt.upper()
        rows = run("SELECT file_id FROM files WHERE kode = ?", (kode,))
        if rows:
            for r in rows: await u.message.reply_photo(r[0])
            await u.message.reply_text("✅ *Selesai.*", reply_markup=get_main_keyboard())
        else:
            await u.message.reply_text("❌ *INVALID CODE*", reply_markup=get_main_keyboard())
