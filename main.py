import sqlite3
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ناوی فایلی داتابەیسەکەت بە وردی بنووسە
DB_FILE = 'Korek Telecom Sam ple.json'

def search_db(query):
    if not os.path.exists(DB_FILE):
        return []
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # دۆزینەوەی ناوی یەکەم خشتە لە داتابەیسەکەدا
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not tables:
        return []
    
    table_name = tables[0][0]
    
    # گەڕان لەناو تەواوی خشتەکەدا
    cursor.execute(f"SELECT * FROM {table_name} WHERE CAST(rowid AS TEXT) LIKE ? OR 1=1 LIMIT 5", ())
    # تێبینی: بۆ گەڕانی وردتر دەتوانیت دواتر ناوی ستوونەکە ڕاست بکەیتەوە
    
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
    results = cursor.fetchall()
    conn.close()
    return results

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("بەخێربێیت! فەرمانی /search لەگەڵ وشەی گەڕان بنووسە.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = " ".join(context.args)
    if not user_query:
        await update.message.reply_text("تکایە دەقێک یان ژمارەیەک بنووسە بۆ گەڕان.")
        return

    data = search_db(user_query)
    if data:
        msg = "ئەنجامەکان:\n\n"
        for row in data:
            msg += f"{row}\n"
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("هیچ زانیارییەک نەدۆزرایەوە.")

# توکنەکەی BotFather لێرە دابنێ
TOKEN = "توکنەکەی_خۆت_لێرە_دابنێ"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))

if __name__ == '__main__':
    app.run_polling()
