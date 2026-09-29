# Guoan Wang — Academic Homepage

Personal academic homepage, live at **<https://tousenkaname.github.io>**.

Built with [Jekyll](https://jekyllrb.com/) on GitHub Pages, based on the
[AcadHomepage](https://github.com/RayeRen/acad-homepage.github.io) template
(Minimal Mistakes theme).

## Features

- **Auto-synced Google Scholar data** — a GitHub Action
  (`.github/workflows/google_scholar_crawler.yaml`) runs every 8 hours, crawls my
  Google Scholar profile, and pushes the results to the `google-scholar-stats`
  branch. The homepage reads that JSON at load time to show the total citation
  badge, per-paper citation counts, and the auto-generated
  "Full Publication List" section. If Scholar can't be reached, the last
  published data is kept and the run is flagged; after 3 days without a
  successful sync the workflow fails so it gets noticed.
- **Visitor globe** — the footer shows a slowly turning globe of where
  visitors come from, with the top countries/regions beside it. A second
  GitHub Action (`.github/workflows/visitor_stats.yaml`) reads the site's
  Flag Counter stats every 6 hours and pushes `visitors.json` to the
  `visitor-stats` branch.
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
| `_includes/visitor-globe.html`, `assets/js/visitor-globe.js` | The visitor globe footer and its renderer |
| `visitor_crawler/` | Builds `visitors.json` from the Flag Counter stats page; `countries.csv` maps country codes to map ids and centroids |

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
