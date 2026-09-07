// Configure marked to use GitHub Flavored Markdown
marked.use({
  gfm: true,
  breaks: true
});

const jurisdictionSelect = document.getElementById('jurisdiction');
const modeSelect = document.getElementById('mode');
const promptInput = document.getElementById('prompt');
const disclaimerCheck = document.getElementById('disclaimer');
const submitBtn = document.getElementById('submitBtn');

const emptyState = document.getElementById('emptyState');
const loadingState = document.getElementById('loadingState');
const resultState = document.getElementById('resultState');
const contentRenderer = document.getElementById('contentRenderer');
const copyBtn = document.getElementById('copyBtn');

// ── Credit & Auth Management ──
const authModal = document.getElementById('authModal');
const authForm = document.getElementById('authForm');
const userEmailInput = document.getElementById('userEmail');
const upgradeModal = document.getElementById('upgradeModal');
const creditCountSpan = document.getElementById('creditCount');
const userEmailDisplay = document.getElementById('userEmailDisplay');

const INITIAL_LIFETIME_CREDITS = 25;

function getStoredUser() {
  const email = localStorage.getItem('socrates_user_email');
  const credits = localStorage.getItem('socrates_lifetime_credits');
  return {
    email: email || null,
    credits: credits !== null ? parseInt(credits, 10) : null
  };
}

function updateCreditDisplay() {
  const { email, credits } = getStoredUser();
  if (email) {
    authModal.classList.add('hidden');
    userEmailDisplay.textContent = email;
    const currentCredits = credits !== null ? credits : INITIAL_LIFETIME_CREDITS;
    creditCountSpan.textContent = currentCredits;
    
    if (currentCredits <= 0) {
      upgradeModal.classList.remove('hidden');
    }
  } else {
    authModal.classList.remove('hidden');
  }
}

function handleAuthSubmit() {
  const userEmailInput = document.getElementById('userEmail');
  if (!userEmailInput) return;
  const emailVal = userEmailInput.value.trim().toLowerCase();
  if (emailVal && emailVal.includes('@')) {
    localStorage.setItem('socrates_user_email', emailVal);
    if (localStorage.getItem('socrates_lifetime_credits') === null) {
      localStorage.setItem('socrates_lifetime_credits', INITIAL_LIFETIME_CREDITS.toString());
    }
    updateCreditDisplay();
  }
}

window.handleAuthSubmit = handleAuthSubmit;

if (authForm) {
  authForm.addEventListener('submit', (e) => {
    e.preventDefault();
    handleAuthSubmit();
  });
}

// Initialize on page load
updateCreditDisplay();

// ── OpenRouter → Claude 3.5 Sonnet ──
const OPENROUTER_API_KEY = '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';
const OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions';

const SOCRATES_SYSTEM_PROMPT = `You are Socrates — a virtual senior associate and research engine operating at the standard of the world's most elite law firms (AmLaw 100 calibre). You don't just retrieve information. You think, you anticipate, you draft, and you deliver output that is ready to go directly to a partner's desk or a client's inbox.

You are not a search engine. You are the associate who never sleeps, never bills for learning, and never misses an issue.

GOVERNING PRINCIPLES:
1. Precision over speed. A misplaced comma changes a contract. A miscited case loses an argument.
2. Jurisdiction before everything. Law is local. Always confirm the operative jurisdiction before analyzing anything.
3. Proactive over reactive. Flag what wasn't asked but should have been.

OPERATING RULES:
- Ask before you assume. If a critical fact is missing, identify exactly what you need before producing a conclusion.
- Acknowledge gray areas. The law is rarely binary. Present the strongest counterargument.
- Escalate appropriately. Flag genuine complexity and recommend attorney review where warranted.
- Protect privilege. Treat all matter information as attorney-client privileged.
- Do not moralize. Identify what the law requires and what the strategic options are.

Always end your output with a "Flags & Watch Items" section highlighting anything the user didn't ask about but should be aware of (limitation periods, conflicts, privilege concerns, etc.).`;

async function submitToSocrates() {
  const { email, credits } = getStoredUser();

  if (!email) {
    authModal.classList.remove('hidden');
    return;
  }

  if (credits !== null && credits <= 0) {
    upgradeModal.classList.remove('hidden');
    return;
  }

  const hasJurisdiction = jurisdictionSelect.value !== '';
  const hasPrompt = promptInput.value.trim().length > 0;
  const hasDisclaimer = disclaimerCheck.checked;

  if (!hasJurisdiction) {
    alert('Please select a Governing Jurisdiction.');
    return;
  }
  if (!hasPrompt) {
    alert('Please enter your Fact Pattern / Inquiry.');
    return;
  }
  if (!hasDisclaimer) {
    alert('Please check the box to acknowledge the disclaimer.');
    return;
  }

  // Prepare UI state
  emptyState.classList.add('hidden');
  resultState.classList.add('hidden');
  loadingState.classList.remove('hidden');
  submitBtn.disabled = true;

  try {
    const userMessage = `TARGET JURISDICTION: ${jurisdictionSelect.value}
OPERATIONAL MODE: ${modeSelect.value}

FACT PATTERN / INQUIRY:
${promptInput.value}`;

    const response = await fetch('http://127.0.0.1:8787/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jurisdiction: jurisdictionSelect.value,
        mode: modeSelect.value,
        message: promptInput.value,
        userEmail: email
      })
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`API error: ${errText}`);
    }

    const data = await response.json();
    const aiText = data?.response ?? data?.candidates?.[0]?.content?.parts?.[0]?.text ?? 'No response received.';

    // Decrement Lifetime Credit
    const currentCredits = credits !== null ? credits : INITIAL_LIFETIME_CREDITS;
    const newCredits = Math.max(0, currentCredits - 1);
    localStorage.setItem('socrates_lifetime_credits', newCredits.toString());
    updateCreditDisplay();

    // Render the markdown response
    const htmlContent = marked.parse(aiText);
    contentRenderer.innerHTML = htmlContent;

    // Show results
    loadingState.classList.add('hidden');
    resultState.classList.remove('hidden');

    // Scroll to top of output container
    document.getElementById('outputContainer').scrollTo({ top: 0, behavior: 'smooth' });

    // Re-enable button
    submitBtn.disabled = false;

  } catch (error) {
    console.error(error);
    loadingState.classList.add('hidden');
    resultState.classList.remove('hidden');
    contentRenderer.innerHTML = `
      <div class="bg-red-900/50 border-l-4 border-red-500 p-4 rounded-md">
        <h3 class="text-red-300 font-semibold mb-2">Connection Error</h3>
        <p class="text-red-200/80 text-sm">${error.message}</p>
      </div>`;
    submitBtn.disabled = false;
  }
}

submitBtn.addEventListener('click', submitToSocrates);

// ── Read Aloud (Web Speech Synthesis) ──
const readAloudBtn = document.getElementById('readAloudBtn');
const readAloudLabel = document.getElementById('readAloudLabel');
const voiceSelect = document.getElementById('voiceSelect');
let isSpeaking = false;

function resetReadAloudBtn() {
  isSpeaking = false;
  speechChunks = [];
  currentChunkIndex = 0;
  currentUtterance = null;
  readAloudLabel.textContent = 'Read Aloud';
  readAloudBtn.classList.remove('bg-red-700', 'border-red-600');
  readAloudBtn.classList.add('bg-brand-700', 'border-brand-600');
}

function populateVoiceList() {
  if (typeof speechSynthesis === 'undefined' || !voiceSelect) return;
  const voices = speechSynthesis.getVoices();
  voiceSelect.innerHTML = '';

  if (voices.length === 0) {
    const option = document.createElement('option');
    option.textContent = 'Loading/No voices...';
    option.value = '';
    voiceSelect.appendChild(option);
    return;
  }

  // Sort: en-GB first, then any en, then prioritize localService: true (offline SAPI), then alphabetical
  const sortedVoices = [...voices].sort((a, b) => {
    const aLang = a.lang.toLowerCase();
    const bLang = b.lang.toLowerCase();
    const aGB = aLang.startsWith('en-gb');
    const bGB = bLang.startsWith('en-gb');
    
    if (aGB && !bGB) return -1;
    if (!aGB && bGB) return 1;
    
    if (aGB && bGB) {
      if (a.localService && !b.localService) return -1;
      if (!a.localService && b.localService) return 1;
    }
    
    const aEN = aLang.startsWith('en');
    const bEN = bLang.startsWith('en');
    if (aEN && !bEN) return -1;
    if (!aEN && bEN) return 1;
    
    if (aEN && bEN) {
      if (a.localService && !b.localService) return -1;
      if (!a.localService && b.localService) return 1;
    }
    
    if (a.localService && !b.localService) return -1;
    if (!a.localService && b.localService) return 1;
    
    return a.name.localeCompare(b.name);
  });

  let selectedIndex = 0;
  sortedVoices.forEach((voice, index) => {
    const option = document.createElement('option');
    const typeLabel = voice.localService ? 'Offline' : 'Network';
    option.textContent = `${voice.name} (${voice.lang}) [${typeLabel}]`;
    option.value = voice.name;
    voiceSelect.appendChild(option);

    // Auto-select British voice if found (prioritizing offline ones)
    if (voice.lang.toLowerCase().startsWith('en-gb') && selectedIndex === 0) {
      selectedIndex = index;
    }
  });

  // Fallback to select the first English voice if no GB voice was found
  if (selectedIndex === 0) {
    const engIndex = sortedVoices.findIndex(v => v.lang.toLowerCase().startsWith('en'));
    if (engIndex !== -1) {
      selectedIndex = engIndex;
    }
  }

  voiceSelect.selectedIndex = selectedIndex;
}

if (typeof speechSynthesis !== 'undefined') {
  speechSynthesis.onvoiceschanged = populateVoiceList;
  // Trigger initial load
  populateVoiceList();
}

let speechChunks = [];
let currentChunkIndex = 0;
let currentUtterance = null;

function cleanTextForSpeech(text) {
  return text
    // Remove Markdown headings indicators (###, ##, #)
    .replace(/#+\s+/g, '')
    // Remove Markdown bold/italic indicators (*, **)
    .replace(/\*\*+/g, '')
    // Remove bullet points/dash prefixes at start of lines or lists
    .replace(/^\s*[-•*]\s+/gm, '')
    // Replace abbreviation periods to avoid false sentence splits
    .replace(/Mr\./gi, 'Mr')
    .replace(/Ms\./gi, 'Ms')
    .replace(/Dr\./gi, 'Dr')
    .replace(/Inc\./gi, 'Inc')
    .replace(/Ltd\./gi, 'Ltd')
    .replace(/vs\./gi, 'versus')
    .replace(/ca\./gi, 'circa')
    .replace(/e\.g\./gi, 'for example')
    .replace(/i\.e\./gi, 'that is')
    .replace(/s\.\s*(\d+)/gi, 'section $1') // s. 8 -> section 8
    .replace(/ss\.\s*(\d+)/gi, 'sections $1') // ss. 8 -> sections 8
    // Normalize quotes
    .replace(/[\u201C\u201D\u201E\u201F\u2033\u2036]/g, '"')
    .replace(/[\u2018\u2019\u201A\u201B\u2032\u2035]/g, "'")
    // Normalize spacing
    .replace(/\s+/g, ' ')
    .trim();
}

function splitTextIntoChunks(text, maxLength = 200) {
  const cleanedText = cleanTextForSpeech(text);
  
  // Split by sentence endings (., !, ?) while keeping the punctuation
  const regex = /[^.!?]+[.!?]*/g;
  const sentences = cleanedText.match(regex) || [cleanedText];
  
  const chunks = [];
  let currentChunk = '';
  
  for (const sentence of sentences) {
    if ((currentChunk + sentence).length < maxLength) {
      currentChunk += sentence;
    } else {
      if (currentChunk.trim()) {
        chunks.push(currentChunk.trim());
      }
      // If a single sentence is longer than maxLength, split by words
      if (sentence.length > maxLength) {
        const words = sentence.split(' ');
        let tempChunk = '';
        for (const word of words) {
          if ((tempChunk + ' ' + word).length < maxLength) {
            tempChunk += (tempChunk ? ' ' : '') + word;
          } else {
            if (tempChunk.trim()) chunks.push(tempChunk.trim());
            tempChunk = word;
          }
        }
        currentChunk = tempChunk;
      } else {
        currentChunk = sentence;
      }
    }
  }
  
  if (currentChunk.trim()) {
    chunks.push(currentChunk.trim());
  }
  
  return chunks;
}

function speakNextChunk() {
  if (currentChunkIndex >= speechChunks.length) {
    console.log("Finished speaking all chunks.");
    resetReadAloudBtn();
    return;
  }

  const chunkText = speechChunks[currentChunkIndex].trim();
  if (!chunkText) {
    currentChunkIndex++;
    speakNextChunk();
    return;
  }

  console.log(`Speaking chunk ${currentChunkIndex + 1}/${speechChunks.length}: "${chunkText.substring(0, 40)}..."`);
  currentUtterance = new SpeechSynthesisUtterance(chunkText);
  currentUtterance.rate = 0.9;
  currentUtterance.pitch = 0.95;
  currentUtterance.volume = 1;

  // Use voice selected in dropdown
  if (voiceSelect && voiceSelect.value) {
    const voices = window.speechSynthesis.getVoices();
    const selectedVoice = voices.find(v => v.name === voiceSelect.value);
    if (selectedVoice) {
      currentUtterance.voice = selectedVoice;
      currentUtterance.lang = selectedVoice.lang;
    }
  }

  currentUtterance.onend = () => {
    // Only proceed to next if we are still in speaking state
    if (isSpeaking) {
      currentChunkIndex++;
      speakNextChunk();
    }
  };

  currentUtterance.onerror = (e) => {
    console.error("Speech synthesis chunk error:", e);
    
    if (!isSpeaking) {
      return;
    }
    
    // If interrupted unexpectedly during startup, retry speaking this chunk after a short delay
    if (e.error === 'interrupted') {
      console.log(`Utterance interrupted. Retrying chunk ${currentChunkIndex + 1} in 150ms...`);
      setTimeout(() => {
        if (isSpeaking) speakNextChunk();
      }, 150);
      return;
    }
    
    if (e.error === 'canceled') {
      resetReadAloudBtn();
      return;
    }
    
    // For other errors, skip and continue
    currentChunkIndex++;
    speakNextChunk();
  };

  window.speechSynthesis.speak(currentUtterance);
}

readAloudBtn.addEventListener('click', () => {
  if (isSpeaking) {
    console.log("Stopping active speech synthesis.");
    isSpeaking = false; // block further callbacks
    window.speechSynthesis.cancel();
    resetReadAloudBtn();
    return;
  }

  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = contentRenderer.innerHTML;
  const plainText = tempDiv.innerText;
  if (!plainText.trim()) {
    console.warn("Read aloud triggered, but content renderer is empty.");
    return;
  }

  console.log("Initializing SpeechSynthesisUtterance chunks...");
  speechChunks = splitTextIntoChunks(plainText, 200);
  currentChunkIndex = 0;

  if (speechChunks.length === 0) {
    return;
  }

  isSpeaking = true;
  readAloudLabel.textContent = 'Stop Reading';
  readAloudBtn.classList.remove('bg-brand-700', 'border-brand-600');
  readAloudBtn.classList.add('bg-red-700', 'border-red-600');

  // Cancel any ongoing speech to start fresh, with settlement safety timeout
  if (window.speechSynthesis.speaking) {
    console.log("Active speaking detected. Cancelling before restart...");
    window.speechSynthesis.cancel();
    setTimeout(() => {
      if (isSpeaking) speakNextChunk();
    }, 250);
  } else {
    speakNextChunk();
  }
});

// Copy to clipboard functionality
copyBtn.addEventListener('click', async () => {
  try {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = contentRenderer.innerHTML;
    const plainText = tempDiv.innerText;

    await navigator.clipboard.writeText(plainText);

    const originalText = copyBtn.innerHTML;
    copyBtn.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-400" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
      </svg>
      <span class="text-emerald-400">Copied!</span>`;
    setTimeout(() => {
      copyBtn.innerHTML = originalText;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy text: ', err);
  }
});
