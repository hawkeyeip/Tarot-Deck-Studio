"""
tarot_intelligence.py - Archetypal knowledge base, model recommendations, and compositional focuses for all 78 Tarot cards.
"""

# AI Model Profiles
MODELS = {
    "gemini_nanobanana": {
        "id": "gemini_nanobanana",
        "name": "Gemini (Nano Banana / Imagen 3)",
        "badge_color": "#38bdf8",
        "badge_bg": "rgba(56, 189, 248, 0.15)",
        "specialty": "Tactile natural materials, cohesive atmospheric lighting, rich symbolic narrative prose",
        "guidance": "Portrait 2:3 Tarot Framing, Pure Natural Language Prose",
        "is_llm": True
    },
    "flux_dev": {
        "id": "flux_dev",
        "name": "FLUX.1 [dev]",
        "badge_color": "#10b981",
        "badge_bg": "rgba(16, 185, 129, 0.15)",
        "specialty": "Anatomical precision, intricate filigree, crisp hands & armor runes",
        "guidance": "High precision concept art, balanced compositional weight",
        "is_llm": False
    },
    "dalle3": {
        "id": "dalle3",
        "name": "DALL-E 3 (ChatGPT)",
        "badge_color": "#a855f7",
        "badge_bg": "rgba(168, 85, 247, 0.15)",
        "specialty": "Literal archetype interpretation, rich fantasy scene narrative",
        "guidance": "Detailed descriptive visual scene, vertical 2:3 framing",
        "is_llm": True
    },
    "universal": {
        "id": "universal",
        "name": "Universal Multimodal",
        "badge_color": "#f59e0b",
        "badge_bg": "rgba(245, 158, 11, 0.15)",
        "specialty": "Clean visual description adaptable across any generation engine",
        "guidance": "Standard 2D Tarot format, balanced illumination",
        "is_llm": True
    },
    "midjourney_v6": {
        "id": "midjourney_v6",
        "name": "Midjourney v6.1 (Legacy)",
        "badge_color": "#ec4899",
        "badge_bg": "rgba(236, 72, 153, 0.15)",
        "specialty": "Grimdark painterly aesthetic, volumetric fog",
        "guidance": "Dark fantasy art style",
        "is_llm": False
    }
}

# Major Arcana Archetype Focuses
MAJOR_ARCANA_FOCUS = {
    "The Fool": {
        "archetype": "The Leap of Faith & Unlimited Potential",
        "symbols": "Standing fearlessly on the precipice of a jagged cliff, carrying an embroidered knapsack, accompanied by a loyal bounding companion, holding a pure white rose.",
        "composition": "Dynamic low-angle wide shot, golden dawn sunrise illuminating mountain peaks, wind whipping robes outward.",
        "model": "gemini_nanobanana",
        "lighting": "Warm morning rim light contrasting against shadowed abyss"
    },
    "The Magician": {
        "archetype": "Mastery, Willpower & Elemental Manifestation",
        "symbols": "Glowing lemniscate (infinity symbol) hovering as a halo, one hand pointing upward to heaven and one hand grounding toward earth, altar holding the 4 sacred relics: wand, cup, blade, pentacle.",
        "composition": "Centered heroic frontal portrait, eyes crackling with arcane power, swirling elemental motes.",
        "model": "flux_dev",
        "lighting": "Bioluminescent arcane glow from the altar, high contrast dramatic lighting"
    },
    "The High Priestess": {
        "archetype": "Intuition, Sacred Mystery & The Subconscious",
        "symbols": "Seated between two monumental pillars (Boaz and Jachin - dark obsidian and luminescent marble), veil woven with sacred pomegranates and palms, crescent moon at the feet, ancient scroll of secrets in hand.",
        "composition": "Symmetrical, reverent eye-level framing, ethereal mist swirling around stone columns.",
        "model": "gemini_nanobanana",
        "lighting": "Cool lunar blue chiaroscuro with silver moonbeams"
    },
    "The Empress": {
        "archetype": "Abundance, Fertility & Earth Creation",
        "symbols": "Regal crown of twelve twelve-pointed stars, flowing gown adorned with golden sheaves and pomegranates, velvet cushions atop a throne surrounded by cascading waterfalls and ripe harvest fields.",
        "composition": "Warm medium shot, rich verdant lushness, golden ratio framing.",
        "model": "flux_dev",
        "lighting": "Warm golden hour sunlight filtering through canopy leaves"
    },
    "The Emperor": {
        "archetype": "Authority, Order, Mastery & Sovereign Power",
        "symbols": "Monolithic stone throne carved with ram heads, heavy plate armor beneath imperial crimson robes, golden orb in left hand and ankh scepter in right, craggy volcanic fortress mountains behind.",
        "composition": "Imposing low-angle shot establishing supreme stoic dominance and unyielding stature.",
        "model": "gemini_nanobanana",
        "lighting": "Deep volcanic crimson backlighting and sharp metallic edge highlights"
    },
    "The Hierophant": {
        "archetype": "Tradition, Spiritual Wisdom & Sacred Keys",
        "symbols": "Triple papal crown (tiara), triple cross scepter, two acolytes kneeling in reverence, crossed golden and silver keys of esoteric wisdom resting on an altar carpet.",
        "composition": "Architectural cathedral perspective, gothic vaulted arches rising into towering shadows.",
        "model": "flux_dev",
        "lighting": "Shafts of sacred light through stained glass illuminating incense smoke"
    },
    "The Lovers": {
        "archetype": "Divine Union, Choice & Cosmic Harmony",
        "symbols": "Angel Raphael hovering with outstretched scarlet wings in golden clouds, twin figures beneath the Tree of Life (twelve fruits) and Tree of Knowledge (serpent entwined), fiery mountain in the distance.",
        "composition": "Harmonious triad composition, golden ethereal glow connecting the figures.",
        "model": "gemini_nanobanana",
        "lighting": "Soft celestial radiance, radiant aura effects"
    },
    "The Chariot": {
        "archetype": "Willpower, Triumph & Controlled Momentum",
        "symbols": "Armored champion inside a chariot canopy studded with stars, held aloft by two sphinxes (one black, one white), holding a wand of destiny, fortified citadel behind.",
        "composition": "Dynamic head-on charge, low camera angle showing sheer unstoppable momentum.",
        "model": "niji_6",
        "lighting": "Blinding sunrise rim lighting against billowing dust and energy trails"
    },
    "Strength": {
        "archetype": "Gentle Mastery, Courage & Inner Compassion",
        "symbols": "Serene figure gently holding open the jaws of a fierce golden lion, wearing a garland of fresh flowers, glowing infinity lemniscate above the brow, peaceful alpine meadows.",
        "composition": "Intimate medium close-up highlighting tenderness overcoming brute ferocity.",
        "model": "flux_dev",
        "lighting": "Warm sunset amber light creating soft hair and fur textures"
    },
    "The Hermit": {
        "archetype": "Solitude, Inner Guidance & Sacred Truth",
        "symbols": "Elderly cloaked wanderer on an icy mountaintop, holding high a lantern containing a glowing six-pointed star of truth, leaning upon a gnarled walking staff.",
        "composition": "Vertical solitude composition, solitary beacon illuminating snow and precipice.",
        "model": "gemini_nanobanana",
        "lighting": "Single focal lantern light casting long shadows across snowdrifts"
    },
    "Wheel of Fortune": {
        "archetype": "Cycles of Destiny, Karma & Constant Transformation",
        "symbols": "Gigantic bronze and stone celestial wheel inscribed with Hebrew and alchemical symbols, Sphinx atop the wheel, Anubis ascending, Typhon descending, winged cherub creatures at the 4 corners.",
        "composition": "Epic symmetrical cosmic diagram, swirling nebulae and celestial clockwork.",
        "model": "ideogram_2",
        "lighting": "Mystical prismatic cosmic glow with golden celestial rings"
    },
    "Justice": {
        "archetype": "Truth, Balance, Cause & Effect",
        "symbols": "Seated figure between two gray pillars, double-edged upright sword in right hand, balanced brass scales of truth in left, square clasp on royal mantle.",
        "composition": "Strict geometric symmetry, direct piercing gaze, clean architectural balance.",
        "model": "flux_dev",
        "lighting": "Clear unyielding daylight, sharp metallic reflections on sword blade"
    },
    "The Hanged Man": {
        "archetype": "Surrender, New Perspective & Enlightenment",
        "symbols": "Suspended upside-down by one foot from a living wooden T-cross (world tree) with green budding leaves, hands behind back forming a triangle, glowing halo around head, tranquil serene expression.",
        "composition": "Inverted perspective, meditative halo creating radiant circular backlight.",
        "model": "gemini_nanobanana",
        "lighting": "Spiritual golden glow radiating from the crown of the head into dark woods"
    },
    "Death": {
        "archetype": "Profound Transformation, Rebirth & Endings",
        "symbols": "Skeletal knight in black plate armor riding a white stallion, holding a black banner embroidered with the mystic white rose of life, rising golden sun between twin distant watchtowers.",
        "composition": "Solemn processional profile shot, fallen king and praying child along the riverbank.",
        "model": "gemini_nanobanana",
        "lighting": "Dark apocalyptic twilight with a piercing beam of rebirth on the horizon"
    },
    "Temperance": {
        "archetype": "Alchemy, Balance, Patience & Spiritual Flow",
        "symbols": "Winged angel with one foot on earth and one in water, pouring glowing celestial liquid between two golden chalices in an unbroken continuous stream, mountain path leading to a glowing crown.",
        "composition": "Graceful contrapposto stance, liquid pouring caught in mid-air suspension.",
        "model": "flux_dev",
        "lighting": "Iridescent water and glowing magical streams with morning mist"
    },
    "The Devil": {
        "archetype": "Shadow Self, Bondage, Temptation & Raw Instinct",
        "symbols": "Horned baphomet chimera perched on a stone altar, inverted pentagram ablaze between horns, torch held downward, two chained figures with tails standing below with loose chains.",
        "composition": "Towering oppressive angle, ominous monolithic altar in deep subterranean crypt.",
        "model": "gemini_nanobanana",
        "lighting": "Hellish sulfurous red and ember glow cutting through pitch black shadows"
    },
    "The Tower": {
        "archetype": "Sudden Breakthrough, Shattering of False Structures",
        "symbols": "Ancient monolithic stone tower struck by a violent lightning bolt, golden crown blasted off the summit, flames bursting from windows, figures falling into the churning sea below.",
        "composition": "Extreme dynamic Dutch angle, catastrophic scale, debris and sparks flying.",
        "model": "gemini_nanobanana",
        "lighting": "Strobe-like flash of jagged lightning against storm clouds and raging fire"
    },
    "The Star": {
        "archetype": "Hope, Healing, Inspiration & Cosmic Blessing",
        "symbols": "Nude maiden kneeling by a starlit pool, pouring living water from two vessels onto earth and into water, one giant radiant eight-pointed star surrounded by seven smaller stars, sacred bird in tree.",
        "composition": "Serene nocturnal waterscape, celestial starry canopy reflecting in mirror pool.",
        "model": "flux_dev",
        "lighting": "Ethereal starlight and bioluminescent water ripples"
    },
    "The Moon": {
        "archetype": "Illusion, Intuition, Dreams & The Wild Unconscious",
        "symbols": "Full moon with dripping yods of dew, a wolf and a dog howling at the night sky, crayfish crawling from the primeval waters, winding path passing between two ominous towers into wilderness.",
        "composition": "Haunting symmetrical nocturnal landscape, distorted dreamlike depths.",
        "model": "gemini_nanobanana",
        "lighting": "Uncanny silver-green lunar luminescence casting long eerie shadows"
    },
    "The Sun": {
        "archetype": "Joy, Success, Radiant Vitality & Clarity",
        "symbols": "Massive smiling golden sun radiating straight and wavy rays, joyous child riding a gentle white horse, four tall blooming sunflowers behind a stone wall, red banner fluttering.",
        "composition": "Expansive uplifting wide shot, blinding joy and crystal clear clarity.",
        "model": "niji_6",
        "lighting": "Glorious high-noon golden brilliance, warm saturated colors"
    },
    "Judgement": {
        "archetype": "Awakening, Resurrection, Higher Calling & Liberation",
        "symbols": "Archangel Gabriel blowing a great golden horn from a cloud, banner with red cross, souls rising with arms outstretched in ecstatic rebirth from stone tombs floating on a quiet sea.",
        "composition": "Epic vertical ascent, clouds parting to reveal cosmic trumpet blast.",
        "model": "gemini_nanobanana",
        "lighting": "Heavenly golden rays breaking through grey storm clouds"
    },
    "The World": {
        "archetype": "Wholeness, Completion, Integration & Cosmic Dance",
        "symbols": "Dancing celestial figure holding two wands, framed within a lush green laurel wreath tied with red ribbons, flanked by the 4 tetramorphs (human/angel, eagle, lion, bull) in the clouds.",
        "composition": "Flawlessly centered mandala composition, floating in boundless cosmic space.",
        "model": "flux_dev",
        "lighting": "Radiant rainbow iridescence and shimmering golden starlight"
    }
}

# Suit Focus Templates for Minor Arcana
SUIT_PROFILES = {
    "Wands": {
        "element": "Fire",
        "theme": "Willpower, Passion, Ambition, Primal Energy",
        "model": "gemini_nanobanana",
        "visual_cues": "Living sprouted wooden staves with green shoots, swirling embers, flame bursts, arid mountain vistas",
        "color_palette": "Deep crimson, burning amber, volcanic charcoal, radiant brass"
    },
    "Cups": {
        "element": "Water",
        "theme": "Love, Intuition, Emotion, Mystic Dreams",
        "model": "flux_dev",
        "visual_cues": "Ornate golden chalices overflowing with living clear water, lotus blossoms, ocean tides, tranquil ponds",
        "color_palette": "Aquamarine, deep sapphire, oceanic blues, iridescent seafoam"
    },
    "Swords": {
        "element": "Air",
        "theme": "Intellect, Truth, Conflict, Strategy, Decisions",
        "model": "gemini_nanobanana",
        "visual_cues": "Double-edged gleaming steel blades, howling winds, storm clouds, shattered chains, rocky cliffs",
        "color_palette": "Steel grey, stormy slate, cold ice blue, sharp silver highlights"
    },
    "Pentacles": {
        "element": "Earth",
        "theme": "Material Wealth, Craftsmanship, Nature, Manifestation",
        "model": "flux_dev",
        "visual_cues": "Golden coins stamped with five-pointed stars, ancient oak roots, stone masonry, lush vineyards",
        "color_palette": "Rich forest greens, terrestrial umber, harvest gold, warm bronze"
    }
}

# Minor Arcana Rank Nuances
RANK_PROFILES = {
    "Ace": "A giant celestial hand emerging from clouds offering the single pristine emblem of the suit.",
    "2": "A figure contemplating two options, balancing the two forces in harmony or crossroads.",
    "3": "Collaboration, early victory, looking out over ships in harbor or crafting intricate architecture.",
    "4": "Stability, resting, consolidation of power, or defensive holding of boundaries.",
    "5": "Strife, challenge, scattering, or loss requiring resilience.",
    "6": "Victory, nostalgia, generous sharing of gifts, or smooth waters ahead.",
    "7": "Perseverance against the odds, strategic deception, or assessing long-term investment.",
    "8": "Rapid flight of arrows, swift momentum, leaving old structures behind, or master craftsmanship.",
    "9": "Wounded warrior on guard, solitary fulfillment, or anxious midnight wakefulness.",
    "10": "Overburdened labor, perfect family harmony, final ending of strife, or generational legacy.",
    "Page": "Youthful student, eager apprentice exploring the emblem with curiosity in open nature.",
    "Knight": "Dynamic mounted warrior on a galloping steed, charging into adventure or quest.",
    "Queen": "Enthroned sovereign of inward mastery, nurturing the realm with elemental grace.",
    "King": "Supreme ruler atop a carved throne, commanding the elemental domain with wise authority."
}


def get_card_recommendation(
    card_name: str,
    deck_theme: str = "",
    deck_subject: str = "",
    target_model: str = "gemini_nanobanana"
) -> dict:
    """Generate model recommendation and customized focus for any of the 78 Tarot cards."""
    # Resolve target model info
    active_model_info = MODELS.get(target_model, MODELS["gemini_nanobanana"])

    # Check if Major Arcana
    if card_name in MAJOR_ARCANA_FOCUS:
        entry = MAJOR_ARCANA_FOCUS[card_name]
        model_key = target_model if target_model in MODELS else entry.get("model", "gemini_nanobanana")
        model_info = MODELS.get(model_key, active_model_info)

        # Blend with deck theme
        theme_note = ""
        if "beaver" in deck_subject.lower() or "beaver" in deck_theme.lower():
            theme_note = " (Adapted for Terraborn Beaverfolk: incorporate woven branch armor, earthen mud-brick architecture, and druidic tooth-carved amulets)."
        elif "cyber" in deck_subject.lower() or "cyber" in deck_theme.lower():
            theme_note = " (Adapted for Cyberpunk: render traditional symbols as holographic displays, chrome implants, and cyber-relics)."

        return {
            "card_name": card_name,
            "type": "Major Arcana",
            "archetype": entry["archetype"],
            "symbols": entry["symbols"] + theme_note,
            "composition": entry["composition"],
            "lighting": entry["lighting"],
            "recommended_model": model_info["name"],
            "model_id": model_key,
            "model_badge_color": model_info["badge_color"],
            "model_badge_bg": model_info["badge_bg"],
            "model_rationale": model_info["specialty"],
            "model_guidance": model_info.get("guidance", "Portrait 2:3 Tarot Framing"),
            "is_llm": model_info.get("is_llm", True),
            "suggested_subject_focus": f"{deck_subject or 'a tarot archetype'}, {entry['symbols'].split('.')[0]}"
        }

    # Handle Minor Arcana
    suit = None
    rank = None
    for s in ["Wands", "Cups", "Swords", "Pentacles"]:
        if f" of {s}" in card_name:
            suit = s
            rank = card_name.replace(f" of {s}", "").strip()
            break

    if suit and suit in SUIT_PROFILES:
        s_profile = SUIT_PROFILES[suit]
        r_note = RANK_PROFILES.get(rank, f"Embodying the essence of {rank} in the suit of {suit}.")
        model_key = target_model if target_model in MODELS else s_profile.get("model", "gemini_nanobanana")
        model_info = MODELS.get(model_key, active_model_info)

        theme_note = ""
        if "beaver" in deck_subject.lower() or "beaver" in deck_theme.lower():
            theme_note = " Adapted for Terraborn Beavers with earthy river motifs, shaped timber, and carved stone."
        elif "cyber" in deck_subject.lower() or "cyber" in deck_theme.lower():
            theme_note = " Adapted with neon circuitry, fiber-optic filaments, and cyber-hardware."

        composition = f"Balanced 2D tarot framing. Focus on the {rank} {suit.lower()} motif: {r_note}"

        return {
            "card_name": card_name,
            "type": f"Minor Arcana ({suit})",
            "archetype": f"{rank} of {suit} - {s_profile['theme']}",
            "symbols": f"{r_note} Elemental cues: {s_profile['visual_cues']}.{theme_note}",
            "composition": composition,
            "lighting": f"{s_profile['color_palette']} color grading with rich atmospheric depth",
            "recommended_model": model_info["name"],
            "model_id": model_key,
            "model_badge_color": model_info["badge_color"],
            "model_badge_bg": model_info["badge_bg"],
            "model_rationale": model_info["specialty"],
            "model_guidance": model_info.get("guidance", "Portrait 2:3 Tarot Framing"),
            "is_llm": model_info.get("is_llm", True),
            "suggested_subject_focus": f"{deck_subject or 'a tarot subject'} manifesting the {rank} of {suit}, with {s_profile['visual_cues'].split(',')[0]}"
        }

    # Fallback generic
    model_key = target_model if target_model in MODELS else "gemini_nanobanana"
    model_info = MODELS.get(model_key, active_model_info)
    return {
        "card_name": card_name,
        "type": "Tarot Card",
        "archetype": f"The Essence of {card_name}",
        "symbols": "Central emblematic figure surrounded by traditional archetypal tarot symbols.",
        "composition": "Centered heroic composition with ornate decorative tarot framing.",
        "lighting": "Dramatic contrast with vivid illumination and rich textural atmosphere",
        "recommended_model": model_info["name"],
        "model_id": model_key,
        "model_badge_color": model_info["badge_color"],
        "model_badge_bg": model_info["badge_bg"],
        "model_rationale": model_info["specialty"],
        "model_guidance": model_info.get("guidance", "Portrait 2:3 Tarot Framing"),
        "is_llm": model_info.get("is_llm", True),
        "suggested_subject_focus": f"{deck_subject or 'a tarot figure'} representing {card_name}"
    }


def format_uniform_prompt(
    card_name: str,
    subject_description: str,
    symbols: str = "",
    composition: str = "",
    lighting: str = "",
    theme_prompt: str = "",
    model_id: str = "gemini_nanobanana"
) -> str:
    """
    Format a uniform natural language prompt tailored for the selected generator model,
    omitting arbitrary technical flags (temperature, --stylize, --cfg, etc.) for LLM models.
    """
    model_info = MODELS.get(model_id, MODELS["gemini_nanobanana"])
    is_llm = model_info.get("is_llm", True)

    parts = []
    # Header card title
    parts.append(f"A full-bleed digital tarot card illustration depicting **{card_name}**.")

    # Central subject
    if subject_description:
        parts.append(f"Central Subject: {subject_description.strip()}.")

    # Symbolic elements
    if symbols:
        parts.append(f"Symbolic Archetype & Elements: {symbols.strip()}")

    # Composition & Framing
    if composition:
        parts.append(f"Composition & Staging: {composition.strip()} Centered subject framed within an ornate decorative tarot card border.")
    else:
        parts.append("Composition & Staging: Centered 2D tarot framing enclosed in an ornate decorative border.")

    # Lighting & Color
    if lighting:
        parts.append(f"Lighting & Atmosphere: {lighting.strip()}")

    # Art style & Theme
    if theme_prompt:
        parts.append(f"Art Style & Aesthetics: {theme_prompt.strip()}")

    if not is_llm and model_id == "midjourney_v6":
        parts.append("\n--ar 2:3 --v 6.1")

    return "\n\n".join(parts)
