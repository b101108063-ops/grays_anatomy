#!/usr/bin/env python3
"""Inject correct homepage CSS into Hugo-built index.html after build."""
import sys, re

target = sys.argv[1] if len(sys.argv) > 1 else 'public/index.html'

with open(target, 'r', encoding='utf-8') as f:
    html = f.read()

# Correct CSS to inject
extra_css = """
.chapter-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.chapter-card{display:block;background:#161b22;border:1px solid #30363d;border-radius:10px;padding:18px 20px 20px;text-decoration:none;transition:border-color .2s,transform .2s,box-shadow .2s;position:relative}
.chapter-card:hover{border-color:#58a6ff;transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.35)}
.ch-num{font-size:.68rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#58a6ff;margin-bottom:5px}
.ch-title{font-size:1rem;font-weight:600;color:#fff;margin-bottom:2px;line-height:1.3}
.ch-title-en{font-size:.78rem;color:#8b949e;font-weight:400;margin-bottom:8px}
.ch-pages{font-size:.8rem;color:#8b949e;line-height:1.5}
.about-section{margin-top:44px;background:#161b22;border:1px solid #30363d;border-radius:10px;padding:24px 28px}
.about-section h2{color:#fff;font-size:1rem;font-weight:600;margin-bottom:10px;border-bottom:1px solid #30363d;padding-bottom:8px;margin-top:0}
.about-section p{font-size:.88rem;color:#8b949e;margin-bottom:8px}
.about-section p:last-child{margin-bottom:0}
.section-title{font-size:.72rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#8b949e;margin-bottom:18px;padding-left:4px}
.container{max-width:960px;margin:0 auto;padding:40px 20px 60px}
"""

# Inject before </style>
if '</style>' in html:
    html = html.replace('</style>', extra_css + '\n</style>', 1)
else:
    print("WARNING: no </style> found, CSS not injected")

with open(target, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Done: {len(html)} bytes")
