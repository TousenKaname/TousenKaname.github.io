# Guoan Wang — Academic Homepage

Personal academic homepage, live at **<https://tousenkaname.github.io>**.

Built with [Jekyll](https://jekyllrb.com/) on GitHub Pages, based on the
[AcadHomepage](https://github.com/RayeRen/acad-homepage.github.io) template
(Minimal Mistakes theme).

## Features

- **Auto-synced Google Scholar data** — a GitHub Action
  (`.github/workflows/google_scholar_crawler.yaml`) runs daily, crawls my
  Google Scholar profile, and pushes the results to the `google-scholar-stats`
  branch. The homepage reads that JSON at load time to show the total citation
  badge, per-paper citation counts, and the auto-generated
  "Full Publication List" section.
- **Single-page layout** — all content lives in `_pages/about.md`.
- **Responsive design** — adapts to desktop and mobile viewports.

## Project structure

| Path | Purpose |
| --- | --- |
| `_pages/about.md` | The homepage content (intro, education, publications, services, awards, internships) |
| `_data/navigation.yml` | Navigation entries shown in the masthead |
| `_config.yml` | Site configuration (title, author profile, theme settings) |
| `_layouts/`, `_includes/` | Theme templates; `_includes/fetch_google_scholar_stats.html` wires the Scholar data into the page |
| `assets/js/scholar-stats.js` | Renders citation counts and the full publication list from `gs_data.json` |
| `_sass/_custom.scss` | All site-specific styles (paper boxes, education rows, publication list) |
| `assets/`, `_sass/` (rest) | Theme CSS/JS/fonts (vendored Minimal Mistakes) |
| `images/` | Avatar, favicons, school logos (`logo-*`), publication figures (`pub-*`) |
| `google_scholar_crawler/` | The crawler run by the GitHub Action (uses the `GOOGLE_SCHOLAR_ID` repo secret) |

## Local development

```bash
bundle install
bundle exec jekyll serve   # http://127.0.0.1:4000
```

Note: the Scholar-driven parts (citation counts, full publication list) fetch
data from the `google-scholar-stats` branch of this repository, so they work
locally too as long as you are online.

## Updating content

- Edit `_pages/about.md` for any section of the page.
- Selected Publications are hand-curated paper boxes with figures; the Full
  Publication List updates itself from Google Scholar — no manual edits needed.
- Add or reorder navigation items in `_data/navigation.yml`.

## License

MIT, following the upstream template. See [LICENSE](LICENSE).
