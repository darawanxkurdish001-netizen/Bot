import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

JSON_FILE = 'KorekTelecomSample.json'

def search_json(query):
    if not os.path.exists(JSON_FILE):
        return None
    
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    results = []
    query_str = str(query).strip().lower()
    
    for item in data:
        for key, value in item.items():
            if value and query_str in str(value).lower():
                results.append(item)
                break
        if len(results) >= 5:
            break
            
    return results

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("بەخێربێیت! فەرمانی /search لەگەڵ ناوانێک یان ژمارەیەک بنووسە.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = " ".join(context.args)
    if not user_query:
        await update.message.reply_text("تکایە دەقێک یان ژمارەیەک بنووسە.")
        return
        
    results = search_json(user_query)
    
    if results is None:
        await update.message.reply_text("فایلی داتابەیسەکە نادۆزرایەوە.")
    elif results:
        msg = "ئەنجامەکان:\n\n"
        for item in results:
            name = item.get("Subscriber Name", "نەنوسراوە")
            gsm = item.get("GSM Number", "نەنوسراوە")
            city = item.get("City", "نەنوسراوە")
            msg += f"👤 ناو: {name}\n📞 ژمارە: {gsm}\n🏙 شار: {city}\n-------------------\n"
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("هیچ زانیارییەک نەدۆزرایەوە.")

TOKEN = "8010547862:AAEHFUKVaC4pQWCWrfd9bRZ3nroQ8SN8Bt0"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))

if __name__ == '__main__':
    print("بۆتەکە چالاک بوو...")
    app.run_polling()
