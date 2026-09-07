import json
import os
import sys
import time
from google import genai
from google.genai import types

# ============================================================
#  FLOWSTATE AI MOONSHOT FA AGENT
#  Evaluates moonshot candidates for narrative strength,
#  early-stage potential, and scam detection
# ============================================================


def load_moonshot_candidates():
    filepath = os.path.join(os.path.dirname(__file__), "..", "data", "moonshot_candidates.json")
    if not os.path.exists(filepath):
        print(f"[!] Error: {filepath} not found. Run the Moonshot Scanner first.")
        return []
    with open(filepath, 'r') as f:
        return json.load(f)


def run_moonshot_fa(coin, score, reasons, client):
    print(f"\n[*] Initiating Moonshot FA for {coin} (Scanner Score: {score}/100)...")
    
    prompt = f"""
    You are an expert cryptocurrency analyst specializing in early-stage, high-potential tokens.
    Your task is to evaluate '{coin}' as a potential MOONSHOT investment — a high-risk, high-reward play.
    
    Scanner data: This coin scored {score}/100 on momentum. Signals: {', '.join(reasons)}.
    
    Use Google Search to find the most recent information about this project.
    
    Evaluate on these 5 MOONSHOT-SPECIFIC criteria.
    For each, answer [YES] or [NO] with a 1-2 sentence explanation.
    
    1. **Narrative Strength**: Is this coin riding a strong, current crypto narrative?
       (AI agents, DeSci, RWA tokenization, Bitcoin L2, memecoin with utility, etc.)
       Answer [YES] if the narrative is hot RIGHT NOW, not 6 months ago.
    
    2. **Catalyst Ahead**: Is there an upcoming catalyst that could drive price?
       (Major exchange listing, protocol upgrade, airdrop, partnership announcement, etc.)
       Answer [YES] if there's a specific, identifiable catalyst in the next 1-3 months.
    
    3. **Community Signal**: Is there growing social buzz and community momentum?
       (Crypto Twitter engagement, Discord/Telegram growth, influencer attention)
       Answer [YES] if the community is actively growing, not stagnant.
    
    4. **Not a Scam**: Is this a legitimate project with identifiable builders?
       (Known team or doxxed founders, audited contracts, no rug-pull history)
       Answer [YES] if the project appears legitimate and safe.
    
    5. **Asymmetric Upside**: Does this coin have realistic 10x+ potential?
       (Low market cap relative to peers, early stage, room to grow into its narrative)
       Answer [YES] if a 10x from current levels is plausible within 6-12 months.
    
    Format your response exactly like this:
    1. [YES/NO] Explanation...
    2. [YES/NO] Explanation...
    3. [YES/NO] Explanation...
    4. [YES/NO] Explanation...
    5. [YES/NO] Explanation...
    
    Then add a final line:
    VERDICT: [MOONSHOT / PASS] - One sentence summary of your recommendation.
    """
    
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
        print(f"[!] API Error during Moonshot FA for {coin}: {str(e)}")
        return None


def parse_score(analysis_text):
    if not analysis_text:
        return 0
    score = 0
    lines = analysis_text.strip().split('\n')
    for line in lines:
        if '[YES]' in line.upper():
            score += 1
    return score


def main():
    print("=" * 60)
    print(" FLOWSTATE AI MOONSHOT FA AGENT")
    print(" Evaluating moonshot candidates for go/no-go")
    print("=" * 60)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[!] GEMINI_API_KEY environment variable is not set.")
        print("Please set it before running this script.")
        sys.exit(1)
    
    client = genai.Client()
    candidates = load_moonshot_candidates()
    
    if not candidates:
        return
    
    # Only evaluate top 5 by score
    top_candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[:5]
    print(f"[*] Evaluating top {len(top_candidates)} moonshot candidates...\n")
    
    results = []
    
    for candidate in top_candidates:
        coin = candidate["coin"]
        score = candidate["score"]
        reasons = candidate.get("reasons", [])
        
        analysis = run_moonshot_fa(coin, score, reasons, client)
        
        if analysis:
            print(f"\n{'='*40}")
            print(f" MOONSHOT FA REPORT: {coin}")
            print(f"{'='*40}")
            print(analysis)
            
            fa_score = parse_score(analysis)
            print(f"\n[*] Moonshot FA Score for {coin}: {fa_score}/5")
            
            candidate["fa_score"] = fa_score
            candidate["fa_report"] = analysis
            
            if fa_score >= 4:
                print(f"[+] {coin} — MOONSHOT CANDIDATE CONFIRMED! ({fa_score}/5)")
                results.append(candidate)
            else:
                print(f"[-] {coin} — Did not pass Moonshot FA ({fa_score}/5)")
        
        time.sleep(2)
    
    print(f"\n{'='*60}")
    print(f" MOONSHOT FA COMPLETE")
    print(f"{'='*60}")
    
    if results:
        # Sort by FA score, then scanner score
        results.sort(key=lambda x: (x["fa_score"], x["score"]), reverse=True)
        
        print(f"\n  APPROVED MOONSHOTS ({len(results)}):")
        for r in results:
            print(f"    {r['coin']:>10} | FA: {r['fa_score']}/5 | Scanner: {r['score']}/100")
        
        # Save the top pick
        output_file = os.path.join(os.path.dirname(__file__), "..", "data", "moonshot_approved.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"\n[*] Saved approved moonshots to {output_file}")
        print(f"[*] Review the reports, pick ONE, and launch with: python moonshot_launcher.py <COIN>")
    else:
        print("\n[-] No moonshot candidates passed FA this week. Patience pays.")


if __name__ == "__main__":
    main()
