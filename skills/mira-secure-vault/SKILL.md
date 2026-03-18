# MIRA Secure Vault - SKILL.md

## Overview

Military-grade secrets management system for MIRA. Encrypts and stores API keys, passwords, tokens, and sensitive credentials using GPG 4096-bit RSA encryption.

---

## Architecture

```
~/.mira/secrets/
├── vault/           # Encrypted secrets storage
│   ├── github_token.gpg
│   ├── openai_key.gpg
│   └── ...
├── keys/            # Key management
└── mira-vault.sh    # Vault CLI
```

---

## Quick Start

### 1. Initialize Vault (One-time)
```bash
~/.mira/secrets/mira-vault.sh init
```

### 2. Add a Secret
```bash
~/.mira/secrets/mira-vault.sh add <name> <value>
```

### 3. Retrieve a Secret
```bash
~/.mira/secrets/mira-vault.sh get <name>
```

### 4. List All Secrets
```bash
~/.mira/secrets/mira-vault.sh list
```

---

## Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize vault with GPG key |
| `add <name> <value>` | Add encrypted secret |
| `get <name>` | Decrypt and display secret |
| `list` | List stored secret names |
| `delete <name>` | Remove secret |
| `rotate` | Re-encrypt all secrets (key rotation) |
| `backup` | Create encrypted backup |
| `audit` | Verify vault integrity |

---

## Security Specifications

### Encryption
- **Algorithm:** AES-256-GCM (via GPG)
- **Key Size:** 4096-bit RSA
- **Key Type:** RSA with subkeys
- **Expiration:** Never (0)

### Access Control
- Directory permissions: `700` (owner only)
- File permissions: `600` (owner read/write)
- No plaintext secrets in filesystem

### Audit Trail
- All vault operations logged
- Key rotation timestamps
- Access attempts tracked

---

## Usage Examples

### Store GitHub Token
```bash
~/.mira/secrets/mira-vault.sh add github_token "ghp_xxxxxxxxxxxx"
```

### Store API Key
```bash
~/.mira/secrets/mira-vault.sh add openai_key "sk-xxxxxxxxxxxxxxxx"
```

### Use in Scripts
```bash
# Decrypt to environment variable (secure)
export GITHUB_TOKEN=$(~/.mira/secrets/mira-vault.sh get github_token)

# Use in git operations
git push origin main
```

### SSH Key Management
```bash
# Store SSH private key
~/.mira/secrets/mira-vault.sh add ssh_key "$(cat ~/.ssh/id_ed25519)"

# Retrieve when needed
~/.mira/secrets/mira-vault.sh get ssh_key > ~/.ssh/id_ed25519
chmod 600 ~/.ssh/id_ed25519
```

---

## Best Practices

1. **Never commit secrets** - Use `.env.example` as template, not actual values
2. **Rotate regularly** - Run `mira-vault.sh rotate` quarterly
3. **Backup vault** - Store encrypted backup in secure location
4. **Use SSH** - Prefer SSH keys over tokens where possible
5. **最小权限** - Grant only necessary access to each credential

---

## Compliance

- [ ] AES-256 encryption at rest
- [ ] RSA-4096 key pairs
- [ ] No plaintext storage
- [ ] Audit logging
- [ ] Key rotation capability
- [ ] Secure memory handling

---

## Integration

### With GitHub (after adding SSH key)
```bash
# Configure git to use SSH
git remote set-url origin git@github.com:intellimira/MiRA.git

# Test connection
ssh -T git@github.com
```

### Environment Variables
```bash
# Load secrets for session
source <(~/.mira/secrets/mira-vault.sh export-all)
```

---

## Troubleshooting

### "No secret found"
- Check vault is initialized: `~/.mira/secrets/mira-vault.sh list`
- Verify secret name spelling

### "GPG key not found"
- Re-initialize: `~/.mira/secrets/mira-vault.sh init`

### Permission denied
- Check directory permissions: `ls -la ~/.mira/secrets/`
- Should show `drwx------` for all directories

---

## Files

| File | Purpose |
|------|---------|
| `mira-vault.sh` | Main CLI tool |
| `vault/` | Encrypted secrets |
| `keys/` | Key storage |
| `.env.example` | Environment template |

---

## Related

- [MIRA-OJ SKILL.md](../mira-oj/SKILL.md)
- [Session Guardian](../session-guardian/SKILL.md)
- [The Library](../library/SKILL.md)
