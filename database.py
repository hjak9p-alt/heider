import sqlite3
from config import DATABASE_FILE
from datetime import datetime

class Database:
    def __init__(self):
        self.db_file = DATABASE_FILE
        self.init_db()
    
    def init_db(self):
        """إنشاء جداول قاعدة البيانات"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                joined_date TIMESTAMP,
                is_banned INTEGER DEFAULT 0
            )
        ''')
        
        # جدول الإحصائيات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                command TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id, username, first_name, last_name):
        """إضافة مستخدم جديد"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO users 
            (user_id, username, first_name, last_name, joined_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_user_count(self):
        """الحصول على عدد المستخدمين"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_banned = 0')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def ban_user(self, user_id):
        """حظر مستخدم"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
    
    def unban_user(self, user_id):
        """إلغاء حظر مستخدم"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET is_banned = 0 WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
    
    def is_banned(self, user_id):
        """التحقق من حظر المستخدم"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT is_banned FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0
    
    def get_all_users(self):
        """الحصول على جميع المستخدمين"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE is_banned = 0')
        users = cursor.fetchall()
        conn.close()
        return [user[0] for user in users]
    
    def clear_db(self):
        """مسح قاعدة البيانات"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users')
        cursor.execute('DELETE FROM stats')
        conn.commit()
        conn.close()
