#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, ADMIN_IDS
from database import Database
import asyncio

# إعداد Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# إنشاء كائن قاعدة البيانات
db = Database()

# ==================== معالجات الأوامر ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /start"""
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    
    welcome_text = f"""
🤖 أهلاً بك {user.first_name}! 👋

أنا بوت متقدم هنا لمساعدتك!

استخدم /help لمعرفة الأوامر المتاحة
    """
    await update.message.reply_text(welcome_text)
    logger.info(f"User {user.id} started the bot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /help"""
    user_id = update.effective_user.id
    
    help_text = """
📚 **الأوامر المتاحة:**

🔹 **الأوامر العامة:**
/start - ابدأ معي
/help - عرض هذه الرسالة
/info - معلومات عنك
/ping - اختبر الاتصال
/stats - إحصائيات البوت
    """
    
    if user_id in ADMIN_IDS:
        help_text += """

🔴 **أوامر المسؤول:**
/users - عدد المستخدمين
/broadcast [النص] - إرسال رسالة لجميع المستخدمين
/ban [معرف] - حظر مستخدم
/unban [معرف] - إلغاء حظر
/cleardb - مسح قاعدة البيانات
        """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /info"""
    user = update.effective_user
    
    info_text = f"""
👤 **معلومات حسابك:**

🆔 معرفك: `{user.id}`
📝 اسمك: {user.first_name} {user.last_name or ''}
👤 اسم المستخدم: @{user.username or 'لا يوجد'}
    """
    await update.message.reply_text(info_text, parse_mode='Markdown')

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /ping"""
    await update.message.reply_text("🟢 البوت يعمل بشكل طبيعي! ✅")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /stats"""
    user_count = db.get_user_count()
    
    stats_text = f"""
📊 **إحصائيات البوت:**

👥 عدد المستخدمين: {user_count}
⚙️ الإصدار: 1.0
🔧 الحالة: نشط ✅
    """
    await update.message.reply_text(stats_text, parse_mode='Markdown')

# ==================== أوامر الـ Admin ====================

async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /users - للمسؤول فقط"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ هذا الأمر للمسؤول فقط!")
        return
    
    count = db.get_user_count()
    await update.message.reply_text(f"👥 عدد المستخدمين: {count}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /broadcast - للمسؤول فقط"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ هذا الأمر للمسؤول فقط!")
        return
    
    if not context.args:
        await update.message.reply_text("استخدام: /broadcast [النص]")
        return
    
    message = ' '.join(context.args)
    users = db.get_all_users()
    
    await update.message.reply_text(f"📢 جاري إرسال الرسالة إلى {len(users)} مستخدم...")
    
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=message)
        except Exception as e:
            logger.error(f"Failed to send message to {uid}: {e}")
    
    await update.message.reply_text(f"✅ تم إرسال الرسالة إلى {len(users)} مستخدم")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /ban - للمسؤول فقط"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ هذا الأمر للمسؤول فقط!")
        return
    
    if not context.args:
        await update.message.reply_text("استخدام: /ban [معرف]")
        return
    
    try:
        target_id = int(context.args[0])
        db.ban_user(target_id)
        await update.message.reply_text(f"🚫 تم حظر المستخدم {target_id}")
    except ValueError:
        await update.message.reply_text("❌ معرف غير صحيح!")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /unban - للمسؤول فقط"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ هذا الأمر للمسؤول فقط!")
        return
    
    if not context.args:
        await update.message.reply_text("استخدام: /unban [معرف]")
        return
    
    try:
        target_id = int(context.args[0])
        db.unban_user(target_id)
        await update.message.reply_text(f"✅ تم إلغاء حظر المستخدم {target_id}")
    except ValueError:
        await update.message.reply_text("❌ معرف غير صحيح!")

async def cleardb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /cleardb - للمسؤول فقط"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ هذا الأمر للمسؤول فقط!")
        return
    
    db.clear_db()
    await update.message.reply_text("🗑️ تم مسح قاعدة البيانات بنجاح!")

# ==================== معالج الرسائل ====================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج الرسائل العامة"""
    user_id = update.effective_user.id
    
    # التحقق من الحظر
    if db.is_banned(user_id):
        await update.message.reply_text("❌ أنت محظور من استخدام هذا البوت!")
        return
    
    # رد عام على الرسائل
    await update.message.reply_text("👋 مرحباً! استخدم /help لمعرفة الأوامر المتاحة")

# ==================== الدالة الرئيسية ====================

def main():
    """دالة البدء الرئيسية"""
    logger.info("🤖 بدء البوت...")
    
    # إنشاء التطبيق
    app = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة معالجات الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("stats", stats))
    
    # أوامر الـ Admin
    app.add_handler(CommandHandler("users", users_command))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("unban", unban_user))
    app.add_handler(CommandHandler("cleardb", cleardb))
    
    # معالج الرسائل العامة
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # بدء البوت
    logger.info("✅ البوت جاهز!")
    logger.info("استخدم Ctrl+C لإيقاف البوت")
    
    try:
        app.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف البوت")

if __name__ == '__main__':
    main()
