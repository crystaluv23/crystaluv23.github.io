# L’s Log — Lil’Log reproduction

## Goal

Reproduce the reading experience and page structure of https://lilianweng.github.io/ using Hugo, the upstream PaperMod theme, and GitHub Pages. Keep the theme as a Git submodule pinned by the parent repository. Do not introduce a custom application framework or redesign the reference.

## Scope

- Site name: L’s Log. Author: L. Reference identity, analytics, and original articles are not reused.
- Match the reference's system font, neutral palette, compact welcome section, article cards, metadata labels, navigation (Posts / Archive / Search / Tags / FAQ), article typography, table of contents, and Hugo / PaperMod footer.
- Support light/dark appearance, responsive layouts, title/body search, tag filtering, yearly/monthly archives, Markdown articles, RSS, sitemap, syntax highlighting, and code copying.
- Include six explicitly identified sample articles. New articles are Markdown files under `content/posts/`.
- Main reading width 720 px; navigation width 1024 px; desktop gutter 24 px; mobile gutter 14 px. Preserve readable, accessible layout on narrow screens.
- No third-party analytics, comments provider, newsletter, or invented personal links.

## Delivery and validation

- Source lives at the workspace root. Hugo version is pinned in `.hugo-version` and CI.
- GitHub Actions builds pull requests and deploys successful main-branch builds to GitHub Pages. The build uses the Pages-provided base URL for deployment.
- Check a production build, generated internal links/assets, search index, RSS, expected routes, and absence of reference-author identity.
- Inspect desktop and mobile preview when browser infrastructure is available. Verify search, theme persistence, archive/tag navigation, article TOC, and copy behavior.
- Document commands, content editing, theme updates, reference differences, and actual deployment state. Do not describe an uncreated remote repository or unverified deployment as completed.
