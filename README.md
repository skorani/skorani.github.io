# skorani.github.io

Source for **https://skorani.github.io/**, the website of Samira Korani (Knowledge Graphs · GraphRAG · LLM Evaluation).

It is a small Jekyll site. GitHub Pages builds it automatically from the `main` branch; there is no build step to run before pushing. Almost everything you will want to change lives in plain YAML files in `_data/`.

## Preview locally

One-time setup on macOS (installs Ruby 3.3, the version GitHub Pages uses, and the exact gems GitHub uses):

```sh
brew install ruby@3.3
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"   # add this line to ~/.zshrc to keep it
cd ~/skorani.github.io
bundle config set --local path vendor/bundle
bundle install
```

Then, each time:

```sh
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
bundle exec jekyll serve
```

Open <http://127.0.0.1:4000/>. Pages rebuild when you save; restart the server after editing `_config.yml`.

To build without serving (output goes to `_site/`, which is not committed):

```sh
JEKYLL_ENV=production bundle exec jekyll build
```

## Publish

GitHub Pages is set to **Deploy from a branch: `main`, `/ (root)`**. Anything merged into `main` goes live within a minute or two.

1. Work on a branch and push it: `git push -u origin <branch>`.
2. Open a pull request on GitHub and check the changes.
3. Merge. Then watch **Actions → pages build and deployment** for a green tick, and reload the site.
4. To undo a release, revert the merge commit on `main`.

## Where to change things

| To change… | Edit |
|---|---|
| A consulting package: price, timing, audience, deliverables, steps, FAQ | its file in `_packages/` (one file = one page at `/services/<file-name>/`) |
| Show or hide a package everywhere | `published: true` or `false` in its `_packages/` file |
| The featured package (homepage) | `featured: true` in one `_packages/` file; `order` sets the order |
| Generic engagement steps (services overview) | `_data/process.yml` |
| Homepage FAQs | `_data/faq.yml` |
| Projects in "Selected technical work" | `_data/projects.yml` |
| Talks, recognition, topics, workshops, talk history | `_data/talks.yml` |
| Articles and research | `_data/writing.yml` (`home: true` puts an article on the homepage; keep it to three) |
| Email, LinkedIn, GitHub, Medium, location | `_data/profile.yml` |
| Email subjects and prefilled text of contact buttons | `enquiries` in `_data/profile.yml` |
| A real booking link ("Book a call") | `booking_url` in `_data/profile.yml` |
| A public CV link | `cv_url` in `_data/profile.yml` |
| **Company particulars in the footer** | `_data/company.yml` |
| Navigation | `_data/nav.yml` |
| Homepage headline, About text | `index.html` |
| Page titles and descriptions | front matter at the top of each page (`index.html`, `services/index.html`, …) |
| Colours, type, spacing | `brand-kit/tokens.css` (see `brand-kit/brand-guidelines.md`) |
| Layout and component styles | `assets/css/site.css` |

### Common edits

**Change a price.** In the package's file in `_packages/`, edit `fee` (shown exactly as written, e.g. `EUR 3,200`) and `fee_note`, and the number in `price_eur` (or `price_low`/`price_high` for a range), which search engines read. The package page, the homepage and `/services/` all update.

**Launch with fewer packages.** Set `published: false` in a package file. Its page, homepage card, links and sitemap entry all disappear; set it back to `true` to relaunch at the same address.

**Add a package.** Copy a file in `_packages/`, rename it (the file name becomes the web address), change every field, and add a matching email subject under `enquiries` in `_data/profile.yml`.

**Add the "Book a call" button.** Paste a real scheduling link (for example Cal.com or a Google Calendar appointment page) into `booking_url` in `_data/profile.yml`. Every package page and the contact section switch from email to "Book a call", with email kept as the second option.

**Add the company's registered details.** In `_data/company.yml`, fill in `place_of_registration`, `registered_number`, `registered_office` and, only if VAT-registered, `vat_number`. Empty values stay off the site, so never type placeholder text there.

**Add a project.** Copy an entry in `_data/projects.yml`. Describe only what the public code actually does, and link to it. A commented-out entry for the GraphRAG agent repository is ready to fill in once that repository has code.

**Add a talk.** For a new headline talk, replace `featured_talk` in `_data/talks.yml` and move the previous one into `archive` (newest first). For anything else, add it to `archive`, with a `url` only if a public recording or page exists.

**Add an article.** Add an entry to the top of `articles` in `_data/writing.yml` with its live URL, date and a one-sentence summary. Only list published pieces.

**Replace the portrait.** Save a 4:5 photo as `assets/img/samira-korani-portrait.jpg` and `.webp` (480 × 600 is enough).

## Optional checks

Two scripts check the site in your installed Google Chrome. They are not needed to publish. One-time setup: `python3 -m venv ~/.venvs/site && ~/.venvs/site/bin/pip install playwright pillow`.

While `bundle exec jekyll serve` is running:

```sh
~/.venvs/site/bin/python tools/verify_site.py    # accessibility, links, keyboard, contrast, redirects
~/.venvs/site/bin/python tools/screenshots.py    # screenshots at 320, 768 and 1440 px in review/screenshots/
```

## Repository layout

```text
_config.yml          site settings and the list of files kept off the website
_data/               all editable content (see the table above)
_packages/           one file per consulting package; each becomes /services/<file-name>/
_includes/           shared pieces: head and SEO, header, footer, contact section, package blocks
_layouts/            page shell (default.html), package pages (package.html), redirects (redirect.html)
index.html           homepage
services/ speaking/ writing/   inner pages
404.html             not-found page
Activities.html, Publications.html, Resource.html, teaching.html, blog.html, docs/
                     redirects from the old site's URLs, so existing links keep working
assets/              site CSS, the copy-email script and images
brand-kit/           brand guidelines, design tokens, fonts, logos, social image
sitemap.xml, robots.txt
tools/              optional checks (verify_site.py) and screenshots (screenshots.py)
```

Brand rules, including when to use "Samira Korani" and when to name MILEAWAY AI SYSTEMS LIMITED, are in `brand-kit/brand-guidelines.md`.
