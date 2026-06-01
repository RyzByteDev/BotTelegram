from telegram.ext import Application, MessageHandler, filters, CommandHandler
import database, handlers, config

def main():
    database.init()
    app = Application.builder().token(config.TOKEN).build()
    
    app.add_handler(CommandHandler("start", handlers.handle_msg))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL, handlers.handle_msg))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__': main()
