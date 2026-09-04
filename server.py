#!/usr/bin/env python3
"""
server.py - Standalone Tarot Deck Studio HTTP Server & REST API.

Serves the frontend application and provides persistent API endpoints
backed by deck_state.json.
"""

import json
import os
import sys
import mimetypes
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import webbrowser
import tarot_intelligence

PORT = 8080
PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deck_state.json")
BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")
MAX_BACKUPS = 30

# Tarot constants
MAJOR_ARCANA = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
]
SUITS = ["Wands", "Cups", "Swords", "Pentacles"]
RANKS = ["Ace"] + [str(i) for i in range(2, 11)] + ["Page", "Knight", "Queen", "King"]
MINOR_ARCANA = [f"{rank} of {suit}" for suit in SUITS for rank in RANKS]
STANDARD_78_CARDS = MAJOR_ARCANA + MINOR_ARCANA

DEFAULT_DIABLO_TEMPLATE = """A masterpiece digital illustration of a tarot card representing **{card_name}**. The central subject is {subject_description}. 

Art Style & Theme: A fusion of dark, gothic grimdark atmosphere (Diablo) and bold, stylized heroic fantasy with oversized, intricate armor (World of Warcraft). Include visual motifs of "Terraborn Beavers"—nature-attuned, earth-shaping humanoid beaver-folk with druidic or shamanistic elements. 

Consistent Formatting: Flat 2D tarot layout, perfectly centered composition. The character is framed within a highly ornate, weathered metallic border featuring dark fantasy gothic architecture and geometric Terraborn earth-runes. 

Lighting & Color: Unified color grading using deep crimsons, shadowy blacks, earthy terrestrial browns, and glowing magical accents. Dramatic rim lighting, striking shadows, high contrast, sharp details, fantasy concept art style."""

GENERIC_TAROT_TEMPLATE = """A masterpiece digital illustration of a tarot card representing **{card_name}**. The central subject is {subject_description}.

Art Style & Theme: Highly detailed fantasy illustration with rich symbolic elements reflecting the traditional archetype of the card.

Consistent Formatting: Flat 2D tarot card frame, ornate decorative border, balanced composition.

Lighting & Color: Vibrant contrast, atmospheric lighting, and high-fidelity textures."""


def get_card_suit_or_arcana(card_name: str) -> str:
    if card_name in MAJOR_ARCANA:
        return "Major Arcana"
    for s in SUITS:
        if f" of {s}" in card_name:
            return s
    return "Major Arcana"


def build_card_dict(default_subject: str = "a symbolic archetype") -> dict:
    return {
        card_name: {
            "status": "pending",
            "subject": default_subject,
            "arcana": "major" if card_name in MAJOR_ARCANA else "minor",
            "suit": get_card_suit_or_arcana(card_name),
            "image_url": ""
        }
        for card_name in STANDARD_78_CARDS
    }


def load_db() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                db = json.load(f)
                # Ensure all cards have suit and arcana fields
                updated = False
                for deck in db.get("decks", {}).values():
                    for name, cdata in deck.get("cards", {}).items():
                        if "suit" not in cdata:
                            cdata["suit"] = get_card_suit_or_arcana(name)
                            cdata["arcana"] = "major" if name in MAJOR_ARCANA else "minor"
                            updated = True
                if updated:
                    save_db(db)
                return db
        except Exception as e:
            print(f"Warning reading state file: {e}")

    db = {
        "active_deck": "diablo_beavers",
        "decks": {
            "diablo_beavers": {
                "name": "Diablo / WoW Terraborn Beavers",
                "template": DEFAULT_DIABLO_TEMPLATE,
                "default_subject": "a Terraborn Beaver hero",
                "cards": build_card_dict("a Terraborn Beaver hero")
            }
        }
    }
    save_db(db)
    return db


def ensure_backup_dir():
    os.makedirs(BACKUP_DIR, exist_ok=True)


def prune_backups():
    ensure_backup_dir()
    files = [f for f in os.listdir(BACKUP_DIR) if f.startswith("snapshot_") and f.endswith(".json")]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(BACKUP_DIR, x)))
    while len(files) > MAX_BACKUPS:
        oldest = files.pop(0)
        try:
            os.remove(os.path.join(BACKUP_DIR, oldest))
        except OSError:
            pass


def list_backups() -> list:
    ensure_backup_dir()
    files = [f for f in os.listdir(BACKUP_DIR) if f.endswith(".json")]
    backups = []
    for fname in sorted(files, reverse=True):
        fpath = os.path.join(BACKUP_DIR, fname)
        try:
            mtime = os.path.getmtime(fpath)
            dt = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            size_kb = round(os.path.getsize(fpath) / 1024, 1)
            with open(fpath, "r", encoding="utf-8") as bf:
                bdata = json.load(bf)
            decks = bdata.get("decks", {})
            total_cards = sum(len(d.get("cards", {})) for d in decks.values())
            completed_cards = sum(
                sum(1 for c in d.get("cards", {}).values() if c.get("status") == "complete")
                for d in decks.values()
            )
            backups.append({
                "filename": fname,
                "timestamp": dt,
                "size_kb": size_kb,
                "deck_count": len(decks),
                "total_cards": total_cards,
                "completed_cards": completed_cards
            })
        except Exception:
            continue
    return backups


def create_manual_snapshot(label: str = "") -> dict:
    ensure_backup_dir()
    db = load_db()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_lbl = ("_" + "".join(c for c in label if c.isalnum() or c in "_-")) if label.strip() else ""
    snap_name = f"manual{clean_lbl}_{ts}.json"
    snap_path = os.path.join(BACKUP_DIR, snap_name)
    with open(snap_path, "w", encoding="utf-8") as sf:
        json.dump(db, sf, indent=2)
    return {
        "filename": snap_name,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "size_kb": round(os.path.getsize(snap_path) / 1024, 1)
    }


def restore_from_snapshot(filename: str) -> bool:
    ensure_backup_dir()
    safe_name = os.path.basename(filename)
    snap_path = os.path.join(BACKUP_DIR, safe_name)
    if not os.path.exists(snap_path):
        raise FileNotFoundError(f"Backup file '{safe_name}' not found")

    # Safety pre-restore snapshot
    curr_db = load_db()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safety_snap = os.path.join(BACKUP_DIR, f"safety_prerestore_{ts}.json")
    with open(safety_snap, "w", encoding="utf-8") as sf:
        json.dump(curr_db, sf, indent=2)

    with open(snap_path, "r", encoding="utf-8") as rf:
        restored_db = json.load(rf)

    if not isinstance(restored_db, dict) or "decks" not in restored_db:
        raise ValueError("Invalid database format: missing 'decks' object")

    save_db(restored_db, create_auto_snapshot=False)
    return True


def save_db(db: dict, create_auto_snapshot: bool = True) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)
    if create_auto_snapshot:
        try:
            ensure_backup_dir()
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            snap_path = os.path.join(BACKUP_DIR, f"snapshot_{ts}.json")
            with open(snap_path, "w", encoding="utf-8") as sf:
                json.dump(db, sf, indent=2)
            prune_backups()
        except Exception as e:
            print(f"Warning creating automated snapshot: {e}")


class TarotStudioHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_HEAD(self):
        self.do_GET(is_head=True)

    def send_json(self, data, status=200):
        content = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_error_json(self, message, status=400):
        self.send_json({"error": message}, status)

    def do_GET(self, is_head=False):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # API Endpoints
        if path == "/api/models":
            self.send_json({
                "models": list(tarot_intelligence.MODELS.values()),
                "profiles": tarot_intelligence.MODELS,
                "default": "gemini_nanobanana"
            })
            return

        if path == "/api/backups":
            b_list = list_backups()
            self.send_json({"backups": b_list, "count": len(b_list)})
            return

        if path == "/api/backups/export":
            db = load_db()
            content = json.dumps(db, indent=2).encode("utf-8")
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Disposition", f'attachment; filename="tarot_deck_vault_{ts}.json"')
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            if not is_head:
                self.wfile.write(content)
            return

        if path == "/api/decks":
            db = load_db()
            deck_list = []
            for did, ddata in db.get("decks", {}).items():
                cards = ddata.get("cards", {})
                total = len(cards)
                done = sum(1 for c in cards.values() if c.get("status") == "complete")
                pct = round((done / total * 100) if total > 0 else 0, 1)
                deck_list.append({
                    "id": did,
                    "name": ddata.get("name", did),
                    "total": total,
                    "completed": done,
                    "pending": total - done,
                    "percentage": pct
                })
            if is_head:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
            else:
                self.send_json({
                    "active_deck": db.get("active_deck", "diablo_beavers"),
                    "target_generator": db.get("target_generator", "gemini_nanobanana"),
                    "decks": deck_list
                })
            return

        if path.startswith("/api/decks/"):
            deck_id = path[len("/api/decks/"):]
            db = load_db()
            decks = db.get("decks", {})
            if deck_id not in decks:
                self.send_error_json(f"Deck '{deck_id}' not found", 404)
                return

            deck = decks[deck_id]
            cards = deck.get("cards", {})
            total = len(cards)
            done = sum(1 for c in cards.values() if c.get("status") == "complete")
            pct = round((done / total * 100) if total > 0 else 0, 1)
            
            maj_done = sum(1 for name, c in cards.items() if name in MAJOR_ARCANA and c.get("status") == "complete")
            min_done = sum(1 for name, c in cards.items() if name in MINOR_ARCANA and c.get("status") == "complete")

            # Determine target model
            target_model = db.get("target_generator", "gemini_nanobanana")
            query_params = urllib.parse.parse_qs(parsed.query)
            if "model" in query_params:
                target_model = query_params["model"][0]

            # Find next incomplete card
            next_card = None
            template = deck.get("template", GENERIC_TAROT_TEMPLATE)
            deck_name = deck.get("name", deck_id)
            default_subj = deck.get("default_subject", "the tarot subject")

            for name, cdata in cards.items():
                if cdata.get("status") == "pending":
                    subj = cdata.get("subject", default_subj)
                    rec = tarot_intelligence.get_card_recommendation(
                        name, deck_name, default_subj, target_model=target_model
                    )
                    formatted_prompt = tarot_intelligence.format_uniform_prompt(
                        name,
                        subj,
                        symbols=rec.get("symbols", ""),
                        composition=rec.get("composition", ""),
                        lighting=rec.get("lighting", ""),
                        theme_prompt=template,
                        model_id=target_model
                    )
                    next_card = {
                        "name": name,
                        "data": cdata,
                        "prompt": formatted_prompt,
                        "recommendation": rec
                    }
                    break

            recommendations = {
                name: tarot_intelligence.get_card_recommendation(
                    name, deck_name, default_subj, target_model=target_model
                )
                for name in cards.keys()
            }

            self.send_json({
                "id": deck_id,
                "name": deck_name,
                "template": template,
                "default_subject": default_subj,
                "target_generator": target_model,
                "total": total,
                "completed": done,
                "pending": total - done,
                "percentage": pct,
                "major_completed": maj_done,
                "major_total": len(MAJOR_ARCANA),
                "minor_completed": min_done,
                "minor_total": len(MINOR_ARCANA),
                "next_card": next_card,
                "cards": cards,
                "recommendations": recommendations
            })
            return

        # Serve static files
        if path == "/" or path == "":
            rel_path = "index.html"
        else:
            rel_path = path.lstrip("/")

        file_path = os.path.abspath(os.path.join(PUBLIC_DIR, rel_path))
        # Directory traversal protection
        if not file_path.startswith(PUBLIC_DIR) or not os.path.exists(file_path) or os.path.isdir(file_path):
            file_path = os.path.join(PUBLIC_DIR, "index.html")

        if os.path.exists(file_path) and not os.path.isdir(file_path):
            ctype, _ = mimetypes.guess_type(file_path)
            if not ctype:
                ctype = "application/octet-stream"
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            if not is_head:
                self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            self.send_error_json("Invalid JSON payload", 400)
            return

        db = load_db()

        # Route: Create Deck
        if path == "/api/decks":
            deck_id = body.get("id", "").strip().lower().replace(" ", "_")
            name = body.get("name", "").strip() or deck_id.replace("_", " ").title()
            template = body.get("template", "").strip() or GENERIC_TAROT_TEMPLATE
            subject = body.get("subject", "").strip() or "a fantasy figure"

            if not deck_id:
                self.send_error_json("Deck ID is required", 400)
                return

            if deck_id in db.get("decks", {}):
                self.send_error_json(f"Deck '{deck_id}' already exists", 409)
                return

            db.setdefault("decks", {})[deck_id] = {
                "name": name,
                "template": template,
                "default_subject": subject,
                "cards": build_card_dict(subject)
            }
            db["active_deck"] = deck_id
            save_db(db)
            self.send_json({"success": True, "deck_id": deck_id})
            return

        # Route: Set Active Deck
        if path == "/api/active_deck":
            deck_id = body.get("id")
            if deck_id in db.get("decks", {}):
                db["active_deck"] = deck_id
                save_db(db)
                self.send_json({"success": True, "active_deck": deck_id})
            else:
                self.send_error_json("Deck not found", 404)
            return

        # Route: Toggle Card Status
        if path == "/api/cards/toggle":
            deck_id = body.get("deck_id")
            card_name = body.get("card_name")
            target_status = body.get("status")  # "complete" or "pending" or None to toggle

            decks = db.get("decks", {})
            if deck_id not in decks or card_name not in decks[deck_id]["cards"]:
                self.send_error_json("Card or Deck not found", 404)
                return

            card = decks[deck_id]["cards"][card_name]
            if target_status in ["complete", "pending"]:
                card["status"] = target_status
            else:
                card["status"] = "pending" if card.get("status") == "complete" else "complete"

            save_db(db)
            self.send_json({"success": True, "card": card, "status": card["status"]})
            return

        # Route: Update Global Settings (Target Generator Model)
        if path == "/api/settings":
            if "target_generator" in body:
                db["target_generator"] = body["target_generator"]
            save_db(db)
            self.send_json({"success": True, "target_generator": db.get("target_generator", "gemini_nanobanana")})
            return

        # Route: Create Manual Backup Snapshot
        if path == "/api/backups/create":
            label = body.get("label", "")
            snap_info = create_manual_snapshot(label)
            self.send_json({"success": True, "snapshot": snap_info})
            return

        # Route: Restore from Snapshot
        if path == "/api/backups/restore":
            filename = body.get("filename", "")
            if not filename:
                self.send_error_json("Filename required", 400)
                return
            try:
                restore_from_snapshot(filename)
                self.send_json({"success": True, "restored": filename})
            except Exception as e:
                self.send_error_json(str(e), 500)
            return

        # Route: Import Full Database JSON
        if path == "/api/backups/import":
            imported_db = body.get("database")
            if not isinstance(imported_db, dict) or "decks" not in imported_db:
                self.send_error_json("Invalid database backup structure: missing 'decks'", 400)
                return
            # Safety backup current state before import
            try:
                ensure_backup_dir()
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                safety_snap = os.path.join(BACKUP_DIR, f"safety_preimport_{ts}.json")
                curr_db = load_db()
                with open(safety_snap, "w", encoding="utf-8") as sf:
                    json.dump(curr_db, sf, indent=2)
                save_db(imported_db, create_auto_snapshot=False)
                self.send_json({"success": True, "message": "Database imported successfully"})
            except Exception as e:
                self.send_error_json(f"Import failed: {e}", 500)
            return

        # Route: Update Card Details (with revision memory)
        if path == "/api/cards/update":
            deck_id = body.get("deck_id")
            card_name = body.get("card_name")
            decks = db.get("decks", {})
            if deck_id not in decks or card_name not in decks[deck_id]["cards"]:
                self.send_error_json("Card or Deck not found", 404)
                return

            card = decks[deck_id]["cards"][card_name]
            if "revisions" not in card:
                card["revisions"] = []

            # Check if subject changed, record previous revision
            if "subject" in body and body["subject"] != card.get("subject"):
                card["revisions"].append({
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "subject": card.get("subject", ""),
                    "reason": "manual_edit"
                })
                if len(card["revisions"]) > 15:
                    card["revisions"] = card["revisions"][-15:]
                card["subject"] = body["subject"]

            if "image_url" in body:
                card["image_url"] = body["image_url"]
            if "status" in body:
                card["status"] = body["status"]

            save_db(db)
            self.send_json({"success": True, "card": card})
            return

        # Route: Revert Card to Revision
        if path == "/api/cards/revert":
            deck_id = body.get("deck_id")
            card_name = body.get("card_name")
            rev_idx = body.get("revision_index")
            decks = db.get("decks", {})
            if deck_id not in decks or card_name not in decks[deck_id]["cards"]:
                self.send_error_json("Card or Deck not found", 404)
                return

            card = decks[deck_id]["cards"][card_name]
            revisions = card.get("revisions", [])
            if not isinstance(rev_idx, int) or rev_idx < 0 or rev_idx >= len(revisions):
                self.send_error_json("Invalid revision index", 400)
                return

            target_rev = revisions[rev_idx]
            old_subj = card.get("subject", "")
            # Push current to revisions before reverting
            card["revisions"].append({
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "subject": old_subj,
                "reason": "pre_revert"
            })
            card["subject"] = target_rev.get("subject", old_subj)
            save_db(db)
            self.send_json({"success": True, "card": card, "subject": card["subject"]})
            return

        # Route: Apply Recommended Focus to Card (with revision memory)
        if path == "/api/cards/apply_focus":
            deck_id = body.get("deck_id")
            card_name = body.get("card_name")
            target_model = body.get("target_model") or db.get("target_generator", "gemini_nanobanana")
            decks = db.get("decks", {})
            if deck_id not in decks or card_name not in decks[deck_id]["cards"]:
                self.send_error_json("Card or Deck not found", 404)
                return

            deck = decks[deck_id]
            card = deck["cards"][card_name]

            if "revisions" not in card:
                card["revisions"] = []

            # Save previous subject to revision history
            card["revisions"].append({
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "subject": card.get("subject", ""),
                "reason": "injected_focus"
            })
            if len(card["revisions"]) > 15:
                card["revisions"] = card["revisions"][-15:]

            rec = tarot_intelligence.get_card_recommendation(
                card_name, deck.get("name", ""), deck.get("default_subject", ""), target_model=target_model
            )
            card["subject"] = rec["suggested_subject_focus"]
            save_db(db)
            self.send_json({"success": True, "card": card, "subject": card["subject"], "recommendation": rec})
            return

        # Route: Reset All Cards in Deck
        if path == "/api/decks/reset":
            deck_id = body.get("deck_id")
            decks = db.get("decks", {})
            if deck_id not in decks:
                self.send_error_json("Deck not found", 404)
                return

            for card in decks[deck_id]["cards"].values():
                card["status"] = "pending"
            save_db(db)
            self.send_json({"success": True})
            return

        self.send_error_json("Endpoint not found", 404)


def run_server(port=PORT, open_browser=True):
    # Ensure state file initialized
    load_db()
    server_address = ("", port)
    
    # Try finding an available port if default is taken
    httpd = None
    curr_port = port
    for p in range(curr_port, curr_port + 20):
        try:
            httpd = HTTPServer(("", p), TarotStudioHandler)
            curr_port = p
            break
        except OSError:
            continue

    if not httpd:
        print(f"Error: Could not bind to port in range {port}-{port+20}")
        sys.exit(1)

    url = f"http://localhost:{curr_port}"
    print("=" * 60)
    print(f"✨ Tarot Deck Studio is running!")
    print(f"👉 Local URL: {url}")
    print(f"📂 State Database: {STATE_FILE}")
    print("=" * 60)
    print("Press Ctrl+C to stop the server.")

    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Tarot Deck Studio...")
        httpd.server_close()


if __name__ == "__main__":
    no_browser = "--no-browser" in sys.argv
    port_arg = PORT
    for i, arg in enumerate(sys.argv):
        if arg == "--port" and i + 1 < len(sys.argv):
            try:
                port_arg = int(sys.argv[i + 1])
            except ValueError:
                pass
    run_server(port=port_arg, open_browser=not no_browser)
