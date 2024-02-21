import argparse
import sys

import markdown2
from bs4 import BeautifulSoup


# <link rel="stylesheet" href="https://unpkg.com/@primer/css@^20.2.4/dist/primer.css">


def translate(markdown_str):
    html_body = markdown2.markdown(markdown_str, extras=["toc", "fenced-code-blocks", "tables", "code-friendly", "strike"])
    soup = BeautifulSoup(html_body.toc_html, "html.parser")
    title = soup.find("a").text
    html_toc = str(soup.find("ul").find("ul"))
    html_body = html_body.replace("<!-- TOC -->", html_toc)
    return f"""<!DOCTYPE html>
<html>
<head>
  <title>{title}</title>
  <link rel="stylesheet" href="primer.css">
  <link rel="stylesheet" href="pygments.css">
</head>
<body>
<div class="container-lg p-4">
<div class="col-12">
<div class="markdown-body border rounded-3 p-6">
{html_body}
</div>
<footer class="p-6 mt-4">
<p class="text-center">Copyright &copy; <strong>Kevin McAreavey</strong> 2024</p>
</footer>
</div>
</div>
</body>
</html>"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate Markdown with Jason code blocks to HTML with Primer CSS")
    parser.add_argument("file", nargs="?", type=argparse.FileType("r"), default=sys.stdin, help="read from Markdown file or stdin")
    args = parser.parse_args()

    html = translate(args.file.read())
    print(html)
