# 🤖 Heider - بوت تيليجرام متقدم

بوت تيليجرام متقدم مكتوب بـ Python مع نظام صلاحيات وقاعدة بيانات.

## ✨ المميزات

- ✅ نظام **Polling** (يعمل على Termux بدون Webhooks)
- ✅ قاعدة بيانات **SQLite** لحفظ البيانات
- ✅ نظام صلاحيات **Admin/User**
- ✅ أوامر متقدمة وسهلة الاستخدام
- ✅ معالجة الأخطاء المتقدمة
- ✅ رسائل مخصصة وديناميكية

---

## 📋 الأوامر

### 🔹 أوامر عامة:
```
/start      - ابدأ معي
/help       - عرض الأوامر
/info       - معلومات حسابك
/ping       - اختبر الاتصال
/stats      - إحصائيات البوت
```

### 🔴 أوامر المسؤول:
```
/users              - عدد المستخدمين
/broadcast [نص]    - إرسال رسالة لجميع المستخدمين
/ban [معرف]        - حظر مستخدم
/unban [معرف]      - إلغاء حظر
/cleardb            - مسح قاعدة البيانات
```

---

## 🚀 التثبيت على Termux

### 1️⃣ تثبيت المتطلبات:
```bash
apt update && apt upgrade
apt install python3 python3-pip git
```

### 2️⃣ استنساخ المستودع:
```bash
git clone https://github.com/hjak9p-alt/heider.git
cd heider
```

### 3️⃣ تثبيت المكتبات:
```bash
pip install -r requirements.txt
```

### 4️⃣ إعداد التوكن:
```bash
nano config.py
```
غير `YOUR_BOT_TOKEN_HERE` برقم التوكن الخاص بك

**أو** استخدم ملف `.env`:
```bash
cp .env.example .env
nano .env
```

### 5️⃣ تشغيل البوت:
```bash
python3 bot.py
```

---

## 🔧 إعداد التوكن

1. افتح Telegram واذهب إلى [@BotFather](https://t.me/BotFather)
2. أرسل `/newbot`
3. اتبع التعليمات وحصل على التوكن
4. ضع التوكن في `config.py` أو ملف `.env`

---

## 📁 هيكل المشروع

```
heider/
├── bot.py           - ملف البوت الرئيسي
├── config.py        - إعدادات البوت
├── database.py      - قاعدة البيانات
├── requirements.txt - المكتبات المطلو��ة
├── .env.example     - مثال لملف الإعدادات
└── README.md        - هذا الملف
```

---

## 💾 قاعدة البيانات

تُحفظ البيانات في ملف `bot_database.db` بـ SQLite:

### جداول:
- **users**: بيانات المستخدمين (ID, Username, اسم، حالة الحظر)
- **stats**: إحصائيات الاستخدام

---

## 🛠️ التطوير

### إضافة أوامر جديدة:

أضف دالة جديدة في `bot.py`:

```python
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("رسالة مخصصة")

# في main():
app.add_handler(CommandHandler("mycommand", my_command))
```

---

## ⚙️ المتطلبات

- Python 3.7+
- python-telegram-bot 20.3+
- sqlite3 (مدمج مع Python)

---

## 📞 الدعم

إذا واجهت مشكلة:

1. تحقق من أن البوت مفعّل عند @BotFather
2. تحقق من التوكن صحيح
3. تأكد من اتصالك بالإنترنت
4. جرّب إعادة تشغيل البوت

---

## 📄 الترخيص

هذا المشروع مفتوح المصدر ومتاح للاستخدام الحر.

---

**صنع بـ ❤️ بواسطة Heider Bot**
