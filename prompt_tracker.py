#!/usr/bin/env python3
"""
prompt_tracker.py - Generalized Tarot Deck Builder & Prompt Tracker CLI.

Manages prompt generation, progress tracking, and deck creation for 78-card Tarot decks.
Default initial test deck: 'diablo_beavers' (Diablo / World of Warcraft / Terraborn Beavers theme).
"""

import argparse
import json
import os
import sys
import tarot_intelligence

STATE_FILE = "deck_state.json"

DEFAULT_DIABLO_TEMPLATE = """A masterpiece digital illustration of a tarot card representing **{card_name}**. The central subject is {subject_description}. 

Art Style & Theme: A fusion of dark, gothic grimdark atmosphere (Diablo) and bold, stylized heroic fantasy with oversized, intricate armor (World of Warcraft). Include visual motifs of "Terraborn Beavers"—nature-attuned, earth-shaping humanoid beaver-folk with druidic or shamanistic elements. 

Consistent Formatting: Flat 2D tarot layout, perfectly centered composition. The character is framed within a highly ornate, weathered metallic border featuring dark fantasy gothic architecture and geometric Terraborn earth-runes. 

Lighting & Color: Unified color grading using deep crimsons, shadowy blacks, earthy terrestrial browns, and glowing magical accents. Dramatic rim lighting, striking shadows, high contrast, sharp details, fantasy concept art style."""

GENERIC_TAROT_TEMPLATE = """A masterpiece digital illustration of a tarot card representing **{card_name}**. The central subject is {subject_description}.

Art Style & Theme: Highly detailed fantasy illustration with rich symbolic elements reflecting the traditional archetype of the card.

Consistent Formatting: Flat 2D tarot card frame, ornate decorative border, balanced composition.

Lighting & Color: Vibrant contrast, atmospheric lighting, and high-fidelity textures."""

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


def build_card_dict(default_subject: str = "a symbolic archetype") -> dict:
    """Build the standard 78-card dictionary with pending status."""
    return {
        card_name: {
            "status": "pending",
            "subject": default_subject,
            "arcana": "major" if card_name in MAJOR_ARCANA else "minor"
        }
        for card_name in STANDARD_78_CARDS
    }


def load_database() -> dict:
    """Load the state file, initializing it with the diablo_beavers deck if missing."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {STATE_FILE} contains invalid JSON. Please check or backup the file.")
            sys.exit(1)

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
    save_database(db)
    print(f"Created new state database '{STATE_FILE}' with initial 'diablo_beavers' test deck (78 cards).")
    return db


def save_database(db: dict) -> None:
    """Save the database to disk."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)


def get_deck(db: dict, deck_id: str) -> dict:
    """Retrieve a deck by ID or exit with a helpful error."""
    decks = db.get("decks", {})
    if deck_id not in decks:
        available = ", ".join(decks.keys()) if decks else "none"
        print(f"Error: Deck '{deck_id}' not found.")
        print(f"Available decks: {available}")
        print(f"To create a new deck: python prompt_tracker.py --new-deck {deck_id}")
        sys.exit(1)
    return decks[deck_id]


def get_next_prompt(deck_id: str) -> None:
    """Fetch and display the next pending card prompt for the deck with model and focus recommendations."""
    db = load_database()
    deck = get_deck(db, deck_id)
    template = deck.get("template", GENERIC_TAROT_TEMPLATE)
    deck_name = deck.get("name", deck_id)
    default_subj = deck.get("default_subject", "the tarot subject")

    for card_name, data in deck["cards"].items():
        if data["status"] == "pending":
            subject = data.get("subject", default_subj)
            prompt = template.format(card_name=card_name, subject_description=subject)
            rec = tarot_intelligence.get_card_recommendation(card_name, deck_name, default_subj)

            print(f"\n========================================================")
            print(f"  NEXT CARD [{deck_id}]: {card_name.upper()}")
            print(f"  Classification: {rec['type']}")
            print(f"========================================================\n")
            print(f"💡 RECOMMENDED MODEL: {rec['recommended_model']}")
            print(f"   • Specialty : {rec['model_rationale']}")
            print(f"   • Settings  : {rec['recommended_settings']}")
            print(f"\n🎯 SYMBOLIC & ARTISTIC FOCUS:")
            print(f"   • Archetype   : {rec['archetype']}")
            print(f"   • Key Symbols : {rec['symbols']}")
            print(f"   • Composition : {rec['composition']}")
            print(f"   • Lighting    : {rec['lighting']}")
            print(f"\n--------------------------------------------------------")
            print(f"FULL GENERATION PROMPT:")
            print(f"--------------------------------------------------------\n")
            print(prompt)
            print(f"\n--------------------------------------------------------")
            print(f"When finished generating and saving the image, run:")
            print(f'  python prompt_tracker.py --deck "{deck_id}" --complete "{card_name}"')
            print(f"--------------------------------------------------------\n")
            return

    print(f"\n🎉 All 78 cards in deck '{deck_id}' are complete! Congratulations!")


def mark_complete(deck_id: str, card_name_query: str) -> None:
    """Mark a specific card as complete (supports case-insensitive lookup)."""
    db = load_database()
    deck = get_deck(db, deck_id)
    cards = deck["cards"]

    # Match exact or case-insensitive
    target_card = None
    for name in cards.keys():
        if name.lower() == card_name_query.strip().lower():
            target_card = name
            break

    if not target_card:
        print(f"Error: Card '{card_name_query}' not recognized in standard 78-card Tarot deck.")
        print("Example card names: 'The Fool', 'Death', 'Ace of Cups', '3 of Swords'")
        sys.exit(1)

    cards[target_card]["status"] = "complete"
    save_database(db)
    print(f"✓ Successfully marked '{target_card}' in deck '{deck_id}' as complete.")


def show_progress(deck_id: str) -> None:
    """Display completion metrics, progress bar, and breakdown."""
    db = load_database()
    deck = get_deck(db, deck_id)
    cards = deck["cards"]

    total = len(cards)
    completed = sum(1 for c in cards.values() if c.get("status") == "complete")
    pending = total - completed
    pct = (completed / total * 100) if total > 0 else 0

    # Major vs Minor Arcana breakdown
    maj_total = len(MAJOR_ARCANA)
    maj_done = sum(1 for name, c in cards.items() if name in MAJOR_ARCANA and c.get("status") == "complete")
    min_total = len(MINOR_ARCANA)
    min_done = sum(1 for name, c in cards.items() if name in MINOR_ARCANA and c.get("status") == "complete")

    bar_width = 30
    filled = int(round(bar_width * completed / float(total))) if total > 0 else 0
    bar = "█" * filled + "░" * (bar_width - filled)

    deck_title = deck.get("name", deck_id)
    print(f"\n========================================================")
    print(f"  PROGRESS: {deck_title} ({deck_id})")
    print(f"========================================================")
    print(f"  [{bar}] {pct:5.1f}%\n")
    print(f"  • Total Cards Completed : {completed} / {total}")
    print(f"  • Pending Cards         : {pending}")
    print(f"  • Major Arcana (0-XXI)  : {maj_done} / {maj_total} ({maj_done/maj_total*100:4.1f}%)")
    print(f"  • Minor Arcana (4 Suits): {min_done} / {min_total} ({min_done/min_total*100:4.1f}%)")
    print(f"========================================================\n")


def list_decks() -> None:
    """List all available decks and their high-level completion status."""
    db = load_database()
    decks = db.get("decks", {})
    if not decks:
        print("No decks found in database.")
        return

    print(f"\n{'DECK ID':<20} {'NAME':<35} {'PROGRESS':<15}")
    print("-" * 72)
    for deck_id, deck in decks.items():
        cards = deck.get("cards", {})
        total = len(cards)
        done = sum(1 for c in cards.values() if c.get("status") == "complete")
        pct = (done / total * 100) if total > 0 else 0
        name = deck.get("name", deck_id)[:33]
        print(f"{deck_id:<20} {name:<35} {done}/{total} ({pct:.0f}%)")
    print()


def create_new_deck(deck_id: str, name: str = None, template: str = None, subject: str = None) -> None:
    """Create a new 78-card deck with custom template and subject."""
    db = load_database()
    decks = db.setdefault("decks", {})

    if deck_id in decks:
        print(f"Deck '{deck_id}' already exists!")
        return

    display_name = name if name else deck_id.replace("_", " ").title()
    default_subject = subject if subject else "a fantasy figure"
    final_template = template if template else GENERIC_TAROT_TEMPLATE

    decks[deck_id] = {
        "name": display_name,
        "template": final_template,
        "default_subject": default_subject,
        "cards": build_card_dict(default_subject)
    }
    save_database(db)
    print(f"✓ Deck '{deck_id}' ('{display_name}') successfully created with 78 cards!")
    print(f"To view the first prompt, run:")
    print(f"  python prompt_tracker.py --deck {deck_id} --next")


def main():
    parser = argparse.ArgumentParser(
        description="Tarot Deck Builder & Prompt Tracker - Manage and track 78-card Tarot decks with custom art templates."
    )
    parser.add_argument("--deck", default="diablo_beavers", help="The ID of the deck to work on (default: diablo_beavers)")
    parser.add_argument("--next", action="store_true", help="Get the next pending tarot card prompt")
    parser.add_argument("--complete", type=str, help="Mark a specific card as complete (e.g., 'The Fool')")
    parser.add_argument("--progress", action="store_true", help="View overall completion progress and stats")
    parser.add_argument("--list-decks", action="store_true", help="List all available decks and their status")
    parser.add_argument("--new-deck", type=str, help="Create a new 78-card deck with the specified ID")
    parser.add_argument("--name", type=str, help="Optional display name for the new deck")
    parser.add_argument("--template", type=str, help="Custom prompt template (must include {card_name} and {subject_description})")
    parser.add_argument("--subject", type=str, help="Default subject description for the new deck")

    args = parser.parse_args()

    if args.list_decks:
        list_decks()
    elif args.new_deck:
        create_new_deck(args.new_deck, name=args.name, template=args.template, subject=args.subject)
    elif args.next:
        get_next_prompt(args.deck)
    elif args.complete:
        mark_complete(args.deck, args.complete)
    elif args.progress:
        show_progress(args.deck)
    else:
        # If no action flag given, initialize database and display help summary
        load_database()
        print("\nTarot Deck Builder & Prompt Tracker initialized.")
        print("Available commands:")
        print("  python prompt_tracker.py --next")
        print('  python prompt_tracker.py --complete "The Fool"')
        print("  python prompt_tracker.py --progress")
        print("  python prompt_tracker.py --list-decks")
        print("  python prompt_tracker.py --new-deck <deck_id> [--subject ...] [--template ...]")


if __name__ == "__main__":
    main()
