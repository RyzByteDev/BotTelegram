from database import run

def get_stats():
    count = run("SELECT COUNT(*) FROM files")[0][0]
    return f"📊 *STATISTIK BOT*\nTotal File: {count}"

def get_all_users():
    return run("SELECT DISTINCT uploader_id FROM files")
