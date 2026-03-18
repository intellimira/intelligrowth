# thunderbird-oauth-reset

## Purpose
Autonomous Thunderbird OAuth token reset for Gmail accounts. Handles expired tokens, auth failures, and OAuth re-authentication flows.

## When to Use
- Gmail OAuth authentication failing in Thunderbird
- "Authentication failed" errors when sending email
- Thunderbird prompting for password repeatedly
- Post-Google OAuth policy changes (2025-2026)

## Workflow

### Phase 1: Detect & Identify
```
1. Find Thunderbird profile via profiles.ini
2. Parse logins.json for oauth://accounts.google.com entries
3. Correlate OAuth entries with IMAP/SMTP entries to identify target account
4. List all Gmail accounts with their UUIDs
```

### Phase 2: Reset OAuth Token
```
1. Remove target OAuth entry from logins.json (by UUID)
2. Optionally clear storage-sync-v2.sqlite OAuth cache
3. Backup original logins.json with timestamp
```

### Phase 3: Trigger Re-auth
```
1. Launch Thunderbird (snap or native)
2. Thunderbird opens browser OAuth flow automatically
3. User completes Google OAuth in browser
4. Verify new token written to logins.json
```

### Phase 4: Send Email (Optional)
```
1. Compose and send test email via Thunderbird
2. Verify SMTP success
```

## Target Account
- `intellimira@gmail.com` (smtp1, server2)

## Files Modified
| File | Action |
|------|--------|
| `logins.json` | Remove OAuth entry |
| `storage-sync-v2.sqlite` | Clear OAuth cache (optional) |

## Profile Location
```
~/.thunderbird/s72xlcuu.default/
```
(Snap: `/home/sir-v/snap/thunderbird/common/.thunderbird/`)

## Dependencies
- python3
- sqlite3 (CLI)
- Thunderbird running

## Usage
```bash
# Run the reset
python3 scripts/reset_oauth.py --email intellimira@gmail.com

# Dry run (show what would be removed)
python3 scripts/reset_oauth.py --email intellimira@gmail.com --dry-run

# With email send
python3 scripts/reset_oauth.py --email intellimira@gmail.com --send-email
```

## Safety
- Always creates timestamped backup before modification
- Only modifies targeted account's OAuth entry
- Does not touch IMAP/SMTP credentials
