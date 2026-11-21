from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.elements = defaultdict(list)
        self.declarations = []
        self.text = defaultdict(list)
        self.text_tag = None
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_decl(self, declaration):
        self.declarations.append(declaration.lower())

    def handle_starttag(self, tag, attrs):
        self.elements[tag].append(dict(attrs))
        if tag in {"h1", "title"}:
            self.text_tag = tag

    def handle_data(self, data):
        if self.text_tag:
            self.text[self.text_tag].append(data)

    def handle_endtag(self, tag):
        if tag == self.text_tag:
            self.text_tag = None

    def text_of(self, tag):
        return "".join(self.text[tag]).strip()

    def local_links(self, *tags):
        for tag in tags:
            for attrs in self.elements[tag]:
                if "href" not in attrs:
                    continue
                href = attrs["href"] or ""
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                target = self.path
                if url.path:
                    target = (self.path.parent / unquote(url.path)).resolve()
                    if target.is_dir():
                        target = target / "index.html"
                yield href, target, unquote(url.fragment)


class PageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        paths = [HOME, *sorted((ROOT / "examples").rglob("*.html"))]
        cls.pages = {path: Page(path) for path in paths}

    def test_pages_have_a_language_title_heading_and_landmark(self):
        for path, page in self.pages.items():
            with self.subTest(page=path.relative_to(ROOT)):
                self.assertIn("doctype html", page.declarations)
                for element in ("html", "title", "main", "h1"):
                    self.assertEqual(len(page.elements[element]), 1, element)
                self.assertTrue(page.elements["html"][0].get("lang"))
                self.assertTrue(page.text_of("title"))
                self.assertTrue(page.text_of("h1"))

    def test_page_titles_are_distinct(self):
        titles = [page.text_of("title") for page in self.pages.values()]
        self.assertEqual(len(titles), len(set(titles)))

    def test_home_keeps_the_original_greeting(self):
        self.assertEqual(self.pages[HOME].text_of("h1"), "Hello World")

    def test_local_links_stylesheets_and_fragments_exist(self):
        for path, page in self.pages.items():
            for href, target, fragment in page.local_links("a", "link"):
                with self.subTest(page=path.relative_to(ROOT), href=href):
                    self.assertIn(ROOT, target.parents)
                    self.assertTrue(target.is_file(), f"Missing file for {href}")
                    if fragment and target.suffix.lower() == ".html":
                        target_page = self.pages.get(target) or Page(target)
                        ids = [attrs.get("id") for tags in target_page.elements.values()
                               for attrs in tags]
                        self.assertEqual(ids.count(fragment), 1, f"Unresolved or duplicate #{fragment}")

    def test_home_links_to_every_example(self):
        linked = {target for _, target, _ in self.pages[HOME].local_links("a")}
        for path in self.pages.keys() - {HOME}:
            with self.subTest(page=path.relative_to(ROOT)):
                self.assertIn(path, linked)
