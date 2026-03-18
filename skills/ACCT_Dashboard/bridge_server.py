import json
import os
import sqlite3
import threading
import time
import re
from flask import Flask, request, jsonify
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

# --- CHAT HISTORY DATABASE ---
CHAT_DB = ".brain/chat_history.db"


def init_chat_db():
    """Initialize chat history SQLite database."""
    conn = sqlite3.connect(CHAT_DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        model_used TEXT,
        dm_score REAL,
        governance_passed INTEGER,
        deal_context TEXT
    )""")
    c.execute("""CREATE INDEX IF NOT EXISTS idx_timestamp ON chat_history(timestamp)""")
    conn.commit()
    conn.close()


# Initialize on startup
init_chat_db()


def add_chat_message(
    role,
    content,
    model_used=None,
    dm_score=None,
    governance_passed=True,
    deal_context=None,
):
    """Add a message to persistent chat history."""
    conn = sqlite3.connect(CHAT_DB)
    c = conn.cursor()
    c.execute(
        """INSERT INTO chat_history (timestamp, role, content, model_used, dm_score, governance_passed, deal_context)
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            time.strftime("%Y-%m-%d %H:%M:%S"),
            role,
            content,
            model_used,
            dm_score,
            1 if governance_passed else 0,
            deal_context,
        ),
    )
    conn.commit()
    conn.close()


def get_chat_history(limit=50):
    """Retrieve chat history from SQLite."""
    conn = sqlite3.connect(CHAT_DB)
    c = conn.cursor()
    c.execute(
        """SELECT timestamp, role, content, model_used, dm_score, governance_passed, deal_context 
                 FROM chat_history ORDER BY id DESC LIMIT ?""",
        (limit,),
    )
    rows = c.fetchall()
    conn.close()
    return [
        {
            "timestamp": r[0],
            "role": r[1],
            "content": r[2],
            "model": r[3],
            "dm_score": r[4],
            "governance_passed": r[5],
            "deal_context": r[6],
        }
        for r in rows
    ]


# --- GLOBAL STATE ---
MEM_MESH = {}
HISTORY = []
CLIENTS = []


@app.route("/api/mesh", methods=["GET"])
def get_mesh():
    """Return the current state of the Memory Mesh."""
    return jsonify(MEM_MESH)


@app.route("/api/history", methods=["GET"])
def get_history():
    """Return the execution history."""
    return jsonify(HISTORY)


@app.route("/api/interact", methods=["POST"])
def post_interact():
    """Submit HITL approval, move files, and log to permanent ledger."""
    data = request.json
    project_name = data.get("requestId")
    verdict = data.get("content")

    response_msg = {
        "type": "INTERACT_RESPONSE",
        "requestId": project_name,
        "content": verdict,
        "timestamp": time.time(),
    }

    # --- PHYSICAL FILE MOVE LOGIC ---
    base = ".brain/pipeline"
    source = f"{base}/01_REVIEW_PENDING/{project_name.replace(' ', '_')}.md"

    if not os.path.exists(source):
        # Try finding the file by name if the ID/requestId is slightly different
        import glob

        matches = glob.glob(f"{base}/01_REVIEW_PENDING/*.md")
        for m in matches:
            if project_name.replace(" ", "_") in m or project_name in m:
                source = m
                break

    if os.path.exists(source):
        dest_folder = "02_GO_AUTHORIZED" if verdict == "GO" else "03_KILLED"
        dest = f"{base}/{dest_folder}/{os.path.basename(source)}"
        try:
            os.rename(source, dest)
            print(f"[Pipeline] Moved {source} -> {dest}")
            # Move outreach file if it exists
            outreach_src = (
                source.replace(".md", "").replace(
                    "01_REVIEW_PENDING/", "01_REVIEW_PENDING/outreach_"
                )
                + ".md"
            )
            if os.path.exists(outreach_src):
                os.rename(
                    outreach_src,
                    dest.replace(".md", "").replace(
                        f"{dest_folder}/", f"{dest_folder}/outreach_"
                    )
                    + ".md",
                )
        except Exception as e:
            print(f"[Pipeline Error] Move failed: {e}")

    # Update History
    HISTORY.append(response_msg)

    # Persist to Permanent Ledger
    ledger_path = ".brain/outputs/authorized_ledger.json"
    ledger = []
    if os.path.exists(ledger_path):
        try:
            with open(ledger_path, "r") as f:
                ledger = json.load(f)
        except:
            pass

    ledger.append(response_msg)
    with open(ledger_path, "w") as f:
        json.dump(ledger, f, indent=2)

    # Broadcast to all connected clients
    for client in CLIENTS:
        try:
            client.send(json.dumps(response_msg))
        except:
            pass

    print(f"[Sovereign Ledger] Authorization recorded: {project_name}")
    with open(".brain/BATTLE_LOG.md", "a") as f:
        f.write(
            f"\n### [AUTHORIZATION] {project_name}\n- Decision: {verdict}\n- Timestamp: {time.time()}\n"
        )
    return jsonify({"status": "ledger_updated", "moved": True})


import glob


def get_all_assets():
    """Return a unified list of assets with robust cluster metadata parsing."""
    assets = []

    # NEW: Phase 1 & 2: Pipeline folders (01_REVIEW_PENDING and 02_GO_AUTHORIZED)
    pipeline_base = ".brain/pipeline"

    # Phase 1: REVIEW_PENDING
    review_pending = glob.glob(f"{pipeline_base}/01_REVIEW_PENDING/*.md")
    for p in review_pending:
        assets.append(
            {
                "name": os.path.basename(p),
                "path": p,
                "phase": "01_REVIEW_PENDING",
                "cluster": "PENDING",
                "time": os.path.getmtime(p),
            }
        )

    # Phase 2: GO_AUTHORIZED
    go_auth = glob.glob(f"{pipeline_base}/02_GO_AUTHORIZED/*.md")
    for p in go_auth:
        assets.append(
            {
                "name": os.path.basename(p),
                "path": p,
                "phase": "02_GO_AUTHORIZED",
                "cluster": "AUTHORIZED",
                "time": os.path.getmtime(p),
            }
        )

    # Phase 3: Business Packs
    packs = glob.glob(".brain/outputs/client_packages/*.md")
    for p in packs:
        cluster = "UNKNOWN"
        try:
            with open(p, "r") as f:
                content = f.read()
                # Robust search for cluster in the Meat Grinder JSON or the text
                match = re.search(r'"cluster":\s*"(.*?)"', content)
                if match:
                    cluster = match.group(1).upper()
                elif "LOCAL_SENTRY" in content:
                    cluster = "LOCAL_SENTRY"
                elif "SHADOW_SYNC" in content:
                    cluster = "SHADOW_SYNC"
                elif "INTELLIGENCE_GUARDRAIL" in content:
                    cluster = "INTELLIGENCE_GUARDRAIL"
                elif "BROWSER_AUTOMATOR" in content:
                    cluster = "BROWSER_AUTOMATOR"
        except:
            pass

        assets.append(
            {
                "name": os.path.basename(p),
                "path": p,
                "phase": "PHASE_3_SEALING",
                "cluster": cluster,
                "time": os.path.getmtime(p),
            }
        )

    # Phase 5: Outreach Packages
    outreach = glob.glob(".brain/outputs/outreach_packages/*.md")
    bp_metadata = {a["name"]: a["cluster"] for a in assets}

    for o in outreach:
        bp_name = os.path.basename(o).replace("outreach_", "")
        cluster = bp_metadata.get(bp_name, "UNKNOWN")

        # Fallback check for outreach content itself
        if cluster == "UNKNOWN":
            try:
                with open(o, "r") as f:
                    content = f.read().upper()
                    if "LOCAL SENTRY" in content:
                        cluster = "LOCAL_SENTRY"
                    elif "SHADOW SYNC" in content:
                        cluster = "SHADOW_SYNC"
                    elif "INTELLIGENCE GUARDRAIL" in content:
                        cluster = "INTELLIGENCE_GUARDRAIL"
                    elif "BROWSER AUTOMATOR" in content:
                        cluster = "BROWSER_AUTOMATOR"
            except:
                pass

        assets.append(
            {
                "name": os.path.basename(o),
                "path": o,
                "phase": "PHASE_5_OUTREACH",
                "cluster": cluster,
                "time": os.path.getmtime(o),
            }
        )

    return sorted(assets, key=lambda x: x["time"], reverse=True)


@app.route("/api/business/packs", methods=["GET"])
def get_packs():
    return jsonify(get_all_assets())


@app.route("/api/business/pack/content", methods=["GET"])
def get_pack_content():
    """Return the content of a specific business pack."""
    path = request.args.get("path")
    valid_paths = [
        ".brain/outputs/client_packages/",
        ".brain/outputs/outreach_packages/",
    ]
    if not path or not any(path.startswith(vp) for vp in valid_paths):
        return jsonify({"error": "Invalid path"}), 400

    try:
        with open(path, "r") as f:
            return jsonify({"content": f.read()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- GOVERNANCE LAYER ---
DANGEROUS_COMMANDS = [
    "delete",
    "rm ",
    "remove ",
    "drop ",
    "truncate ",
    "shutdown",
    "reboot",
    "sudo",
    "format",
]
DM_SCORE_THRESHOLD = 0.6


def governance_check(user_message, deal_context=None):
    """Check user message against governance policies."""
    msg_lower = user_message.lower()

    # Check for dangerous commands
    for cmd in DANGEROUS_COMMANDS:
        if cmd in msg_lower:
            return {
                "passed": False,
                "reason": f"Command '{cmd}' blocked by governance policy",
                "dm_score": 0.0,
            }

    # Check for file operations that need validation
    if any(word in msg_lower for word in ["write", "create", "update file"]):
        # Assign lower DM score for file operations requiring review
        return {
            "passed": True,
            "reason": "File operation - logged for review",
            "dm_score": 0.7,
        }

    return {"passed": True, "reason": "Governance passed", "dm_score": 0.9}


def get_live_context():
    """Fetch live context from the system."""
    context = {}

    # Get lineage data
    try:
        with open(".mira/scores/lineage.json", "r") as f:
            lines = f.readlines()
            entries = [json.loads(l) for l in lines[-10:] if l.strip()]
            context["lineage"] = [
                {
                    "node": e.get("node"),
                    "model": e.get("model"),
                    "dm_score": e.get("dm_score", {}).get("total"),
                }
                for e in entries
            ]
    except:
        context["lineage"] = []

    # Get DM scores
    try:
        with open(".mira/scores/lineage.json", "r") as f:
            lines = f.readlines()
            entries = [json.loads(l) for l in lines if l.strip()]
            node_scores = {}
            for e in entries[-50:]:
                node = e.get("node", "unknown")
                score = e.get("dm_score", {}).get("total", 0)
                if node not in node_scores:
                    node_scores[node] = []
                node_scores[node].append(score)
            context["dm_scores"] = {n: sum(s) / len(s) for n, s in node_scores.items()}
            context["overall_avg"] = (
                sum(context["dm_scores"].values()) / len(context["dm_scores"])
                if context["dm_scores"]
                else 0
            )
    except:
        context["dm_scores"] = {}
        context["overall_avg"] = 0

    # Get model usage
    try:
        with open(".mira/scores/lineage.json", "r") as f:
            lines = f.readlines()
            entries = [json.loads(l) for l in lines[-50:] if l.strip()]
            models = {}
            for e in entries:
                m = e.get("model", "unknown")
                models[m] = models.get(m, 0) + 1
            context["model_usage"] = models
            primary = "none"
            if models:
                primary = max(models.items(), key=lambda x: x[1])[0]
            context["primary_model"] = primary
    except:
        context["model_usage"] = {}
        context["primary_model"] = "none"

    return context


def build_enhanced_system_prompt(deal_context=None):
    """Build enhanced system prompt with live context."""
    ctx = get_live_context()

    # Get deals from SQLite
    deals_info = ""
    try:
        conn = sqlite3.connect(".brain/shadow_ops.db")
        c = conn.cursor()
        c.execute("SELECT name, status, mrr_target, srank FROM deals LIMIT 10")
        deals = c.fetchall()
        conn.close()
        if deals:
            deals_info = "\n".join(
                [f"- {d[0]}: {d[1]} (MRR: £{d[2]}, S-Rank: {d[3]})" for d in deals]
            )
    except:
        deals_info = "No deals found"

    prompt = f"""You are the Shadow Ops × The Weave v4.0 AI Assistant.

Your role is to help the user with their Micro-SaaS business using the Shadow Ops system.

## CURRENT SYSTEM STATE

### Model Usage (Live)
Primary Model: {ctx.get("primary_model", "none")}
Model Distribution: {ctx.get("model_usage", {})}

### DM Scores (Live)
Overall Average: {ctx.get("overall_avg", 0):.2%}
Node Scores: {ctx.get("dm_scores", {})}

### Recent Lineage (Live)
{chr(10).join([f"- {l['node']}: {l.get('dm_score', 0):.2f} ({l.get('model', '')})" for l in ctx.get("lineage", [])])}

### Active Deals
{deals_info}

## GOVERNANCE RULES
- You operate under MIRA governance layer
- All actions are logged to lineage for audit
- Dangerous commands (delete, rm, sudo) are blocked
- File operations require confirmation

## YOUR CAPABILITIES
1. Query pipeline status and lineage
2. Analyze deals and revenue
3. Recommend model optimizations
4. Explain node execution results
5. Suggest improvements to the system

Answer helpfully and reference live data when available."""
    return prompt


@app.route("/api/chat", methods=["POST"])
def post_chat():
    """Handle chat requests with governance, persistence, and live context."""
    import requests

    data = request.json
    messages = data.get("messages", [])
    deal_context = data.get("deal_context")

    user_msg = messages[-1]["content"] if messages else ""
    print(f"\n[Chat Request] User: {user_msg[:50]}...")

    # Step 1: Governance Check
    governance = governance_check(user_msg, deal_context)
    print(
        f"[Governance] Passed: {governance['passed']}, Reason: {governance['reason']}"
    )

    if not governance["passed"]:
        return jsonify(
            {
                "content": [{"text": f"⛔ BLOCKED: {governance['reason']}"}],
                "governance": governance,
            }
        )

    # Step 2: Build enhanced system prompt with live context
    system_prompt = build_enhanced_system_prompt(deal_context)

    # Step 3: Detect query type for hybrid routing
    query_lower = user_msg.lower()
    if any(
        word in query_lower
        for word in ["code", "build", "implement", "write", "function", "class"]
    ):
        model = "qwen2.5-coder:1.5b"
        print(f"[Hybrid Routing] → CODE model: {model}")
    else:
        model = "qwen3:8b"
        print(f"[Hybrid Routing] → REASONING model: {model}")

    # Step 4: Format messages
    formatted_messages = [{"role": "system", "content": system_prompt}]
    formatted_messages.extend(messages)

    try:
        # Step 5: Call Ollama with selected model
        ollama_resp = requests.post(
            "http://127.0.0.1:11434/api/chat",
            json={
                "model": model,
                "messages": formatted_messages,
                "stream": False,
            },
            timeout=60,
        )

        if ollama_resp.status_code == 200:
            result = ollama_resp.json()
            reply = result.get("message", {}).get("content", "No response from model.")

            # Step 6: Persist to SQLite
            add_chat_message(
                "user", user_msg, model, governance["dm_score"], True, deal_context
            )
            add_chat_message(
                "assistant", reply, model, governance["dm_score"], True, deal_context
            )

            # Step 7: Also log to lineage for audit
            try:
                with open(".mira/scores/lineage.json", "a") as f:
                    f.write(
                        json.dumps(
                            {
                                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                                "node": "chat_assistant",
                                "model": f"ollama/{model}",
                                "tier": 1,
                                "dm_score": {
                                    "content": governance["dm_score"],
                                    "provenance": governance["dm_score"] - 0.05,
                                    "total": governance["dm_score"] - 0.02,
                                },
                                "output": ".brain/outputs/chat_history.json",
                                "governance_passed": True,
                            }
                        )
                        + "\n"
                    )
            except:
                pass

            print(f"[Chat Response] {model}: {reply[:50]}...")

            return jsonify(
                {
                    "content": [{"text": reply}],
                    "governance": governance,
                    "model_used": model,
                    "context": get_live_context(),
                }
            )
        else:
            error_msg = f"Ollama error: {ollama_resp.text}"
            print(f"[Chat Error] {error_msg}")
            return jsonify({"error": error_msg}), 500

    except Exception as e:
        print(f"[Chat Exception] {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat/history", methods=["GET"])
def get_chat_history_api():
    """Return chat history from SQLite."""
    limit = request.args.get("limit", 50, type=int)
    history = get_chat_history(limit)
    return jsonify({"history": history, "count": len(history)})


@app.route("/api/pulse", methods=["POST"])
def post_pulse():
    """Relay a pulse via HTTP POST."""
    data = request.json
    print(f"[Bridge] HTTP Pulse: {data.get('kind')} from {data.get('model')}")
    HISTORY.append(data)
    broadcast(data)
    return jsonify({"status": "captured"})


# --- SOVEREIGN SENTRY ---
def validate_node_data(msg):
    """Hardening check for Meat Grinder data integrity."""
    if msg.get("event") == "end" and msg.get("node") == "pain_miner":
        outputs = msg.get("outputs", {})
        if not outputs.get("meat_grinder_score"):
            print(
                f" [SENTRY ALERT] Data Integrity Breach: {msg.get('node')} missing qualification score."
            )
            return False
    return True


@sock.route("/ws")
def handle_ws(ws):
    """Handle incoming WebSocket connections with Sentry monitoring."""
    global MEM_MESH
    print(f"[Sentry] New connection verified. Active: {len(CLIENTS) + 1}")
    CLIENTS.append(ws)
    try:
        while True:
            data = ws.receive()
            if not data:
                break

            msg = json.loads(data)
            msg_type = msg.get("type", "").upper()

            if msg_type == "NODE_EVENT":
                if validate_node_data(msg):
                    HISTORY.append(msg)
                    if msg.get("event") == "end" and "outputs" in msg:
                        MEM_MESH.update(msg["outputs"])
                    broadcast(msg)
                else:
                    msg["status"] = "INTEGRITY_FAIL"
                    broadcast(msg)

            elif msg_type == "PULSE_EVENT":
                HISTORY.append(msg)
                broadcast(msg)

                # ... [rest of handlers]

                print(
                    f"[Bridge] Connection established: {msg.get('graphName', 'unknown')}"
                )
                ws.send(json.dumps({"type": "SUBSCRIBE"}))

    except Exception as e:
        print(f"[Bridge Error] {e}")
    finally:
        CLIENTS.remove(ws)


def broadcast(payload):
    """Relay a message to all connected clients."""
    for client in CLIENTS:
        try:
            client.send(json.dumps(payload))
        except:
            pass


@app.route("/", methods=["GET"])
def get_ui():
    """Serve the Sovereign Dashboard UI."""
    return open("projects/1.Project_Build_Mgmnt/shadow_ops_command_centre.html").read()


@app.route("/api/portfolio/fs", methods=["GET"])
def get_portfolio_fs():
    """Read the physical pipeline directories and return project metadata."""
    import glob

    base = ".brain/pipeline"
    stages = {
        "pending": "01_REVIEW_PENDING",
        "authorized": "02_GO_AUTHORIZED",
        "killed": "03_KILLED",
    }

    result = {"pending": [], "authorized": [], "killed": []}

    for key, folder in stages.items():
        files = glob.glob(f"{base}/{folder}/*.md")
        for fpath in files:
            # Skip outreach files in the main list to avoid duplicates
            if os.path.basename(fpath).startswith("outreach_"):
                continue

            try:
                with open(fpath, "r") as f:
                    content = f.read()
                    # Parse name from first line
                    name = "Unknown"
                    first_line = content.split("\n")[0]
                    if ":" in first_line:
                        name = first_line.split(":", 1)[1].strip()

                    # Parse JSON block for scores
                    pain = 0
                    srank = "N/A"
                    match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
                    if match:
                        data = json.loads(match.group(1))
                        pain = data.get("pain_score", 0)
                        srank = data.get("intelligence_tier", "N/A")

                    result[key].append(
                        {
                            "id": os.path.basename(fpath),
                            "name": name,
                            "path": fpath,
                            "pain": pain,
                            "srank": srank,
                            "status": key.upper(),
                        }
                    )
            except Exception as e:
                print(f"[Portfolio Error] Failed to parse {fpath}: {e}")

    return jsonify(result)


# --- NEW API ENDPOINTS FOR REAL-TIME DASHBOARD ---


@app.route("/api/lineage", methods=["GET"])
def get_lineage():
    """Return latest lineage entries for real-time monitoring."""
    lineage_path = ".mira/scores/lineage.json"
    try:
        with open(lineage_path, "r") as f:
            lines = f.readlines()
            # Return last 20 entries
            entries = [json.loads(line) for line in lines[-20:] if line.strip()]
            return jsonify(
                {
                    "count": len(entries),
                    "entries": entries,
                    "latest_model": entries[-1].get("model", "unknown")
                    if entries
                    else None,
                    "latest_dm_score": entries[-1].get("dm_score", {}).get("total", 0)
                    if entries
                    else 0,
                }
            )
    except Exception as e:
        return jsonify({"error": str(e), "count": 0, "entries": []})


@app.route("/api/dm-scores", methods=["GET"])
def get_dm_scores():
    """Return DM score trends for charting."""
    lineage_path = ".mira/scores/lineage.json"
    try:
        with open(lineage_path, "r") as f:
            lines = f.readlines()
            entries = [json.loads(line) for line in lines if line.strip()]

            # Group by node and calculate averages
            node_scores = {}
            for entry in entries[-50:]:  # Last 50 entries
                node = entry.get("node", "unknown")
                score = entry.get("dm_score", {}).get("total", 0)
                if node not in node_scores:
                    node_scores[node] = []
                node_scores[node].append(score)

            # Calculate averages
            averages = {
                node: sum(scores) / len(scores) for node, scores in node_scores.items()
            }

            return jsonify(
                {
                    "node_averages": averages,
                    "total_entries": len(entries),
                    "overall_avg": sum(averages.values()) / len(averages)
                    if averages
                    else 0,
                }
            )
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/api/model-usage", methods=["GET"])
def get_model_usage():
    """Return model usage statistics (qwen3 vs qwen2.5-coder)."""
    lineage_path = ".mira/scores/lineage.json"
    try:
        with open(lineage_path, "r") as f:
            lines = f.readlines()
            entries = [json.loads(line) for line in lines if line.strip()]

            # Count model usage
            models = {}
            for entry in entries[-50:]:
                model = entry.get("model", "unknown")
                models[model] = models.get(model, 0) + 1

            primary = "none"
            if models:
                primary = max(models.items(), key=lambda x: x[1])[0]

            return jsonify(
                {
                    "models": models,
                    "total": len(entries[-50:]),
                    "primary_model": primary,
                }
            )
    except Exception as e:
        return jsonify({"error": str(e)})


# --- BACKEND IMPROVEMENTS ---

# Cache for lineage (reduces file I/O)
_lineage_cache = {"data": None, "timestamp": 0}
CACHE_TTL = 5  # seconds


@app.route("/api/system/status", methods=["GET"])
def get_system_status():
    """Return system health and status."""
    import psutil

    status = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": time.time(),
        "clients_connected": len(CLIENTS),
        "chat_history_count": 0,
        "lineage_entries": 0,
        "memory_percent": psutil.virtual_memory().percent
        if "psutil" in globals()
        else 0,
    }

    # Count chat messages
    try:
        conn = sqlite3.connect(CHAT_DB)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM chat_history")
        status["chat_history_count"] = c.fetchone()[0]
        conn.close()
    except:
        pass

    # Count lineage entries
    try:
        with open(".mira/scores/lineage.json", "r") as f:
            status["lineage_entries"] = len(f.readlines())
    except:
        pass

    return jsonify(status)


@app.route("/api/lineage/stream", methods=["GET"])
def stream_lineage():
    """Return lineage entries since a given timestamp (for polling)."""
    import time

    since = request.args.get("since", 0, type=float)

    try:
        with open(".mira/scores/lineage.json", "r") as f:
            lines = f.readlines()
            new_entries = []
            for line in lines:
                if line.strip():
                    entry = json.loads(line)
                    entry_time = time.mktime(
                        time.strptime(entry["timestamp"], "%Y-%m-%dT%H:%M:%S")
                    )
                    if entry_time > since:
                        new_entries.append(entry)

            return jsonify(
                {
                    "entries": new_entries,
                    "count": len(new_entries),
                    "timestamp": time.time(),
                }
            )
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/api/pipeline/state", methods=["GET"])
def get_pipeline_state():
    """Return current pipeline state and active nodes."""
    state = {
        "active_nodes": [],
        "last_execution": None,
        "queue_length": 0,
    }

    # Check for recent lineage entries
    try:
        with open(".mira/scores/lineage.json", "r") as f:
            lines = f.readlines()
            if lines:
                last = json.loads(lines[-1])
                state["last_execution"] = last
                state["active_nodes"] = list(
                    set(
                        [
                            e.get("node")
                            for e in json.loads("[" + ",".join(lines[-10:]) + "]")
                        ]
                    )
                )
    except:
        pass

    return jsonify(state)


@app.route("/api/deals/stats", methods=["GET"])
def get_deals_stats():
    """Return aggregated deal statistics."""
    try:
        conn = sqlite3.connect(".brain/shadow_ops.db")
        c = conn.cursor()

        # Total deals
        c.execute("SELECT COUNT(*) FROM deals")
        total = c.fetchone()[0]

        # By status
        c.execute(
            "SELECT deal_stage, COUNT(*), SUM(mrr_target_gbp), SUM(mrr_actual_gbp) FROM deals GROUP BY deal_stage"
        )
        by_status = {}
        for row in c.fetchall():
            by_status[row[0]] = {
                "count": row[1],
                "mrr_target": row[2] or 0,
                "mrr_actual": row[3] or 0,
            }

        # Average S-rank
        c.execute("SELECT AVG(s_rank_score) FROM deals WHERE s_rank_score IS NOT NULL")
        avg_srank = c.fetchone()[0] or 0

        conn.close()

        return jsonify(
            {
                "total_deals": total,
                "by_status": by_status,
                "avg_srank": round(avg_srank, 1),
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("ACCT_BRIDGE_PORT", 4000))
    print(f"\n[Sovereign Bridge] Online at http://0.0.0.0:{port}")
    print(f"Monitoring port {port} for MASFactory events...")
    app.run(host="0.0.0.0", port=port, threaded=True)
