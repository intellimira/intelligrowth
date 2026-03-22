---
name: enquiry-automation
description: "MIRA Email Enquiry Automation - Poll Gmail, parse enquiries, score leads, send Telegram alerts. Self-hosted CRM pipeline."
---

# MIRA Enquiry Automation Skill

## Overview

Automated system for processing website enquiries, qualifying leads, and alerting the user.

## Architecture

```
Website Form → mailto: → Thunderbird/Gmail → Poll → Parse → Score → Alert
```

## Components

### 1. Email Polling (`poll_enquiries.py`)
- Polls Gmail IMAP for enquiry emails
- Parses subject/body for contact info
- Saves to local enquiries repo clone
- Auto-syncs to GitHub

### 2. Pain Scoring (`score_leads.py`)
- Calculates lead score (1-10)
- Thresholds:
  - 9-10: 🔥 CRITICAL → Immediate alert
  - 7-8: ⚠️ HIGH → Telegram alert
  - 5-6: 📊 MEDIUM → Weekly digest
  - 3-4: 📝 LOW → Nurture
  - 1-2: ❌ MINIMAL → Log only

### 3. Telegram Alerts (`telegram_alerts.py`)
- Sends instant alerts for score >= 7
- Weekly digest every Monday 9am
- Formatted with urgency labels

## Setup

### 1. Gmail IMAP Access
```bash
# Enable IMAP in Gmail Settings
# Generate App Password: https://myaccount.google.com/security
echo "your-app-password" > ~/.config/himalaya/password
```

### 2. Telegram Bot
```bash
# Create bot via @BotFather
# Set environment variables:
export MIRA_TELEGRAM_BOT_TOKEN="your-bot-token"
export MIRA_TELEGRAM_CHAT_ID="your-chat-id"
```

### 3. Clone Enquiries Repo
```bash
git clone https://github.com/intellimira/enquiries.git ~/MiRA/enquiries_local
```

## Usage

### Manual Run
```bash
# Poll for new enquiries
python3 ~/MiRA/Memory_Mesh/poll_enquiries.py

# Score all leads
python3 ~/MiRA/Memory_Mesh/score_leads.py

# Send Telegram alerts
python3 ~/MiRA/Memory_Mesh/telegram_alerts.py

# Send weekly digest
python3 ~/MiRA/Memory_Mesh/telegram_alerts.py --digest
```

### Cron Setup
```bash
# Add to crontab
*/5 * * * * python3 ~/MiRA/Memory_Mesh/poll_enquiries.py && python3 ~/MiRA/Memory_Mesh/telegram_alerts.py >> ~/MiRA/Memory_Mesh/cron.log 2>&1
0 9 * * 1 python3 ~/MiRA/Memory_Mesh/telegram_alerts.py --digest >> ~/MiRA/Memory_Mesh/cron.log 2>&1
```

## Lead Tally

### Running Metrics
- Qualified (5+): Leads ready for outreach
- Not Qualified (<5): Needs more nurturing
- Pending: Awaiting scoring

### Report Format
```
━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 MIRA LEAD SCORING REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━
Qualified: X (Y%)
Not Qualified: X (Y%)
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Self-Improvement Integration

Enquiries are stored as training data in:
```
~/MiRA/Memory_Mesh/training_data/enquiries/
```

Patterns identified from enquiries are used to:
1. Improve pain scoring keywords
2. Generate new skills based on needs
3. Update website content

## Files

| File | Purpose |
|------|---------|
| `poll_enquiries.py` | Gmail IMAP polling |
| `score_leads.py` | Pain score calculation |
| `telegram_alerts.py` | Telegram notifications |

## Status

✅ Active - Cron jobs configured
