# jason-tutorial-series

```bash
python3 -m pip install markdown2 beautifulsoup4 pygments-agentspeak
for f in md/*.md; do name=$(basename "$f" ".md"); python3 md2html.py "$f" > "html/$name.html"; done
```