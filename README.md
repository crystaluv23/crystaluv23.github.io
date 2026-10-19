# L’s Log

基于 **Hugo + PaperMod + GitHub Pages** 的个人博客，参照 [Lil’Log](https://lilianweng.github.io/) 当前站点复现排版与页面结构。

## 本地运行

```sh
# 首次拉取项目时同时拉取主题
git clone --recurse-submodules https://github.com/crystaluv23/crystaluv23.github.io.git
cd crystaluv23.github.io

# macOS；CI 使用 .hugo-version 中固定的版本
brew install hugo
hugo server --renderToMemory
```

打开 http://localhost:1313/ 。当前实现使用 Hugo **0.164.0**；PaperMod 固定在 Git submodule 记录的 commit。

## 写一篇文章

```sh
hugo new content posts/my-first-post.md
hugo server -D --renderToMemory
```

编辑 `content/posts/my-first-post.md`：

```yaml
---
title: "我的第一篇笔记"
date: "2026-10-19T18:00:00+08:00"
description: "一句话摘要"
tags: ["学习", "笔记"]
draft: false
---
```

下方直接写 Markdown 正文。`draft: true` 的文章只有使用 `-D` 才显示；未来日期默认不发布。摘要可通过正文中的 `<!--more-->` 指定。中文阅读时间已启用 CJK 字数支持。

当前六篇文章的 `sample: true` 与正文首句都明确标注示例。正式使用时可删除示例 Markdown 文件并写入自己的文章，归档、标签、搜索与 RSS 会自动更新。

公式支持 `$...$`、`$$...$$`、`\(...\)` 和 `\[...\]`，由固定版本 MathJax 3.2.2 渲染。文章 frontmatter 设置 `math: false` 可停止加载公式脚本。代码高亮由 Hugo 在构建时完成。

## 个性化配置

- `hugo.yaml`：站名、作者、简介、菜单、网站地址与主题选项。
- `content/faq.md`：个人介绍及常见问题。
- `static/favicon.svg`：站点图标。
- `assets/css/extended/lillog.css`：相对于上游 PaperMod 的样式补充。
- `layouts/_partials/post_meta.html`：与参考站一致的元信息标签。

## 检查与发布

```sh
hugo --gc --minify --panicOnWarning
python3 scripts/check_site.py public
```

GitHub Actions 配置在 `.github/workflows/hugo.yml`。仓库的 **Settings → Pages → Build and deployment → Source** 使用 **GitHub Actions**。推送 `main` 后构建并发布；pull request 只构建和检查。

```sh
git add .
git commit -m "Write a new post"
git push origin main
```

生产地址配置为 https://crystaluv23.github.io/ 。发布是否完成应以 GitHub Actions 的部署结果为准。构建产物 `public/` 不提交；主题和源码由 Git 管理。更换仓库或域名时更新 `hugo.yaml` 中的 `baseURL`，部署流程也会使用 GitHub Pages 提供的实际地址。

## 复现范围与来源

参考站只公开生成后的 HTML/CSS，未公开当前 Hugo 配置；因此这是基于官方 PaperMod 的样式和行为复现，并非其私有源码的副本。保留了文章列表、归档、搜索、标签、FAQ、主题切换、文章目录、代码复制、公式、RSS 和原有 Hugo / PaperMod 署名。

主要匹配：720px 阅读宽度、系统字体、16px 正文、24px 卡片标题、36px 文章标题、灰白配色、两行摘要、紧凑桌面欢迎区和元信息格式。手机端修正原站固定 logo 可能移出屏幕的问题。作者身份、文章、社交账号和统计代码不沿用。

PaperMod 遵循主题目录内的 MIT LICENSE；没有直接修改主题源文件。主题版本更新后应重新验证排版：

```sh
git submodule update --remote --merge themes/PaperMod
hugo --gc --minify --panicOnWarning
python3 scripts/check_site.py public
```

参考：[Lil’Log](https://lilianweng.github.io/) · [PaperMod](https://github.com/adityatelange/hugo-PaperMod) · [Hugo 部署文档](https://gohugo.io/host-and-deploy/deploy-to-github-pages/)
