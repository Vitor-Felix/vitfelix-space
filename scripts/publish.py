#!/usr/bin/env python3

from pathlib import Path
import json
import re

import markdown


ROOT = Path(__file__).resolve().parent.parent

CONTENT_DIR = ROOT / "content"
TEMPLATE = ROOT / "templates" / "post.html"
OUTPUT_DIR = ROOT / "public" / "posts"
BLOG_FILE = ROOT / "public" / "blog.html"
POSTS_JSON = ROOT / "public" / "data" / "posts.json"


def read_post(md_file):
    text = md_file.read_text(encoding="utf-8")

    metadata = {}
    body = text

    if text.startswith("---"):
        parts = text.split("---", 2)

        if len(parts) >= 3:
            header = parts[1]
            body = parts[2]

            for line in header.splitlines():
                line = line.strip()

                if ":" not in line:
                    continue

                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

    return metadata, body.strip()


def render_post(template, title, content_html, prefix):
    return (
        template
        .replace("{{TITLE}}", title)
        .replace("{{CONTENT}}", content_html)
        .replace("{{PREFIX}}", prefix)
    )


def slug(filename):
    return re.sub(r"\.md$", "", filename)


def build_blog(posts):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog - Vitor Felix</title>
<link rel="stylesheet" href="css/style.css">
</head>
<body>

<div class="container">

<header>
<h1>Blog</h1>
<p>Notes, experiments and things I'm learning.</p>
</header>

<nav>
<a href="index.html">Home</a> |
<a href="blog.html">Blog</a>
</nav>

<main>
<section>

<h2>Posts</h2>

<ul>
"""

    for post in sorted(posts, key=lambda p: p["title"]):
        html += f"""
<li>
<a href="{post['url']}">{post['title']}</a>
</li>
"""

    html += """
</ul>

</section>
</main>

<footer>
<p>© 2026 Vitor Felix ☕</p>
</footer>

</div>

</body>
</html>
"""

    BLOG_FILE.write_text(html, encoding="utf-8")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    POSTS_JSON.parent.mkdir(parents=True, exist_ok=True)

    template = TEMPLATE.read_text(encoding="utf-8")

    posts = []

    for md in sorted(CONTENT_DIR.rglob("*.md")):
        metadata, body = read_post(md)

        title = metadata.get("title", md.stem)

        html_content = markdown.markdown(
            body,
            extensions=["fenced_code", "tables"],
        )

        # Calculate the path relative to the content directory
        # before using it to determine the URL prefix.
        relative_path = md.relative_to(CONTENT_DIR)

        depth = len(relative_path.parts) - 1
        prefix = "../" * (depth + 1)

        page = render_post(
            template,
            title,
            html_content,
            prefix,
        )

        output_path = OUTPUT_DIR / relative_path.with_suffix(".html")

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            page,
            encoding="utf-8",
        )

        posts.append(
            {
                "title": title,
                "slug": slug(md.name),
                "url": f"posts/{relative_path.with_suffix('.html')}",
            }
        )

    POSTS_JSON.write_text(
        json.dumps(posts, indent=4),
        encoding="utf-8",
    )

    build_blog(posts)

    print(f"Published {len(posts)} posts.")


if __name__ == "__main__":
    main()
    