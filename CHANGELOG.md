# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-09-03

### Added
- **AI Model Recommendation Engine**: Integrates tailored model recommendations for all 78 Tarot cards across FLUX.1 [dev], Midjourney v6.1, Niji 6, Ideogram 2.0, and Stable Diffusion 3.5 Large.
- **Card Focus & Archetype Guide**: Full 78-card archetypal intelligence database in `tarot_intelligence.py` with symbolic elements, composition cues, and lighting directions.
- **Dynamic Theme Blending**: Automatically adapts traditional card symbolism to active deck themes (e.g. Terraborn Beavers or Cyberpunk).
- **1-Click Focus Injection**: Added "✦ Inject Focus into Prompt" in the Focus Queue and Card Inspector modal, backed by `POST /api/cards/apply_focus`.
- **Visual Model Badges**: Display model badges on individual tarot cards in the 78-card deck grid.
- **CLI Enhancements**: `python prompt_tracker.py --next` now prints the recommended model, specialty, settings, archetype, and composition guidance.

## [1.0.0] - 2026-09-03

### Added
- **Tarot Deck Studio Standalone App**: Lightweight Python HTTP server (`server.py`) and rich dark-fantasy frontend (`public/index.html`, `public/styles.css`, `public/app.js`).
- **Persistent State**: Full JSON database persistence with `deck_state.json` supporting multiple decks and all 78 standard Tarot cards.
- **"Next Up" Focus Queue**: Dedicated hero panel displaying next card prompt with one-click copy and completion workflow.
- **Multi-Deck Idea Builder**: Interactive modal for creating custom 78-card decks with theme presets (Diablo/WoW, Cyberpunk, Gothic Eldritch, Solarpunk, Art Nouveau).
- **Progress Tracking & Analytics**: Radial progress ring, Major/Minor Arcana breakdown bars, and 100% completion celebration banner.
- **Interactive 78-Card Grid**: Filtering by status, search by keyword, and filter tabs across Arcana and suits.
- **Companion CLI Tool**: Full command-line interface (`prompt_tracker.py`) with `--next`, `--complete`, `--progress`, and `--new-deck`.
- **Launcher Script**: Single-command execution via `launch.sh`.
