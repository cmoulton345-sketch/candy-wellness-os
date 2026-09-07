import json
import os
import sys
import time
from google import genai
from google.genai import types


def load_qualified_pairs():
    filepath = os.path.join(os.path.dirname(__file__), "..", "data", "qualified_pairs.json")
    if not os.path.exists(filepath):
        print(f"[!] Error: {filepath} not found. Run the Scanner first.")
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

def load_regime():
    filepath = os.path.join(os.path.dirname(__file__), "..", "data", "market_regime.json")
    if not os.path.exists(filepath):
        print("[!] No regime file found. Defaulting to BULL.")
        return "BULL"
    with open(filepath, 'r') as f:
        return json.load(f).get("regime", "BULL")

def get_regime_prompt(coin, regime):
    base = f"""
    You are an expert cryptocurrency fundamental analyst.
    Your task is to research the crypto token '{coin}' (which trades on Hyperliquid as a perpetual contract).
    Use Google Search to find the most recent, up-to-date information about this project from the last few months.
    """
    
    if regime == "BULL":
        return base + """
    Evaluate the token based on the following 5 strict criteria for a LONG swing trade.
    For each criterion, start your response with exactly [YES] or [NO], followed by a 1-2 sentence explanation.
    
    1. Utility: Does this project have a live, working product or a demonstrable use case?
    2. Development: Has there been active development or significant ecosystem news in the last 3-6 months?
    3. Traction: Is there proof of real user adoption (e.g., TVL, active users, or major partnerships)?
    4. Safety: Is the project free of major warning signs (recent hacks, regulatory lawsuits, or rug-pull history)? Answer [YES] if safe.
    5. Tokenomics: Is the token reasonably distributed (not heavily centralized with VCs holding 80%+ ready to dump)?
    
    Format exactly:
    1. [YES/NO] Explanation...
    2. [YES/NO] Explanation...
    3. [YES/NO] Explanation...
    4. [YES/NO] Explanation...
    5. [YES/NO] Explanation...
    """
    elif regime == "CHOP":
        return base + """
    The market is in a CHOP (sideways) regime. We are doing a short-term mechanical range trade.
    Long-term fundamentals do not matter, only immediate existential threats matter.
    Evaluate the token based on this 1 strict criterion.
    Start your response with exactly [YES] or [NO].
    
    1. Safety: Is the project free of IMMEDIATE existential threats? You MUST check for and explicitly rule out: active SEC lawsuits, imminent massive VC token unlocks, or major exchange delisting notices. Answer [YES] if it is clear of these threats, [NO] if any of these threats exist.
    
    Format exactly:
    1. [YES/NO] Explanation...
    """
    elif regime == "BEAR":
        return base + """
    The market is in a BEAR (downtrend) regime. We are looking to SHORT SELL this token.
    We WANT terrible fundamentals to confirm the short thesis.
    Evaluate the token based on the following 5 strict criteria for a SHORT trade.
    For each criterion, answer [YES] if the token is BAD/WEAK, and [NO] if the token is strong.
    
    1. No Utility: Is the project essentially useless, a pure meme, or vaporware without a working product? (Answer [YES] if useless).
    2. Dead Project: Is development dead or stagnant (no recent updates)? (Answer [YES] if dead).
    3. No Traction: Are users abandoning it or is TVL dropping? (Answer [YES] if dropping/low).
    4. Regulatory/Security Risk: Are there active lawsuits, recent hacks, or major FUD? (Answer [YES] if risky).
    5. Predatory Tokenomics: Do insiders/VCs control a massive supply that is currently unlocking or about to dump? (Answer [YES] if predatory).
    
    Format exactly:
    1. [YES/NO] Explanation...
    2. [YES/NO] Explanation...
    3. [YES/NO] Explanation...
    4. [YES/NO] Explanation...
    5. [YES/NO] Explanation...
    """

def run_fa_analysis(coin, client, regime):
    print(f"\n[*] Initiating Fundamental Analysis for {coin} ({regime} Mode)...")
    prompt = get_regime_prompt(coin, regime)
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=0.2
            )
        )
        return response.text
    except Exception as e:
        print(f"[!] API Error during FA for {coin}: {str(e)}")
        return None

def parse_score(analysis_text):
    if not analysis_text: return 0
    score = 0
    lines = analysis_text.strip().split('\n')
    for line in lines:
        if '[YES]' in line.upper():
            score += 1
    return score

def main():
    print("="*60)
    print(" AUTOMATED FUNDAMENTAL ANALYSIS (FA) AGENT")
    print("="*60)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[!] GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)
        
    client = genai.Client()
    qualified_pairs = load_qualified_pairs()
    regime = load_regime()
    
    print(f"[*] Current Market Regime: {regime}")
    
    if not qualified_pairs:
        return
        
    print(f"[*] Found {len(qualified_pairs)} pairs to analyze.")
    final_approved_pairs = []
    
    # Passing score thresholds based on regime
    pass_threshold = 4 if regime == "BULL" else (1 if regime == "CHOP" else 2)
    
    for pair in qualified_pairs:
        coin = pair['coin']
        analysis = run_fa_analysis(coin, client, regime)
        
        if analysis:
            print(f"\n--- FA REPORT: {coin} ---")
            print(analysis)
            print("-------------------------")
            
            score = parse_score(analysis)
            print(f"[*] Total FA Score for {coin}: {score}")
            
            if score >= pass_threshold:
                print(f"[+] {coin} PASSED the FA Rubric for {regime} mode!")
                pair['fa_score'] = score
                pair['fa_report'] = analysis
                final_approved_pairs.append(pair)
            else:
                print(f"[-] {coin} FAILED the FA Rubric for {regime} mode. (Needs {pass_threshold}, got {score})")
                
        time.sleep(2)
        
    print("\n" + "="*60)
    print(f" FA COMPLETE. {len(final_approved_pairs)} pairs approved.")
    print("="*60)
    
    if final_approved_pairs:
        output_file = os.path.join(os.path.dirname(__file__), "..", "data", "fa_approved_pairs.json")
        with open(output_file, 'w') as f:
            json.dump(final_approved_pairs, f, indent=4)
        print(f"[*] Saved final approved pairs to {output_file}")
    else:
        print("[-] No pairs passed the FA rubric today.")

if __name__ == "__main__":
    main()
