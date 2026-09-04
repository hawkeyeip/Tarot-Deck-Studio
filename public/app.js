/**
 * app.js - Tarot Deck Studio Client Logic
 */

// Theme Presets for Deck Creator
const THEME_PRESETS = {
  diablo: {
    name: "Diablo & WoW Terraborn Beavers",
    subject: "a Terraborn Beaver hero",
    template: `A masterpiece digital illustration of a tarot card representing **{card_name}**. The central subject is {subject_description}. 

Art Style & Theme: A fusion of dark, gothic grimdark atmosphere (Diablo) and bold, stylized heroic fantasy with oversized, intricate armor (World of Warcraft). Include visual motifs of "Terraborn Beavers"—nature-attuned, earth-shaping humanoid beaver-folk with druidic or shamanistic elements. 

Consistent Formatting: Flat 2D tarot layout, perfectly centered composition. The character is framed within a highly ornate, weathered metallic border featuring dark fantasy gothic architecture and geometric Terraborn earth-runes. 

Lighting & Color: Unified color grading using deep crimsons, shadowy blacks, earthy terrestrial browns, and glowing magical accents. Dramatic rim lighting, striking shadows, high contrast, sharp details, fantasy concept art style.`
  },
  cyberpunk: {
    name: "Cyberpunk 2099 Oracle",
    subject: "a cybernetically augmented operative",
    template: `A cinematic masterpiece digital tarot card illustrating **{card_name}**. The central figure is {subject_description}.

Art Style & Theme: High-tech low-life cyberpunk aesthetic, glowing holographic cyber-tattoos, reflective chrome prosthetics, and neon-lit rainy megacity alleys.

Consistent Formatting: Vertical 2D tarot frame surrounded by sleek holographic HUD borders and luminous cybernetic circuit glyphs.

Lighting & Color: Volumetric neon lighting, rich obsidian blacks, electric cyan, vibrant magenta, and amber warnings. Sharp edge reflections and photorealistic reflections.`
  },
  gothic: {
    name: "Victorian Eldritch Tarot",
    subject: "a Victorian mystic scholar",
    template: `An evocative dark fantasy tarot card representing **{card_name}**. The focal subject is {subject_description}.

Art Style & Theme: Victorian gothic horror infused with subtle eldritch cosmic mystery. Ornate antique textures, oil painting style reminiscent of classical romanticism.

Consistent Formatting: Antique tarot parchment bordered with intricately carved blackened silver vines and arcane astrological sigils.

Lighting & Color: Chiaroscuro candlelight, deep Prussian blues, tarnished golds, and deep burgundy accents.`
  },
  solarpunk: {
    name: "Solarpunk Druidic Deck",
    subject: "a solar druid botanist",
    template: `A lush, radiant tarot card illustration of **{card_name}**. The central subject is {subject_description}.

Art Style & Theme: Optimistic solarpunk aesthetic harmonizing organic flora with brass clockwork automatons, stained-glass solar collectors, and clean architectural arches.

Consistent Formatting: Elegant art-deco arched tarot border accented with blossoming vines, sunburst motifs, and polished brass filigree.

Lighting & Color: Golden hour sunlight, rich emerald greens, warm terracotta, polished bronze, and radiant golden lens flares.`
  },
  artnouveau: {
    name: "Art Nouveau Gilded Tarot",
    subject: "an allegorical celestial maiden",
    template: `A magnificent Art Nouveau illustration representing the tarot archetype **{card_name}**. The subject is {subject_description}.

Art Style & Theme: Alphonse Mucha inspired aesthetic, elegant flowing whiplash linework, botanical tendrils, and decorative mosaic backdrops.

Consistent Formatting: Classic vintage French lithograph poster layout, embellished with circular floral aureoles and embossed gold foil ornamental borders.

Lighting & Color: Pastel jewel tones, antique gold leaf, muted sage, lavender, and delicate parchment highlights.`
  }
};

let currentDeckData = null;
let currentFilter = "all";
let currentSearch = "";

// DOM Elements
const deckSelect = document.getElementById("deckSelect");
const btnNewDeck = document.getElementById("btnNewDeck");
const cardsGrid = document.getElementById("cardsGrid");
const searchInput = document.getElementById("searchInput");
const filterTabs = document.getElementById("filterTabs");
const completionBanner = document.getElementById("completionBanner");

// Focus Panel Elements
const focusCardTitle = document.getElementById("focusCardTitle");
const focusSubject = document.getElementById("focusSubject");
const focusPromptText = document.getElementById("focusPromptText");
const focusArcanaBadge = document.getElementById("focusArcanaBadge");
const btnCopyFocusPrompt = document.getElementById("btnCopyFocusPrompt");
const btnCompleteFocusCard = document.getElementById("btnCompleteFocusCard");
const btnEditFocusCard = document.getElementById("btnEditFocusCard");

// Stats Elements
const statPercentage = document.getElementById("statPercentage");
const progressRingCircle = document.getElementById("progressRingCircle");
const statCardRatio = document.getElementById("statCardRatio");
const statMajorRatio = document.getElementById("statMajorRatio");
const statMinorRatio = document.getElementById("statMinorRatio");
const barMajor = document.getElementById("barMajor");
const barMinor = document.getElementById("barMinor");
const countPending = document.getElementById("countPending");
const countComplete = document.getElementById("countComplete");
const btnResetDeck = document.getElementById("btnResetDeck");

// Modals
const newDeckModal = document.getElementById("newDeckModal");
const btnCloseModal = document.getElementById("btnCloseModal");
const btnCancelNewDeck = document.getElementById("btnCancelNewDeck");
const newDeckForm = document.getElementById("newDeckForm");
const presetSelect = document.getElementById("presetSelect");
const templateInput = document.getElementById("templateInput");
const defaultSubjectInput = document.getElementById("defaultSubjectInput");
const deckNameInput = document.getElementById("deckNameInput");
const deckIdInput = document.getElementById("deckIdInput");

// Inspect Modal
const cardInspectModal = document.getElementById("cardInspectModal");
const btnCloseInspectModal = document.getElementById("btnCloseInspectModal");
const inspectCardName = document.getElementById("inspectCardName");
const inspectClassification = document.getElementById("inspectClassification");
const inspectSubjectInput = document.getElementById("inspectSubjectInput");
const inspectImageInput = document.getElementById("inspectImageInput");
const inspectPromptDisplay = document.getElementById("inspectPromptDisplay");
const btnCopyInspectPrompt = document.getElementById("btnCopyInspectPrompt");
const btnSaveCardDetails = document.getElementById("btnSaveCardDetails");

// Recommendation Elements
const focusRecommendationCard = document.getElementById("focusRecommendationCard");
const focusModelBadge = document.getElementById("focusModelBadge");
const focusModelSpecialty = document.getElementById("focusModelSpecialty");
const focusModelSettings = document.getElementById("focusModelSettings");
const focusArchetype = document.getElementById("focusArchetype");
const focusComposition = document.getElementById("focusComposition");
const btnApplyFocus = document.getElementById("btnApplyFocus");

const inspectRecommendationBox = document.getElementById("inspectRecommendationBox");
const inspectModelBadge = document.getElementById("inspectModelBadge");
const inspectModelText = document.getElementById("inspectModelText");
const inspectSymbolsText = document.getElementById("inspectSymbolsText");
const inspectCompositionText = document.getElementById("inspectCompositionText");
const btnApplyInspectFocus = document.getElementById("btnApplyInspectFocus");

let inspectingCardName = null;

// ==========================================================================
// API & DATA FETCHING
// ==========================================================================

async function fetchDecks() {
  try {
    const res = await fetch("/api/decks");
    const data = await res.json();

    deckSelect.innerHTML = "";
    data.decks.forEach(deck => {
      const opt = document.createElement("option");
      opt.value = deck.id;
      opt.textContent = `${deck.name} (${deck.completed}/${deck.total} - ${deck.percentage}%)`;
      deckSelect.appendChild(opt);
    });

    const activeId = data.active_deck || (data.decks[0] ? data.decks[0].id : "diablo_beavers");
    deckSelect.value = activeId;
    loadDeck(activeId);
  } catch (err) {
    showToast("Failed to load decks: " + err.message);
  }
}

async function loadDeck(deckId) {
  try {
    const res = await fetch(`/api/decks/${encodeURIComponent(deckId)}`);
    if (!res.ok) throw new Error("Could not fetch deck");
    currentDeckData = await res.json();

    renderFocusCard();
    renderStats();
    renderCardsGrid();
  } catch (err) {
    showToast("Error loading deck: " + err.message);
  }
}

// ==========================================================================
// RENDERING
// ==========================================================================

function renderFocusCard() {
  if (!currentDeckData) return;
  const next = currentDeckData.next_card;

  if (!next) {
    focusCardTitle.textContent = "All 78 Cards Completed!";
    focusSubject.textContent = "You have generated every single card in this deck!";
    focusPromptText.textContent = "Congratulations! You can review or re-generate individual cards below, or build another deck idea.";
    focusArcanaBadge.textContent = "Complete";
    btnCompleteFocusCard.classList.add("hidden");
    btnCopyFocusPrompt.classList.add("hidden");
    btnEditFocusCard.classList.add("hidden");
    if (focusRecommendationCard) focusRecommendationCard.classList.add("hidden");
    return;
  }

  btnCompleteFocusCard.classList.remove("hidden");
  btnCopyFocusPrompt.classList.remove("hidden");
  btnEditFocusCard.classList.remove("hidden");

  focusCardTitle.textContent = next.name;
  focusSubject.textContent = `Subject: ${next.data.subject || currentDeckData.default_subject}`;
  focusPromptText.textContent = next.prompt;
  focusArcanaBadge.textContent = next.data.arcana === "major" ? "Major Arcana" : (next.data.suit || "Minor Arcana");

  // Render Recommendation Card
  const rec = next.recommendation;
  if (rec && focusRecommendationCard) {
    focusRecommendationCard.classList.remove("hidden");
    focusModelBadge.textContent = rec.recommended_model;
    focusModelBadge.style.color = rec.model_badge_color;
    focusModelBadge.style.background = rec.model_badge_bg;
    focusModelBadge.style.borderColor = rec.model_badge_color;

    focusModelSpecialty.textContent = rec.model_rationale;
    focusModelSettings.textContent = rec.recommended_settings;
    focusArchetype.textContent = `${rec.archetype} — ${rec.symbols}`;
    focusComposition.textContent = `${rec.composition} | Lighting: ${rec.lighting}`;
  } else if (focusRecommendationCard) {
    focusRecommendationCard.classList.add("hidden");
  }
}

function renderStats() {
  if (!currentDeckData) return;
  const { completed, total, percentage, major_completed, major_total, minor_completed, minor_total } = currentDeckData;

  // Percentage & Circular Ring
  statPercentage.textContent = `${Math.round(percentage)}%`;
  const circumference = 2 * Math.PI * 54; // r=54 -> ~339.29
  const offset = circumference - (percentage / 100) * circumference;
  progressRingCircle.style.strokeDashoffset = offset;

  // Count ratios
  statCardRatio.textContent = `${completed} / ${total}`;
  statMajorRatio.textContent = `${major_completed} / ${major_total}`;
  statMinorRatio.textContent = `${minor_completed} / ${minor_total}`;

  barMajor.style.width = `${(major_completed / major_total) * 100}%`;
  barMinor.style.width = `${(minor_completed / minor_total) * 100}%`;

  countPending.textContent = total - completed;
  countComplete.textContent = completed;

  // Celebration banner
  if (completed === total && total > 0) {
    completionBanner.classList.remove("hidden");
  } else {
    completionBanner.classList.add("hidden");
  }
}

function renderCardsGrid() {
  if (!currentDeckData) return;
  cardsGrid.innerHTML = "";

  const query = currentSearch.trim().toLowerCase();
  const template = currentDeckData.template;
  const defaultSubj = currentDeckData.default_subject;

  let visibleCards = Object.entries(currentDeckData.cards).filter(([name, data]) => {
    // Suit/Category Filter
    if (currentFilter === "pending" && data.status !== "pending") return false;
    if (currentFilter === "complete" && data.status !== "complete") return false;
    if (currentFilter === "Major Arcana" && data.arcana !== "major") return false;
    if (["Wands", "Cups", "Swords", "Pentacles"].includes(currentFilter) && data.suit !== currentFilter) return false;

    // Search Query
    if (query) {
      const matchName = name.toLowerCase().includes(query);
      const matchSubj = (data.subject || "").toLowerCase().includes(query);
      const matchSuit = (data.suit || "").toLowerCase().includes(query);
      if (!matchName && !matchSubj && !matchSuit) return false;
    }

    return true;
  });

  if (visibleCards.length === 0) {
    cardsGrid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 48px; color: var(--text-muted);">
      No cards match your filter criteria.
    </div>`;
    return;
  }

  visibleCards.forEach(([cardName, cardData]) => {
    const isComplete = cardData.status === "complete";
    const subject = cardData.subject || defaultSubj;
    const prompt = template.replace(/{card_name}/g, cardName).replace(/{subject_description}/g, subject);

    const cardEl = document.createElement("div");
    cardEl.className = `tarot-card ${isComplete ? "is-complete" : ""}`;

    const rec = currentDeckData.recommendations ? currentDeckData.recommendations[cardName] : null;
    const modelBadgeHtml = rec ? `<span class="badge" style="font-size: 9px; padding: 2px 6px; color: ${rec.model_badge_color}; background: ${rec.model_badge_bg}; border: 1px solid ${rec.model_badge_color}55;">${rec.recommended_model.split(" ")[0]}</span>` : "";

    cardEl.innerHTML = `
      <div class="card-top">
        <span class="card-arcana-tag">${cardData.suit || (cardData.arcana === "major" ? "Major Arcana" : "Minor")}</span>
        <div style="display: flex; gap: 6px; align-items: center;">
          ${modelBadgeHtml}
          <span class="badge badge-status ${isComplete ? "status-complete" : "status-pending"}">
            ${isComplete ? "✓ DONE" : "PENDING"}
          </span>
        </div>
      </div>

      ${cardData.image_url ? `<div class="card-image-preview" style="background-image: url('${cardData.image_url}')"></div>` : ""}

      <h3 class="card-title-h3">${cardName}</h3>
      <p class="card-subject-p">${subject}</p>

      <div class="card-footer-actions">
        <button class="btn-card-action btn-copy" title="Copy formatted prompt to clipboard">
          📋 Prompt
        </button>
        <button class="btn-card-action btn-inspect" title="Customize card subject or view details">
          ⚙ Edit
        </button>
        <button class="btn-toggle-check" title="Toggle card complete/pending">
          ✓
        </button>
      </div>
    `;

    // Event Handlers for Card Card
    const btnCopy = cardEl.querySelector(".btn-copy");
    btnCopy.addEventListener("click", (e) => {
      e.stopPropagation();
      copyToClipboard(prompt, `Prompt copied for ${cardName}!`);
    });

    const btnInspect = cardEl.querySelector(".btn-inspect");
    btnInspect.addEventListener("click", (e) => {
      e.stopPropagation();
      openInspectModal(cardName, cardData, prompt);
    });

    const btnToggle = cardEl.querySelector(".btn-toggle-check");
    btnToggle.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleCardStatus(cardName, isComplete ? "pending" : "complete");
    });

    cardsGrid.appendChild(cardEl);
  });
}

// ==========================================================================
// CARD STATUS & ACTIONS
// ==========================================================================

async function toggleCardStatus(cardName, newStatus) {
  try {
    const res = await fetch("/api/cards/toggle", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        deck_id: currentDeckData.id,
        card_name: cardName,
        status: newStatus
      })
    });
    if (!res.ok) throw new Error("Failed to update status");
    
    // Refresh deck data
    await loadDeck(currentDeckData.id);
    showToast(`${cardName} marked as ${newStatus}!`);
  } catch (err) {
    showToast("Error updating card: " + err.message);
  }
}

function copyToClipboard(text, successMsg = "Copied to clipboard!") {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => {
      showToast(successMsg);
    }).catch(() => fallbackCopy(text, successMsg));
  } else {
    fallbackCopy(text, successMsg);
  }
}

function fallbackCopy(text, successMsg) {
  const ta = document.createElement("textarea");
  ta.value = text;
  document.body.appendChild(ta);
  ta.select();
  document.execCommand("copy");
  document.body.removeChild(ta);
  showToast(successMsg);
}

function showToast(message) {
  const container = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerHTML = `<span>✦</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(10px)";
    setTimeout(() => toast.remove(), 300);
  }, 2600);
}

// ==========================================================================
// MODAL HANDLERS
// ==========================================================================

// New Deck Modal
btnNewDeck.addEventListener("click", () => {
  newDeckModal.classList.remove("hidden");
  deckIdInput.value = "";
  deckNameInput.value = "";
  defaultSubjectInput.value = "";
  templateInput.value = THEME_PRESETS.diablo.template;
  presetSelect.value = "diablo";
});

btnCloseModal.addEventListener("click", () => newDeckModal.classList.add("hidden"));
btnCancelNewDeck.addEventListener("click", () => newDeckModal.classList.add("hidden"));

presetSelect.addEventListener("change", () => {
  const val = presetSelect.value;
  if (THEME_PRESETS[val]) {
    const preset = THEME_PRESETS[val];
    templateInput.value = preset.template;
    if (!defaultSubjectInput.value) defaultSubjectInput.value = preset.subject;
    if (!deckNameInput.value) deckNameInput.value = preset.name;
    if (!deckIdInput.value) deckIdInput.value = val + "_tarot";
  }
});

newDeckForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = deckIdInput.value.trim().toLowerCase().replace(/[^a-z0-9_\-]/g, "_");
  const name = deckNameInput.value.trim();
  const subject = defaultSubjectInput.value.trim();
  const template = templateInput.value.trim();

  try {
    const res = await fetch("/api/decks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, name, subject, template })
    });
    const result = await res.json();
    if (!res.ok) throw new Error(result.error || "Failed to create deck");

    newDeckModal.classList.add("hidden");
    showToast(`Deck '${name}' successfully created!`);
    await fetchDecks();
    deckSelect.value = id;
    loadDeck(id);
  } catch (err) {
    showToast("Error: " + err.message);
  }
});

// Card Inspector Modal
function openInspectModal(cardName, cardData, prompt) {
  inspectingCardName = cardName;
  inspectCardName.textContent = cardName;
  inspectClassification.textContent = cardData.suit || (cardData.arcana === "major" ? "Major Arcana" : "Minor Arcana");
  inspectSubjectInput.value = cardData.subject || currentDeckData.default_subject;
  inspectImageInput.value = cardData.image_url || "";
  inspectPromptDisplay.textContent = prompt;

  const rec = currentDeckData.recommendations ? currentDeckData.recommendations[cardName] : null;
  if (rec && inspectRecommendationBox) {
    inspectRecommendationBox.classList.remove("hidden");
    inspectModelBadge.textContent = rec.recommended_model;
    inspectModelBadge.style.color = rec.model_badge_color;
    inspectModelBadge.style.background = rec.model_badge_bg;
    inspectModelBadge.style.borderColor = rec.model_badge_color;

    inspectModelText.textContent = `${rec.recommended_model} (${rec.recommended_settings}) — ${rec.model_rationale}`;
    inspectSymbolsText.textContent = `${rec.archetype}: ${rec.symbols}`;
    inspectCompositionText.textContent = `${rec.composition} | Lighting: ${rec.lighting}`;

    btnApplyInspectFocus.onclick = () => {
      inspectSubjectInput.value = rec.suggested_subject_focus;
      // Also update prompt preview live
      const newPrompt = currentDeckData.template
        .replace(/{card_name}/g, cardName)
        .replace(/{subject_description}/g, rec.suggested_subject_focus);
      inspectPromptDisplay.textContent = newPrompt;
      showToast(`Applied archetype focus to subject input!`);
    };
  } else if (inspectRecommendationBox) {
    inspectRecommendationBox.classList.add("hidden");
  }

  cardInspectModal.classList.remove("hidden");
}

btnCloseInspectModal.addEventListener("click", () => cardInspectModal.classList.add("hidden"));

btnCopyInspectPrompt.addEventListener("click", () => {
  copyToClipboard(inspectPromptDisplay.textContent, `Prompt copied for ${inspectingCardName}!`);
});

btnSaveCardDetails.addEventListener("click", async () => {
  if (!inspectingCardName || !currentDeckData) return;
  const newSubject = inspectSubjectInput.value.trim();
  const newImageUrl = inspectImageInput.value.trim();

  try {
    const res = await fetch("/api/cards/update", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        deck_id: currentDeckData.id,
        card_name: inspectingCardName,
        subject: newSubject,
        image_url: newImageUrl
      })
    });
    if (!res.ok) throw new Error("Could not update card");

    cardInspectModal.classList.add("hidden");
    showToast(`Updated details for ${inspectingCardName}`);
    loadDeck(currentDeckData.id);
  } catch (err) {
    showToast("Error: " + err.message);
  }
});

// ==========================================================================
// TOP FOCUS BUTTONS & LISTENERS
// ==========================================================================

btnCopyFocusPrompt.addEventListener("click", () => {
  if (currentDeckData && currentDeckData.next_card) {
    copyToClipboard(currentDeckData.next_card.prompt, `Prompt copied for ${currentDeckData.next_card.name}!`);
  }
});

btnApplyFocus.addEventListener("click", async () => {
  if (!currentDeckData || !currentDeckData.next_card) return;
  const next = currentDeckData.next_card;
  try {
    const res = await fetch("/api/cards/apply_focus", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        deck_id: currentDeckData.id,
        card_name: next.name
      })
    });
    if (!res.ok) throw new Error("Could not apply focus");
    showToast(`Injected recommended focus into prompt for ${next.name}!`);
    await loadDeck(currentDeckData.id);
  } catch (err) {
    showToast("Error: " + err.message);
  }
});

btnCompleteFocusCard.addEventListener("click", () => {
  if (currentDeckData && currentDeckData.next_card) {
    toggleCardStatus(currentDeckData.next_card.name, "complete");
  }
});

btnEditFocusCard.addEventListener("click", () => {
  if (currentDeckData && currentDeckData.next_card) {
    const next = currentDeckData.next_card;
    openInspectModal(next.name, next.data, next.prompt);
  }
});

// Reset Deck Listener
btnResetDeck.addEventListener("click", async () => {
  if (!confirm(`Are you sure you want to reset all cards in '${currentDeckData.name}' to incomplete?`)) return;

  try {
    const res = await fetch("/api/decks/reset", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ deck_id: currentDeckData.id })
    });
    if (!res.ok) throw new Error("Reset failed");
    showToast(`Deck '${currentDeckData.name}' reset to 0% completed.`);
    loadDeck(currentDeckData.id);
  } catch (err) {
    showToast("Error resetting deck: " + err.message);
  }
});

// Deck Selector Change
deckSelect.addEventListener("change", () => {
  const selected = deckSelect.value;
  // Set active deck on backend
  fetch("/api/active_deck", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: selected })
  });
  loadDeck(selected);
});

// Search Input Listener
searchInput.addEventListener("input", (e) => {
  currentSearch = e.target.value;
  renderCardsGrid();
});

// Filter Tabs Listener
filterTabs.addEventListener("click", (e) => {
  if (e.target.classList.contains("filter-tab")) {
    document.querySelectorAll(".filter-tab").forEach(tab => tab.classList.remove("active"));
    e.target.classList.add("active");
    currentFilter = e.target.getAttribute("data-filter");
    renderCardsGrid();
  }
});

// Initial boot
window.addEventListener("DOMContentLoaded", () => {
  fetchDecks();
});
