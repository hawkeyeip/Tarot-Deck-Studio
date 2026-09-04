# Tarot Deck Builder & Prompt Tracker

A Python command-line utility and state tracking system for generating and tracking image prompts for complete 78-card Tarot decks (22 Major Arcana + 56 Minor Arcana across 4 suits).

## Project Location
`/Users/brandonheisey/.gemini/antigravity-ide/scratch/tarot-prompt-tracker`

## Quick Start

### 1. View the Next Pending Prompt
Fetches the prompt for the next incomplete card in the deck (default is `diablo_beavers`):
```bash
python prompt_tracker.py --next
```

### 2. Mark a Card as Completed
Once you have generated and saved the image:
```bash
python prompt_tracker.py --complete "The Fool"
```

### 3. Check Overall Progress
Displays total cards completed, percentage bar, and breakdown by Major Arcana vs. Minor Arcana:
```bash
python prompt_tracker.py --progress
```

### 4. Create Custom Decks
Build new 78-card decks with custom themes, subjects, or visual templates:
```bash
# Create a deck with custom subject
python prompt_tracker.py --new-deck cyberpunk_oracle --name "Cyberpunk Oracle" --subject "a cybernetic operative"

# Create a deck with a completely custom style template
python prompt_tracker.py --new-deck solar_punk --subject "a solar druid" --template "Tarot illustration of {card_name} featuring {subject_description}, solarpunk brass and lush bioluminescent foliage."
```

### 5. Switch Between Decks
Use `--deck <DECK_ID>` with any command:
```bash
python prompt_tracker.py --deck cyberpunk_oracle --next
python prompt_tracker.py --deck cyberpunk_oracle --complete "The Fool"
python prompt_tracker.py --deck cyberpunk_oracle --progress
```

### 6. List All Decks
```bash
python prompt_tracker.py --list-decks
```

## State File (`deck_state.json`)
All deck configurations, style templates, and completion statuses are saved in `deck_state.json`. You can also manually inspect or backup this JSON file at any time.
