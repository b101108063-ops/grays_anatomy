#!/usr/bin/env python3
"""Fix all formatting issues in Gray's Anatomy content files."""

import re, os

BASE = "/home/node/.openclaw/workspace/grays_anatomy_hugo/content/docs"

files = [
    "abdomen/_index.md",
    "appendix/_index.md",
    "back/_index.md",
    "body/_index.md",
    "head-neck/_index.md",
    "lower-limb/_index.md",
    "pelvis/_index.md",
    "thorax/_index.md",
    "upper-limb/_index.md",
]

def fix_heading(line):
    """Fix mixed Chinese/English heading to English（中文）format."""
    # Match headings: ## or ### followed by text with both Chinese and English
    m = re.match(r'^(#{1,3})\s+(.*)', line)
    if not m:
        return line
    hashes, text = m.group(1), m.group(2).strip()
    
    # Check if has both Chinese and English
    has_zh = bool(re.search(r'[\u4e00-\u9fff]', text))
    has_en = bool(re.search(r'[A-Za-z]{2,}', text))
    
    if not (has_zh and has_en):
        return line
    
    original = text
    
    # Pattern: Chinese first, then English in parentheses or after dash
    # e.g. "骨盆腔靜脈 (Pelvic Veins)" or "骨盆腔靜脈 (Pelvic Veins）"
    m2 = re.match(r'^([\u4e00-\u9fff\u3000-\u303f\uff00-\uffef（）『』（）、，．：；？！「」『』\[\]【】—–\-–_（）\(\)（ ）\s]+)\s*[\(（]\s*([A-Za-z][A-Za-z\s&,\-:]+?)\s*[\)）]\s*$', text)
    if m2:
        zh_part = m2.group(1).strip()
        en_part = m2.group(2).strip()
        # Remove trailing punctuation from en_part
        en_part = re.sub(r'[\s\-–—]+$', '', en_part)
        text = f"{en_part}（{zh_part}）"
        return f"{hashes} {text}"
    
    # Pattern: Chinese first, English after dash/em-dash without parentheses
    # e.g. "Pelvis and Perineum — 骨盆與會陰" or "Pelvis and Perineum - 骨盆與會陰"
    m3 = re.match(r'^([A-Za-z][A-Za-z\s&,\-:\']+)[\s\-–—]+([\u4e00-\u9fff\u3000-\u303f\uff00-\uffef（）『』（）、，．：；？！「」『』\[\]【】\s]+)$', text)
    if m3:
        en_part = m3.group(1).strip()
        zh_part = m3.group(2).strip()
        text = f"{en_part}（{zh_part}）"
        return f"{hashes} {text}"
    
    # Pattern: Chinese first, English at end (no punctuation)
    # e.g. "Gray's Anatomy — Head & Neck：Regional Anatomy"  (has both Chinese punctuation and English)
    # e.g. "骨盆腔靜脈 (Pelvic Veins)" already handled above
    
    return line

def fix_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    changes = {'double_space': 0, 'trailing_ws': 0, 'heading': 0, 'allcaps': 0}
    
    for line in lines:
        original = line
        
        # Fix double spaces
        new_line = re.sub(r'  +', ' ', line)
        if new_line != line:
            changes['double_space'] += line.count('  ')
            line = new_line
        
        # Fix trailing whitespace
        if line.rstrip() != line:
            changes['trailing_ws'] += 1
            line = line.rstrip() + '\n'
        
        # Fix headings (only H2 and H3)
        if re.match(r'^#{2,3}\s+', line):
            new_line = fix_heading(line)
            if new_line != line:
                changes['heading'] += 1
                line = new_line
        
        # Fix all-caps English headings (add proper formatting)
        m = re.match(r'^(#{2,3})\s+([A-Z][A-Z\s\&\-\,\:\'\(\)]+)$', line.strip())
        if m:
            hashes, text = m.group(1), m.group(2).strip()
            # This catches ALL-CAPS headings without Chinese
            # Only fix if it looks like a real heading (has 3+ words)
            words = text.split()
            if len(words) >= 2 and all(w.isupper() or w in ['&', '-', ',', ':', "'", '(', ')'] for w in words):
                changes['allcaps'] += 1
                # Convert to Title Case
                title_case = text.title()
                # Keep specific acronyms uppercase: DNA, RNA, CNS, etc
                title_case = re.sub(r'\bCns\b', 'CNS', title_case)
                title_case = re.sub(r'\bDna\b', 'DNA', title_case)
                title_case = re.sub(r'\bRna\b', 'RNA', title_case)
                title_case = re.sub(r'\bAids\b', 'AIDS', title_case)
                title_case = re.sub(r'\bHiv\b', 'HIV', title_case)
                title_case = re.sub(r'\bCt\b', 'CT', title_case)
                title_case = re.sub(r'\bMri\b', 'MRI', title_case)
                title_case = re.sub(r'\bPet\b', 'PET', title_case)
                line = f"{hashes} {title_case}\n"
        
        fixed_lines.append(line)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    total = sum(changes.values())
    if total > 0 or changes['double_space'] > 0 or changes['trailing_ws'] > 0:
        print(f"  {os.path.basename(os.path.dirname(filepath))}/{os.path.basename(filepath)}: "
              f"headings={changes['heading']}, allcaps={changes['allcaps']}, "
              f"dbl_space={changes['double_space']}, trailing_ws={changes['trailing_ws']}")
    
    return changes

print("Fixing all format issues...")
total_changes = {'double_space': 0, 'trailing_ws': 0, 'heading': 0, 'allcaps': 0}
for f in files:
    path = os.path.join(BASE, f)
    if os.path.exists(path):
        c = fix_file(path)
        for k in total_changes:
            total_changes[k] += c[k]

print(f"\n總計: 混合標題修正={total_changes['heading']}, 全大寫修正={total_changes['allcaps']}, "
      f"雙空格={total_changes['double_space']}, 行尾空白={total_changes['trailing_ws']}")
