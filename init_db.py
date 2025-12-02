import sqlite3
import os

def init_db():
    if os.path.exists('my_portal.db'):
        os.remove('my_portal.db')
        
    conn = sqlite3.connect('my_portal.db')
    c = conn.cursor()
    
    # Student table
    c.execute('''CREATE TABLE IF NOT EXISTS student (
        id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        middle_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        date_of_birth TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email_verified INTEGER DEFAULT 0,
        profile_avatar TEXT,
        gender TEXT DEFAULT 'male'
    )''')

    # Teacher table
    c.execute('''CREATE TABLE IF NOT EXISTS teacher (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        date_of_birth TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email_verified INTEGER DEFAULT 0,
        profile_avatar TEXT,
        gender TEXT DEFAULT 'male'
    )''')
    
    # Subject table
    c.execute('''CREATE TABLE IF NOT EXISTS subject (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT UNIQUE NOT NULL,
        created_date TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    # Teacher Subject
    c.execute('''CREATE TABLE IF NOT EXISTS teacher_sub (
        primary_teacher INTEGER DEFAULT 0,
        teacher_id INTEGER NOT NULL,
        sub_id INTEGER NOT NULL,
        PRIMARY KEY (teacher_id, sub_id),
        FOREIGN KEY (teacher_id) REFERENCES teacher(id),
        FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
    )''')

    # Student Subject
    c.execute('''CREATE TABLE IF NOT EXISTS student_sub (
        student_id TEXT NOT NULL,
        sub_id INTEGER NOT NULL,
        PRIMARY KEY (student_id, sub_id),
        FOREIGN KEY (student_id) REFERENCES student(id),
        FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
    )''')

    # Book
    c.execute('''CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link TEXT NOT NULL,
        sub_id INTEGER NOT NULL,
        FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
    )''')

    # Lecture
    c.execute('''CREATE TABLE IF NOT EXISTS lecture (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        notes TEXT,
        sub_id INTEGER NOT NULL,
        FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
    )''')

    # Video
    c.execute('''CREATE TABLE IF NOT EXISTS video (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link TEXT NOT NULL,
        lec_id INTEGER NOT NULL,
        sub_id INTEGER NOT NULL,
        FOREIGN KEY (lec_id) REFERENCES lecture(id) ON DELETE CASCADE,
        FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
    )''')

    # PDFs
    c.execute('''CREATE TABLE IF NOT EXISTS pdfs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link TEXT NOT NULL,
        lec_id INTEGER NOT NULL,
        sub_id INTEGER NOT NULL,
        FOREIGN KEY (lec_id) REFERENCES lecture(id) ON DELETE CASCADE,
        FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
    )''')

    # Sheets
    c.execute('''CREATE TABLE IF NOT EXISTS sheets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_link TEXT NOT NULL,
        submit_link TEXT NOT NULL,
        lec_id INTEGER NOT NULL,
        sub_id INTEGER NOT NULL,
        FOREIGN KEY (lec_id) REFERENCES lecture(id) ON DELETE CASCADE,
        FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
    )''')

    # Grade
    c.execute('''CREATE TABLE IF NOT EXISTS grade (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grade INTEGER DEFAULT 0,
        student_id TEXT NOT NULL,
        sub_id INTEGER NOT NULL,
        FOREIGN KEY (student_id) REFERENCES student(id),
        FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
    )''')

    # Quiz
    c.execute('''CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        start_time TIMESTAMP NOT NULL,
        duration INTEGER NOT NULL,
        link TEXT,
        sub_id INTEGER NOT NULL,
        FOREIGN KEY (sub_id) REFERENCES subject(id)
    )''')

    # Subject Ann Chat
    c.execute('''CREATE TABLE IF NOT EXISTS subject_ann_chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT NOT NULL,
        message_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        teacher_id INTEGER NOT NULL,
        sub_id INTEGER NOT NULL,
        FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE,
        FOREIGN KEY (teacher_id) REFERENCES teacher(id)
    )''')

    # Chat Messages
    c.execute('''CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sub_id INTEGER,
        user_id INTEGER,
        role TEXT,
        message TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
    )''')
    
    conn.commit()
    conn.close()
    print("Database initialized (v2).")

if __name__ == '__main__':
    init_db()