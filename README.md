# ApnaCollege-Project

This is my Repository. The [practice page](index.html) starts with "Hello World" and links to two HTML exercises.

Author - Aditya Pratap (Programming Events)

## Local preview

Open [index.html](index.html) directly in a browser. To serve the pages with Python 3, open a terminal in the repository root and run the following command.

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Open [the local preview](http://127.0.0.1:8000/). Keep the terminal open as you edit. Save a file and refresh the page to see the change. Press Ctrl+C in the terminal to stop the server.

## Practice

1. **Edit the greeting page.** Add `<p>My first HTML edit.</p>` directly after the `<h1>` in [index.html](index.html). Refresh the page and look for your sentence below “Hello World”.
2. **Compare two list types.** Open the [lemonade recipe](examples/lemonade.html). Add `<li>Ice cubes</li>` inside the ingredient list and `<li>Add ice before serving.</li>` at the end of the method. Refresh to see a new bullet and a fourth numbered step. Open print preview to see the recipe as a handout.
3. **Use a disclosure with the keyboard.** Open the [HTML self-check](examples/quiz.html). Press Tab until the first question has a focus outline, then press Enter to reveal the answer. Follow the ingredient link to jump to that section in the recipe.

## Check your edits

From the repository root, run the checks with Python 3. They verify the greeting, page titles, language, headings and main landmarks. They also follow local links to catch missing examples, stylesheets and section IDs.

```sh
python -m unittest discover -s tests -v
```
