import json

path = "crypto/data/moonshot_candidates.json"
with open(path) as f:
    all_candidates = json.load(f)

target = ["PENGU", "MEME", "PEOPLE"]
filtered = [c for c in all_candidates if c["coin"] in target]

coins_found = [c["coin"] for c in filtered]
print("[*] Filtered to: " + str(coins_found))

with open(path, "w") as f:
    json.dump(filtered, f, indent=4)

print("[*] moonshot_candidates.json updated — ready for FA agent")
