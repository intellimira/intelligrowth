#!/usr/bin/env python3
"""
Thunderbird Email Indexer
Indexes and searches Thunderbird local email cache
"""

import argparse
import email
import mailbox
import os
import re
import sqlite3
import sys
from datetime import datetime
from email.header import decode_header
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Optional

THUNDERBIRD_PROFILE = (
    "/home/sir-v/snap/thunderbird/common/.thunderbird/s72xlcuu.default"
)
DB_PATH = Path.home() / ".local" / "share" / "thunderbird-indexer" / "emails.db"

ACCOUNTS = {
    "intellimira@gmail.com": "ImapMail/imap.gmail.com",
    "randolphdube@gmail.com": "ImapMail/imap.gmail-1.com",
}


def get_account_paths():
    base = Path(THUNDERBIRD_PROFILE)
    return {email: base / path for email, path in ACCOUNTS.items()}


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY,
        message_id TEXT UNIQUE,
        account TEXT,
        folder TEXT,
        subject TEXT,
        sender TEXT,
        sender_email TEXT,
        recipients TEXT,
        date TEXT,
        timestamp INTEGER,
        has_attachments INTEGER,
        snippet TEXT,
        body_text TEXT
    )""")

    c.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS emails_fts USING fts5(
        subject, sender_email, body_text,
        content='emails',
        content_rowid='id'
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS attachments (
        id INTEGER PRIMARY KEY,
        email_id INTEGER,
        filename TEXT,
        content_type TEXT,
        size INTEGER,
        FOREIGN KEY(email_id) REFERENCES emails(id)
    )""")

    c.execute("CREATE INDEX IF NOT EXISTS idx_sender ON emails(sender_email)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_date ON emails(date)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_folder ON emails(folder)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_account ON emails(account)")

    conn.commit()
    return conn


def decode_email_header(header):
    if not header:
        return ""
    decoded = decode_header(header)
    result = ""
    for part, encoding in decoded:
        if isinstance(part, bytes):
            result += part.decode(encoding or "utf-8", errors="ignore")
        else:
            result += part
    return result


def extract_email(msg, account, folder):
    try:
        message_id = msg.get("Message-ID", "")
        if not message_id:
            subject = decode_email_header(msg.get("Subject", ""))
            date_str = msg.get("Date", "")
            message_id = f"{account}:{folder}:{subject[:30]}:{date_str[:20]}"

        subject = decode_email_header(msg.get("Subject", ""))
        date_str = msg.get("Date", "")
        sender = decode_email_header(msg.get("From", ""))
        recipients = decode_email_header(msg.get("To", ""))

        sender_email = ""
        match = re.search(r"<(.+?)>", sender)
        if match:
            sender_email = match.group(1)
        else:
            match = re.search(r"\S+@\S+", sender)
            if match:
                sender_email = match.group()

        try:
            timestamp = int(parsedate_to_datetime(date_str).timestamp())
        except:
            timestamp = 0

        body_text = ""
        snippet = ""
        has_attachments = 0

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        body = part.get_payload(decode=True)
                        if body:
                            body_text = body.decode("utf-8", errors="ignore")
                            snippet = body_text[:200].replace("\n", " ")
                    except:
                        pass
                if part.get_filename():
                    has_attachments = 1
        else:
            try:
                body = msg.get_payload(decode=True)
                if body:
                    body_text = body.decode("utf-8", errors="ignore")
                    snippet = body_text[:200].replace("\n", " ")
            except:
                pass

        return {
            "message_id": message_id,
            "account": account,
            "folder": folder,
            "subject": subject,
            "sender": sender,
            "sender_email": sender_email,
            "recipients": recipients,
            "date": date_str,
            "timestamp": timestamp,
            "has_attachments": has_attachments,
            "snippet": snippet,
            "body_text": body_text[:10000],
        }
    except Exception as e:
        return None


def index_mbox(mbox_path, account, folder, conn):
    c = conn.cursor()
    indexed = 0

    if not mbox_path.exists():
        print(f"  [SKIP] {folder}: mbox not found")
        return 0

    try:
        mbox = mailbox.mbox(mbox_path)
    except:
        try:
            mbox = mailbox.Maildir(str(mbox_path), factory=None)
        except Exception as e:
            print(f"  [ERROR] {folder}: {e}")
            return 0

    total = len(mbox)
    print(f"  Processing {total} emails from {folder}...")

    for key, msg in mbox.items():
        try:
            email_data = extract_email(msg, account, folder)
            if not email_data:
                continue

            c.execute(
                """INSERT OR REPLACE INTO emails 
                (message_id, account, folder, subject, sender, sender_email, 
                 recipients, date, timestamp, has_attachments, snippet, body_text)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    email_data["message_id"],
                    email_data["account"],
                    email_data["folder"],
                    email_data["subject"],
                    email_data["sender"],
                    email_data["sender_email"],
                    email_data["recipients"],
                    email_data["date"],
                    email_data["timestamp"],
                    email_data["has_attachments"],
                    email_data["snippet"],
                    email_data["body_text"],
                ),
            )

            email_id = c.lastrowid

            if msg.is_multipart():
                for part in msg.walk():
                    filename = part.get_filename()
                    if filename:
                        filename = decode_email_header(filename)
                        c.execute(
                            "INSERT INTO attachments (email_id, filename, content_type, size) VALUES (?, ?, ?, ?)",
                            (
                                email_id,
                                filename,
                                part.get_content_type(),
                                len(part.get_payload(decode=True) or b""),
                            ),
                        )

            indexed += 1
            if indexed % 100 == 0:
                conn.commit()
                print(f"    Indexed {indexed}/{total}...")

        except Exception as e:
            continue

    conn.commit()
    print(f"  [DONE] Indexed {indexed} emails from {folder}")
    return indexed


def rebuild_fts(conn):
    c = conn.cursor()
    print("Rebuilding full-text search index...")
    try:
        c.execute("DELETE FROM emails_fts")
        c.execute("""INSERT INTO emails_fts(rowid, subject, sender_email, body_text)
            SELECT id, subject, sender_email, body_text FROM emails""")
        conn.commit()
        print("[DONE] FTS index rebuilt")
    except Exception as e:
        print(f"[WARN] FTS rebuild failed: {e}")
        print("       Full-text search will use LIKE queries instead")


def cmd_index(args, conn):
    paths = get_account_paths()
    total = 0

    c = conn.cursor()
    c.execute("DELETE FROM attachments")
    c.execute("DELETE FROM emails")
    conn.commit()

    for account, account_path in paths.items():
        print(f"\n📧 Indexing account: {account}")

        if not account_path.exists():
            print(f"  [SKIP] Account path not found: {account_path}")
            continue

        for root, dirs, files in os.walk(account_path):
            root_path = Path(root)

            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for f in files:
                if f.endswith(".sbd"):
                    folder_name = f.replace(".sbd", "")
                    if folder_name == "[Gmail]":
                        continue
                    mbox_path = root_path / f
                    count = index_mbox(mbox_path, account, folder_name, conn)
                    total += count
                elif f == "INBOX" or (
                    not f.endswith(".msf")
                    and not f.endswith(".dat")
                    and not f.startswith(".")
                ):
                    if f == "INBOX":
                        folder_name = "INBOX"
                    elif f in ["msgFilterRules.dat"]:
                        continue
                    else:
                        folder_name = f
                    mbox_path = root_path / f
                    count = index_mbox(mbox_path, account, folder_name, conn)
                    total += count
                elif f == "INBOX" or (
                    not f.endswith(".msf") and not f.endswith(".dat")
                ):
                    if f in ["INBOX", "msgFilterRules.dat"]:
                        folder_name = "INBOX" if f == "INBOX" else None
                    else:
                        folder_name = f
                    if folder_name:
                        mbox_path = root_path / f
                        count = index_mbox(mbox_path, account, folder_name, conn)
                        total += count

    rebuild_fts(conn)
    print(f"\n✅ Total indexed: {total} emails")


def cmd_search(args, conn):
    c = conn.cursor()
    query = args.query

    account_filter = ""
    params = [f"%{query}%", f"%{query}%", f"%{query}%"]

    if args.account and args.account != "all":
        account_filter = "AND account = ?"
        params.append(args.account)

    if args.sender:
        account_filter += " AND sender_email LIKE ?"
        params.append(f"%{args.sender}%")

    sql = f"""SELECT id, account, folder, subject, sender_email, date, has_attachments, snippet
        FROM emails
        WHERE (subject LIKE ? OR sender_email LIKE ? OR body_text LIKE ?)
        {account_filter}
        ORDER BY timestamp DESC
        LIMIT ?"""
    params.append(args.limit)

    c.execute(sql, params)
    results = c.fetchall()

    print(f"Found {len(results)} results:\n")
    for row in results:
        att = "📎" if row[6] else "  "
        print(f"{att} [{row[1][:15]}...] {row[2]}")
        print(f"   From: {row[4]}")
        print(f"   Subject: {row[3][:60]}")
        print(f"   Date: {row[5][:25]}")
        print()


def cmd_fts(args, conn):
    c = conn.cursor()
    query = args.query

    sql = """SELECT e.id, e.account, e.folder, e.subject, e.sender_email, e.date, e.has_attachments
        FROM emails e
        JOIN emails_fts ON e.id = emails_fts.rowid
        WHERE emails_fts MATCH ?
        ORDER BY rank
        LIMIT ?"""

    c.execute(sql, (query, args.limit))
    results = c.fetchall()

    print(f"Full-text search results ({len(results)}):\n")
    for row in results:
        att = "📎" if row[6] else "  "
        print(f"{att} [{row[1]}] {row[2]}: {row[3][:50]}")
        print(f"   From: {row[4]} | {row[5][:20]}")
        print()


def cmd_from(args, conn):
    c = conn.cursor()
    sender = args.sender

    sql = """SELECT id, account, folder, subject, date, has_attachments
        FROM emails
        WHERE sender_email LIKE ?
        ORDER BY timestamp DESC
        LIMIT ?"""

    c.execute(sql, (f"%{sender}%", args.limit))
    results = c.fetchall()

    print(f"Emails from '{sender}' ({len(results)}):\n")
    for row in results:
        att = "📎" if row[5] else "  "
        print(f"{att} [{row[1][:20]}...] {row[2]}: {row[3][:50]}")
        print(f"   Date: {row[4][:25]}")
        print()


def cmd_subject(args, conn):
    c = conn.cursor()
    subject = args.subject

    sql = """SELECT id, account, folder, sender_email, date, has_attachments
        FROM emails
        WHERE subject LIKE ?
        ORDER BY timestamp DESC
        LIMIT ?"""

    c.execute(sql, (f"%{subject}%", args.limit))
    results = c.fetchall()

    print(f"Emails matching subject '{subject}' ({len(results)}):\n")
    for row in results:
        att = "📎" if row[5] else "  "
        print(f"{att} [{row[1][:20]}...] {row[4][:25]}")
        print(f"   From: {row[3]}")
        print(f"   Subject: {row[2]}")
        print()


def cmd_stats(args, conn):
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM emails")
    total = c.fetchone()[0]

    c.execute("SELECT account, COUNT(*) FROM emails GROUP BY account")
    by_account = c.fetchall()

    c.execute(
        "SELECT folder, COUNT(*) FROM emails GROUP BY folder ORDER BY COUNT(*) DESC LIMIT 10"
    )
    by_folder = c.fetchall()

    c.execute(
        "SELECT sender_email, COUNT(*) FROM emails GROUP BY sender_email ORDER BY COUNT(*) DESC LIMIT 10"
    )
    top_senders = c.fetchall()

    c.execute("SELECT COUNT(*) FROM attachments")
    total_attachments = c.fetchone()[0]

    print(f"""
📊 Thunderbird Email Statistics
================================

Total Emails: {total:,}
Total Attachments: {total_attachments:,}

By Account:
""")
    for acc, count in by_account:
        print(f"  {acc}: {count:,}")

    print("\nTop Folders:")
    for folder, count in by_folder:
        print(f"  {folder}: {count:,}")

    print("\nTop Senders:")
    for sender, count in top_senders:
        print(f"  {sender}: {count}")


def cmd_folders(args, conn):
    c = conn.cursor()

    sql = """SELECT account, folder, COUNT(*) as count 
        FROM emails 
        GROUP BY account, folder 
        ORDER BY account, count DESC"""

    c.execute(sql)
    results = c.fetchall()

    current_acc = ""
    for acc, folder, count in results:
        if acc != current_acc:
            print(f"\n📬 {acc}")
            current_acc = acc
        print(f"   {folder}: {count}")


def cmd_attachments(args, conn):
    c = conn.cursor()

    conditions = []
    params = []

    if args.sender:
        conditions.append("e.sender_email LIKE ?")
        params.append(f"%{args.sender}%")

    if args.account and args.account != "all":
        conditions.append("e.account = ?")
        params.append(args.account)

    if args.type:
        conditions.append("a.filename LIKE ?")
        params.append(f"%.{args.type}")

    where = " AND ".join(conditions) if conditions else "1=1"

    sql = f"""SELECT a.filename, a.content_type, a.size, e.subject, e.sender_email, e.account
        FROM attachments a
        JOIN emails e ON a.email_id = e.id
        WHERE {where}
        ORDER BY a.size DESC
        LIMIT ?"""
    params.append(args.limit)

    c.execute(sql, params)
    results = c.fetchall()

    print(f"Found {len(results)} attachments:\n")
    for row in results:
        size_kb = row[2] / 1024
        print(f"📎 {row[0][:50]}")
        print(f"   Type: {row[1]} | Size: {size_kb:.1f} KB")
        print(f"   From: {row[4]} | Account: {row[5][:20]}")
        print(f"   Subject: {row[3][:50]}")
        print()


def cmd_folder_stats(args, conn):
    c = conn.cursor()

    sql = """SELECT account, folder, COUNT(*) as count,
        SUM(CASE WHEN has_attachments = 1 THEN 1 ELSE 0 END) as with_attachments
        FROM emails
        GROUP BY account, folder
        ORDER BY account, count DESC"""

    c.execute(sql)
    results = c.fetchall()

    current_acc = ""
    for acc, folder, count, with_att in results:
        if acc != current_acc:
            print(f"\n📬 {acc}")
            current_acc = acc
        att_pct = (with_att / count * 100) if count > 0 else 0
        print(f"   {folder}: {count} ({att_pct:.0f}% with attachments)")


def cmd_date_range(args, conn):
    c = conn.cursor()

    start_ts = int(datetime.strptime(args.start, "%Y-%m-%d").timestamp())
    end_ts = int(datetime.strptime(args.end, "%Y-%m-%d").timestamp()) + 86400

    sql = """SELECT id, account, folder, subject, sender_email, date
        FROM emails
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY timestamp DESC
        LIMIT ?"""

    c.execute(sql, (start_ts, end_ts, args.limit))
    results = c.fetchall()

    print(f"Emails between {args.start} and {args.end} ({len(results)}):\n")
    for row in results:
        print(f"  [{row[1][:20]}...] {row[2]}: {row[3][:50]}")
        print(f"     From: {row[4]} | {row[5][:25]}")
        print()


def cmd_recent(args, conn):
    c = conn.cursor()

    c.execute(
        """SELECT id, account, folder, subject, sender_email, date, has_attachments
        FROM emails
        ORDER BY timestamp DESC
        LIMIT ?""",
        (args.limit,),
    )

    results = c.fetchall()

    print(f"Recent {len(results)} emails:\n")
    for row in results:
        att = "📎" if row[6] else "  "
        print(f"{att} [{row[1][:20]}...] {row[2]}")
        print(f"   From: {row[4]}")
        print(f"   Subject: {row[3][:60]}")
        print(f"   Date: {row[5][:25]}")
        print()


def cmd_threads(args, conn):
    c = conn.cursor()

    if args.subject:
        search = f"%{args.subject}%"
    else:
        search = "%"

    sql = """SELECT subject, sender_email, COUNT(*) as count, MAX(date) as latest
        FROM emails
        WHERE subject LIKE ?
        GROUP BY subject
        ORDER BY count DESC
        LIMIT ?"""

    c.execute(sql, (search, args.limit))
    results = c.fetchall()

    print(f"Thread analysis ({len(results)} threads):\n")
    for subject, sender, count, latest in results:
        print(f"  📧 {subject[:60]}")
        print(f"     Author: {sender} | Messages: {count} | Latest: {latest[:20]}")
        print()


def cmd_email_body(args, conn):
    c = conn.cursor()

    c.execute(
        """SELECT id, subject, sender_email, body_text 
        FROM emails 
        WHERE id = ?""",
        (args.id,),
    )

    result = c.fetchone()
    if not result:
        print(f"No email found with ID {args.id}")
        return

    print(f"Subject: {result[1]}")
    print(f"From: {result[2]}")
    print("-" * 60)
    print(result[3][: args.chars] if args.chars else result[3])


def main():
    parser = argparse.ArgumentParser(
        prog="thunderbird-indexer", description="Thunderbird Email Indexer & Search"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    p_index = subparsers.add_parser("index", help="Index all emails")

    p_search = subparsers.add_parser("search", help="Search emails")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--account", default="all", help="Filter by account")
    p_search.add_argument("--sender", help="Filter by sender")
    p_search.add_argument("--limit", type=int, default=20, help="Result limit")

    p_fts = subparsers.add_parser("fts", help="Full-text search")
    p_fts.add_argument("query", help="FTS query")
    p_fts.add_argument("--limit", type=int, default=20, help="Result limit")

    p_from = subparsers.add_parser("from", help="Search by sender")
    p_from.add_argument("sender", help="Sender email")
    p_from.add_argument("--limit", type=int, default=20, help="Result limit")

    p_subject = subparsers.add_parser("subject", help="Search by subject")
    p_subject.add_argument("subject", help="Subject keyword")
    p_subject.add_argument("--limit", type=int, default=20, help="Result limit")

    p_stats = subparsers.add_parser("stats", help="Show statistics")

    p_folders = subparsers.add_parser("folders", help="List all folders")

    p_attachments = subparsers.add_parser("attachments", help="List attachments")
    p_attachments.add_argument("--sender", help="Filter by sender")
    p_attachments.add_argument("--account", default="all", help="Filter by account")
    p_attachments.add_argument("--type", help="File extension (e.g., pdf)")
    p_attachments.add_argument("--limit", type=int, default=50, help="Result limit")

    p_folder_stats = subparsers.add_parser(
        "folder-stats", help="Email count per folder"
    )

    p_date = subparsers.add_parser("date-range", help="Search by date range")
    p_date.add_argument("start", help="Start date (YYYY-MM-DD)")
    p_date.add_argument("end", help="End date (YYYY-MM-DD)")
    p_date.add_argument("--limit", type=int, default=50, help="Result limit")

    p_recent = subparsers.add_parser("recent", help="Show recent emails")
    p_recent.add_argument("--limit", type=int, default=20, help="Number of emails")

    p_threads = subparsers.add_parser("threads", help="Analyze email threads")
    p_threads.add_argument("--subject", help="Filter by subject keyword")
    p_threads.add_argument("--limit", type=int, default=20, help="Result limit")

    p_body = subparsers.add_parser("body", help="View email body")
    p_body.add_argument("id", type=int, help="Email ID")
    p_body.add_argument("--chars", type=int, help="Limit characters")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    conn = init_db()

    if args.command == "index":
        cmd_index(args, conn)
    elif args.command == "search":
        cmd_search(args, conn)
    elif args.command == "fts":
        cmd_fts(args, conn)
    elif args.command == "from":
        cmd_from(args, conn)
    elif args.command == "subject":
        cmd_subject(args, conn)
    elif args.command == "stats":
        cmd_stats(args, conn)
    elif args.command == "folders":
        cmd_folders(args, conn)
    elif args.command == "attachments":
        cmd_attachments(args, conn)
    elif args.command == "folder-stats":
        cmd_folder_stats(args, conn)
    elif args.command == "date-range":
        cmd_date_range(args, conn)
    elif args.command == "recent":
        cmd_recent(args, conn)
    elif args.command == "threads":
        cmd_threads(args, conn)
    elif args.command == "body":
        cmd_email_body(args, conn)

    conn.close()


if __name__ == "__main__":
    main()
