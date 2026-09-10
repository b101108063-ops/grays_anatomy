#!/usr/bin/env python3
"""Replace homepage HTML after Hugo build with correct card grid layout."""
import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract just the content (body innerHTML) from Hugo output
# We need to keep the Hugo-generated structure but inject correct CSS
body_m = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL)
if not body_m:
    print("ERROR: no body tag found")
    exit(1)

body_content = body_m.group(1)

# Inject chapter-grid CSS into the existing style block
correct_css = """
    .chapter-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; }
    .chapter-card { display: block; background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 18px 20px 20px; text-decoration: none; transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s; position: relative; }
    .chapter-card:hover { border-color: #58a6ff; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.35); }
    .ch-num { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #58a6ff; margin-bottom: 5px; }
    .ch-title { font-size: 1rem; font-weight: 600; color: #fff; margin-bottom: 2px; line-height: 1.3; }
    .ch-title-en { font-size: 0.78rem; color: #8b949e; font-weight: 400; margin-bottom: 8px; }
    .ch-pages { font-size: 0.8rem; color: #8b949e; line-height: 1.5; }
    .about-section { margin-top: 44px; background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 24px 28px; }
    .about-section h2 { color: #fff; font-size: 1rem; font-weight: 600; margin-bottom: 10px; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-top: 0; }
    .about-section p { font-size: 0.88rem; color: #8b949e; margin-bottom: 8px; }
    .about-section p:last-child { margin-bottom: 0; }
    .section-title { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: #8b949e; margin-bottom: 18px; padding-left: 4px; }
    .container { max-width: 960px; margin: 0 auto; padding: 40px 20px 60px; }
    .site-header { background: linear-gradient(135deg, #1a2332 0%, #0d1117 100%); border-bottom: 1px solid #30363d; padding: 40px 24px 32px; text-align: center; }
    .site-header h1 { font-size: 2rem; font-weight: 700; color: #fff; letter-spacing: -0.02em; margin-bottom: 4px; }
    .site-header .subtitle { font-size: 0.9rem; color: #8b949e; }
    .site-header .divider { width: 60px; height: 3px; background: #58a6ff; margin: 14px auto 0; border-radius: 2px; }
"""

# Find existing style tag and append our CSS
if '<style>' in html:
    # Append CSS before closing </style>
    html = re.sub(r'(</style>)', correct_css + r'\1', html, count=1)
else:
    # No style tag, add one before body
    html = re.sub(r'(<body)', f'<style>{correct_css}</style>\\1', html, count=1)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Done. HTML size: {len(html)} bytes")
