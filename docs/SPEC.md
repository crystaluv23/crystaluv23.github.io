# L’s Log — Lil’Log reproduction

## Goal

Reproduce the reading experience and page structure of https://lilianweng.github.io/ using Hugo, the upstream PaperMod theme, and GitHub Pages. Keep the theme as a Git submodule pinned by the parent repository. Do not introduce a custom application framework or redesign the reference.

## Scope

- Site name: L’s Log. Author: L. Reference identity, analytics, and original articles are not reused.
- Match the reference's system font, neutral palette, compact welcome section, article cards, metadata labels, navigation (Posts / Archive / Search / Tags / FAQ), article typography, table of contents, and Hugo / PaperMod footer.
- Support light/dark appearance, responsive layouts, title/body search, tag filtering, yearly/monthly archives, Markdown articles, RSS, sitemap, syntax highlighting, and code copying.
- Publish only the author's real articles under `content/posts/`. Remove the six demonstration articles after validation. Keep unfinished work locally under ignored `content/drafts/` with `draft: true` and `type: posts`.
- Provide a live writing workflow: `scripts/dev.sh` runs Hugo with drafts, full rebuilds, automatic browser reload and navigation to the edited article. Saving Markdown must update text and LaTeX formulas without a push or manual refresh.
- Main reading width 720 px; navigation width 1024 px; desktop gutter 24 px; mobile gutter 14 px. Preserve readable, accessible layout on narrow screens.
- No third-party analytics, comments provider, newsletter, or invented personal links.

## Delivery and validation

- Source lives at the workspace root. Hugo version is pinned in `.hugo-version` and CI.
- GitHub Actions builds pull requests and deploys successful main-branch builds to GitHub Pages. The build uses the Pages-provided base URL for deployment.
- Check a production build, generated internal links/assets, search index, RSS, expected routes, and absence of reference-author identity.
- Inspect desktop and mobile preview when browser infrastructure is available. Verify search, theme persistence, archive/tag navigation, article TOC, and copy behavior. Formula support must also work in article summaries on list pages.
- Use clean production builds so deleted articles and local drafts cannot remain as stale published output. Confirm production excludes draft routes and draft text from search/RSS/sitemap.
- Document commands, content editing, theme updates, reference differences, and actual deployment state. Do not describe an uncreated remote repository or unverified deployment as completed.
