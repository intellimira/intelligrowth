# core_sentry.py  —  The Reusable Modular Frame
# Cluster: LOCAL_SENTRY
# Status: S-RANK SEALED

import os
import sqlite3
import imaplib
import email
import time

class LocalSentry:
    def __init__(self, project_name, db_path="sentry_log.db"):
        self.project_name = project_name
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the immutable local audit log."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT,
                data TEXT,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def log_event(self, event_type, data, status="PROCESSED"):
        """Record an event in the local mesh."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO audit_log (event_type, data, status) VALUES (?, ?, ?)', 
                       (event_type, str(data), status))
        conn.commit()
        conn.close()
        print(f" [SENTRY] Event Logged: {event_type} - {status}")

    def listen_imap(self, host, user, password, folder="INBOX", search_criteria="UNSEEN"):
        """Generic IMAP listener for data-triggers."""
        print(f" [SENTRY] Listening for triggers on {host}...")
        try:
            mail = imaplib.IMAP4_SSL(host)
            mail.login(user, password)
            mail.select(folder)
            
            result, data = mail.search(None, search_criteria)
            ids = data[0].split()
            
            for msg_id in ids:
                result, msg_data = mail.fetch(msg_id, '(RFC822)')
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                subject = msg['Subject']
                sender = msg['From']
                
                # Logic for trigger detection (e.g., 'Delete' or 'Compliance')
                self.log_event("EMAIL_TRIGGER", {"subject": subject, "from": sender})
                
            mail.logout()
        except Exception as e:
            print(f" [Error] IMAP Listen failed: {e}")

    def run_check(self, check_func, interval=3600):
        """Infinite loop for periodic sentry checks."""
        print(f" [SENTRY] Heartbeat active for {self.project_name}. Interval: {interval}s")
        while True:
            try:
                check_func()
                time.sleep(interval)
            except KeyboardInterrupt:
                break
