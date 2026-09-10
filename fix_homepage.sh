#!/bin/bash
# Post-build script: fix homepage CSS classes and grid layout
# Replaces Hugo's plain body tag with one that has the homepage class
# and injects proper card grid CSS

# Fix body tag to add homepage class
sed -i 's/<body>/<body class="homepage">/' public/index.html

# Inject card grid CSS after </style>
CSS_INJECT='
<style>
.chapter-grid{display:grid!important;grid-template-columns:repeat(auto-fill,minmax(260px,1fr))!important;gap:14px!important}
.chapter-card{display:block!important;background:#161b22!important;border:1px solid #30363d!important;border-radius:10px!important;padding:18px 20px 20px!important;text-decoration:none!important;transition:border-color .2s,transform .2s,box-shadow .2s!important;position:relative!important}
.chapter-card:hover{border-color:#58a6ff!important;transform:translateY(-2px)!important;box-shadow:0 6px 20px rgba(0,0,0,.35)!important}
.ch-num{font-size:.68rem!important;font-weight:700!important;letter-spacing:.1em!important;text-transform:uppercase!important;color:#58a6ff!important;margin-bottom:5px!important}
.ch-title{font-size:1rem!important;font-weight:600!important;color:#fff!important;margin-bottom:2px!important;line-height:1.3!important}
.ch-title-en{font-size:.78rem!important;color:#8b949e!important;font-weight:400!important;margin-bottom:8px!important}
.ch-pages{font-size:.8rem!important;color:#8b949e!important;line-height:1.5!important}
.about-section{margin-top:44px!important;background:#161b22!important;border:1px solid #30363d!important;border-radius:10px!important;padding:24px 28px!important}
.about-section h2{color:#fff!important;font-size:1rem!important;font-weight:600!important;margin-bottom:10px!important;border-bottom:1px solid #30363d!important;padding-bottom:8px!important;margin-top:0!important}
.about-section p{font-size:.88rem!important;color:#8b949e!important;margin-bottom:8px!important}
.section-title{font-size:.72rem!important;font-weight:600!important;letter-spacing:.12em!important;text-transform:uppercase!important;color:#8b949e!important;margin-bottom:18px!important;padding-left:4px!important}
.container{max-width:960px!important;margin:0 auto!important;padding:40px 20px 60px!important}
</style>'

# Use awk to inject after </style> tag
awk -v css="$CSS_INJECT" '
    /<\/style>/ {
        print $0
        print css
        next
    }
    { print }
' public/index.html > public/index.html.tmp && mv public/index.html.tmp public/index.html

echo "Homepage CSS fix applied. index.html size: $(wc -c < public/index.html) bytes"
