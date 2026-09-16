# Telegram Bot Configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Bot Token (احصل عليه من @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Admin IDs (ضع معرفك هنا)
ADMIN_IDS = [123456789]  # غير هذا برقم معرفك

# Database
DATABASE_FILE = "bot_database.db"

# Port للـ Webhook (لا تحتاجه على Termux - استخدم Polling)
WEBHOOK_PORT = 8443
