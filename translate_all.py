#!/usr/bin/env python3
"""
Split Gray's Anatomy chapters into chunks for parallel translation.
Outputs manifest of chunks: {section, chunk_index, start_line, end_line, path}
"""
import os, json

BASE = "/home/node/.openclaw/workspace/grays_anatomy_hugo/content/docs"
CHUNK_SIZE = 500  # lines per chunk

sections = [
    ("body", "content/docs/body/_index.md"),
    ("back", "content/docs/back/_index.md"),
    ("thorax", "content/docs/thorax/_index.md"),
    ("abdomen", "content/docs/abdomen/_index.md"),
    ("pelvis", "content/docs/pelvis/_index.md"),
    ("lower-limb", "content/docs/lower-limb/_index.md"),
    ("upper-limb", "content/docs/upper-limb/_index.md"),
    ("head-neck", "content/docs/head-neck/_index.md"),
    ("appendix", "content/docs/appendix/_index.md"),
]

manifest = []

for sec_name, rel_path in sections:
    full_path = os.path.join("/home/node/.openclaw/workspace/grays_anatomy_hugo", rel_path)
    with open(full_path, encoding='utf-8') as f:
        lines = f.readlines()

    total = len(lines)
    chunks = []
    i = 0
    chunk_idx = 0
    while i < total:
        start = i
        end = min(i + CHUNK_SIZE, total)
        chunk_idx += 1

        # Extract this chunk's content
        chunk_lines = lines[start:end]
        chunk_text = ''.join(chunk_lines)

        out_name = f"/tmp/grays_translate_{sec_name}_chunk{chunk_idx:02d}.txt"
        with open(out_name, 'w', encoding='utf-8') as f:
            f.write(chunk_text)

        manifest.append({
            "section": sec_name,
            "chunk": chunk_idx,
            "start_line": start + 1,  # 1-based
            "end_line": end,
            "total_lines": total,
            "num_lines": end - start,
            "source_path": rel_path,
            "chunk_path": out_name,
            "done_path": out_name.replace("_chunk", "_done_chunk"),
        })
        i = end

    print(f"{sec_name}: {total} lines → {chunk_idx} chunks")

with open("/tmp/grays_translate_manifest.json", 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"\n總共 {len(manifest)} 個 chunk，已寫入 /tmp/grays_translate_manifest.json")
