#!/usr/bin/env python3
"""
validate_roster.py — MECE Agent OS Roster Validator
====================================================
Checks every active file in .agent/rules/ for structural integrity:
  (a) `---` is line 1 with valid YAML frontmatter
  (b) No duplicate Session Behavior or self-intro blocks
  (c) Zero references to archived persona names
  (d) No references to memory.md
  (e) No self-naming clauses in agent files
  (f) Frontmatter has required fields (trigger, description, inherits)

Usage:
  python .agent/evals/validate_roster.py
  python .agent/evals/validate_roster.py --verbose
"""

import os
import sys
import re
import yaml
from pathlib import Path

# ============================================================
# Configuration
# ============================================================

RULES_DIR = Path(__file__).resolve().parent.parent / "rules"

# Archived persona names that should NOT appear as routing targets
ARCHIVED_NAMES = [
    "Nate", "Atlas", "Brunsen", "Clarity", "Jeeves", "Collect",
    "Chairman", "Uncle G", "Stephen", "Navigator", "Keller", "Web Builder"
]

# Required frontmatter fields
REQUIRED_FM_FIELDS = {"trigger", "description", "inherits"}

# Files exempt from certain checks
EXEMPT_FROM_FM_FIELDS = {"core_axioms.md", "factory_protocol.md"}

VERBOSE = "--verbose" in sys.argv

# ============================================================
# Test Functions
# ============================================================

class ValidationResult:
    def __init__(self):
        self.passes = []
        self.failures = []
    
    def add_pass(self, file, check, detail=""):
        self.passes.append((file, check, detail))
    
    def add_fail(self, file, check, detail):
        self.failures.append((file, check, detail))
    
    def summary(self):
        total = len(self.passes) + len(self.failures)
        return f"{len(self.passes)} passed, {len(self.failures)} failed, {total} total"


def get_active_files():
    """Get all .md files in rules dir, excluding _archive directory."""
    files = []
    for f in sorted(RULES_DIR.iterdir()):
        if f.is_file() and f.suffix == '.md' and f.name != '_archive':
            files.append(f)
    return files


def check_frontmatter(filepath, results):
    """Check (a): --- is line 1, valid YAML frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    lines = [l.rstrip('\r') for l in lines]
    
    # Check line 1 is ---
    if not lines or lines[0].strip() != '---':
        results.add_fail(filepath.name, "frontmatter", f"Line 1 is '{lines[0].strip()}' instead of '---'")
        return
    
    # Find closing ---
    fm_end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            fm_end = i
            break
    
    if fm_end is None:
        results.add_fail(filepath.name, "frontmatter", "No closing --- found for frontmatter")
        return
    
    # Parse YAML
    fm_text = '\n'.join(lines[1:fm_end])
    try:
        fm_data = yaml.safe_load(fm_text)
        if not isinstance(fm_data, dict):
            results.add_fail(filepath.name, "frontmatter", "Frontmatter is not a valid YAML mapping")
            return
    except yaml.YAMLError as e:
        results.add_fail(filepath.name, "frontmatter", f"Invalid YAML: {e}")
        return
    
    results.add_pass(filepath.name, "frontmatter", f"Valid YAML with {len(fm_data)} fields")
    
    # Check required fields
    if filepath.name not in EXEMPT_FROM_FM_FIELDS:
        missing = REQUIRED_FM_FIELDS - set(fm_data.keys())
        if missing:
            results.add_fail(filepath.name, "fm_fields", f"Missing required fields: {missing}")
        else:
            results.add_pass(filepath.name, "fm_fields", "All required fields present")
    
    # Check for stale token_estimate field
    if 'token_estimate' in fm_data:
        results.add_fail(filepath.name, "fm_stale", "Contains deprecated 'token_estimate' field")


def check_duplicates(filepath, results):
    """Check (b): No duplicate Session Behavior or self-intro blocks."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count Session Behavior sections
    sb_count = len(re.findall(r'^## Session Behavior Rules', content, re.MULTILINE))
    if sb_count > 1:
        results.add_fail(filepath.name, "dup_session", f"Found {sb_count} '## Session Behavior Rules' blocks (expected ≤1)")
    elif sb_count == 1:
        results.add_pass(filepath.name, "dup_session", "Single Session Behavior block")
    else:
        results.add_pass(filepath.name, "dup_session", "No Session Behavior block (OK for some files)")
    
    # Count Self-Introduction sections
    intro_count = len(re.findall(r'^## Self-Introduction', content, re.MULTILINE))
    if intro_count > 1:
        results.add_fail(filepath.name, "dup_intro", f"Found {intro_count} Self-Introduction blocks (expected ≤1)")
    else:
        results.add_pass(filepath.name, "dup_intro", f"{intro_count} Self-Introduction block(s)")
    
    # Check for duplicate parenthetical in self-intro heading
    if re.search(r'never repeat this unprompted\).*never repeat this unprompted\)', content):
        results.add_fail(filepath.name, "dup_intro_text", "Self-intro heading has duplicated parenthetical")
    
    # Count H1 headings
    h1_count = len(re.findall(r'^# [^#]', content, re.MULTILINE))
    if h1_count > 1:
        # Check if they're the same heading (duplicate)
        h1s = re.findall(r'^# (.+)$', content, re.MULTILINE)
        unique_h1s = set(h.strip() for h in h1s)
        if len(unique_h1s) < len(h1s):
            results.add_fail(filepath.name, "dup_h1", f"Duplicate H1 headings: {h1s}")


def check_stale_references(filepath, results):
    """Check (c): Zero references to archived persona names."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    found_stale = []
    for name in ARCHIVED_NAMES:
        # Check for **Name** pattern (bold routing reference)
        if f'**{name}**' in content:
            found_stale.append(name)
    
    if found_stale:
        results.add_fail(filepath.name, "stale_refs", f"References archived personas: {', '.join(found_stale)}")
    else:
        results.add_pass(filepath.name, "stale_refs", "No archived persona references")


def check_memory_refs(filepath, results):
    """Check (d): No references to memory.md as a rule file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for direct references to memory.md as a rules file
    if re.search(r'memory system defined in memory\.md', content):
        results.add_fail(filepath.name, "memory_ref", "References 'memory system defined in memory.md'")
    elif re.search(r'\.agent/rules/memory\.md', content):
        results.add_fail(filepath.name, "memory_ref", "References '.agent/rules/memory.md'")
    elif '## Memory Protocol' in content and filepath.name != 'core_axioms.md':
        # Allow core_axioms to have OS.13 Memory Protocol
        results.add_fail(filepath.name, "memory_ref", "Contains '## Memory Protocol' section (should be in core_axioms.md only)")
    else:
        results.add_pass(filepath.name, "memory_ref", "No stale memory references")


def check_self_naming(filepath, results):
    """Check (e): No self-naming clauses."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'let the agent choose its own name' in content.lower():
        results.add_fail(filepath.name, "self_naming", "Contains 'let the agent choose its own name' (factory-level)")
    elif 'your name is yours to choose' in content.lower():
        # Per-agent self-naming — will be resolved in Wave 2 (name assignment)
        results.add_fail(filepath.name, "self_naming", "Contains 'Your name is yours to choose' [WAVE 2 — deferred]")
    elif re.search(r'choose.*name.*answer to', content, re.IGNORECASE):
        results.add_fail(filepath.name, "self_naming", "Contains self-naming pattern [WAVE 2 — deferred]")


def check_core_axioms(filepath, results):
    """Check core_axioms.md specific integrity requirements."""
    if filepath.name != "core_axioms.md":
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Exactly one summary matrix heading
    matrix_headings = re.findall(r'^##\s+.*OS Axiom Stack Summary Matrix', content, re.MULTILINE)
    if len(matrix_headings) == 1:
        results.add_pass(filepath.name, "axioms_matrix_count", "Exactly one summary matrix heading")
    else:
        results.add_fail(filepath.name, "axioms_matrix_count", f"Found {len(matrix_headings)} summary matrix headings (expected 1)")

    # 2. Balanced code fences
    fence_count = len(re.findall(r'^```', content, re.MULTILINE))
    if fence_count % 2 == 0:
        results.add_pass(filepath.name, "axioms_code_fences", f"Balanced code fences ({fence_count} total)")
    else:
        results.add_fail(filepath.name, "axioms_code_fences", f"Unbalanced code fences ({fence_count} total)")

    # 3. All axiom numbers OS.00-OS.18 present exactly once as section headers
    expected_axioms = [
        "OS.00", "OS.0", "OS.1", "OS.2", "OS.3", "OS.4", "OS.5", "OS.6", "OS.7",
        "OS.8", "OS.9", "OS.10", "OS.11", "OS.12", "OS.13", "OS.14", "OS.15",
        "OS.16", "OS.17", "OS.18"
    ]
    
    headers = re.findall(r'^##\s+.*?(OS\.\d+)', content, re.MULTILINE)
    header_counts = {}
    for h in headers:
        header_counts[h] = header_counts.get(h, 0) + 1
    
    missing_headers = [a for a in expected_axioms if header_counts.get(a, 0) == 0]
    duplicate_headers = [a for a, c in header_counts.items() if c > 1]
    
    if not missing_headers and not duplicate_headers and len(headers) == len(expected_axioms):
        results.add_pass(filepath.name, "axioms_headers", f"All {len(expected_axioms)} axioms OS.00-OS.18 present exactly once as section headers")
    else:
        errs = []
        if missing_headers:
            errs.append(f"missing: {missing_headers}")
        if duplicate_headers:
            errs.append(f"duplicates: {duplicate_headers}")
        results.add_fail(filepath.name, "axioms_headers", f"Axiom header check failed ({', '.join(errs)})")

    # 4. Matrix rows match section headers
    matrix_match = re.search(r'##\s+.*OS Axiom Stack Summary Matrix\s*\n\n```\n(.*?)\n```', content, re.DOTALL)
    if matrix_match:
        matrix_text = matrix_match.group(1)
        matrix_axioms = re.findall(r'\|\s*(?:Level\s*\d+|L[\d\.]+)\s*\|\s*(OS\.\d+)', matrix_text)
        if matrix_axioms == expected_axioms:
            results.add_pass(filepath.name, "axioms_matrix_rows", f"Matrix rows ({len(matrix_axioms)}) match section headers in exact order")
        else:
            results.add_fail(filepath.name, "axioms_matrix_rows", f"Matrix rows do not match expected section headers. Got: {matrix_axioms}")
    else:
        results.add_fail(filepath.name, "axioms_matrix_rows", "Could not parse summary matrix table block")


# ============================================================
# Main
# ============================================================

def main():
    if not RULES_DIR.exists():
        print(f"ERROR: Rules directory not found: {RULES_DIR}")
        sys.exit(1)
    
    files = get_active_files()
    print(f"Validating {len(files)} active files in {RULES_DIR}\n")
    
    results = ValidationResult()
    
    for filepath in files:
        check_frontmatter(filepath, results)
        check_duplicates(filepath, results)
        check_stale_references(filepath, results)
        check_memory_refs(filepath, results)
        check_self_naming(filepath, results)
        check_core_axioms(filepath, results)
    
    # Print results
    if results.failures:
        print("=" * 60)
        print(f"FAILURES ({len(results.failures)})")
        print("=" * 60)
        for file, check, detail in results.failures:
            print(f"  FAIL  {file:25s} [{check:15s}] {detail}")
    
    if VERBOSE and results.passes:
        print()
        print("=" * 60)
        print(f"PASSES ({len(results.passes)})")
        print("=" * 60)
        for file, check, detail in results.passes:
            print(f"  PASS  {file:25s} [{check:15s}] {detail}")
    
    print()
    print("=" * 60)
    print(f"SUMMARY: {results.summary()}")
    print("=" * 60)
    
    # Exit with error code if any failures
    sys.exit(1 if results.failures else 0)


if __name__ == "__main__":
    main()
