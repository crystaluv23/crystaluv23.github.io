# 写作与发布

## 打开编辑器和预览

在项目根目录启动：

```sh
./scripts/dev.sh
```

保持终端运行，浏览器打开 [http://localhost:1313/](http://localhost:1313/)。用 VS Code 或任意文本编辑器打开 `content/drafts/first-post.md`，将编辑器和浏览器并排放置。若已安装 VS Code 的命令行工具，也可运行：

```sh
code content/drafts/first-post.md
```

修改并保存文件后，Hugo 会重新渲染，浏览器自动刷新并导航到修改的页面。VS Code 可在 **File → Auto Save** 开启自动保存，减少手动保存操作。预览仍以文件保存为触发条件。

启动脚本包含 `-D --disableFastRender --renderToMemory --navigateToChanged`：显示草稿、重新渲染修改、在内存中提供页面，并定位修改的文章。端口是 `1313`。结束写作后，在终端按 `Ctrl+C` 停止服务。

## 草稿与文章头部

本机已准备 `content/drafts/first-post.md` 作为第一篇草稿。文件开头的 `---` 区域是文章信息；保留日期，修改标题、摘要与标签：

```yaml
---
title: "我的第一篇笔记"
date: "2026-10-19"
description: "一句话说明这篇文章写什么"
tags: ["笔记"]
draft: true
type: posts
---
```

实际文件中的 `date` 请设置为真实写作时间。未来日期的文章默认不显示，预览脚本也不包含显示未来文章的 `-F`。

`draft: true` 使文章仅在开启草稿的预览中出现；普通生产构建会排除它。`type: posts` 让位于草稿目录的文章沿用文章模板。

`content/drafts/` 已加入 `.gitignore`，正常 `git add` 不会上传这个目录；不要用 `git add -f` 强制加入草稿。`draft: true` 只控制网站是否生成页面，不能隐藏已被提交到公开仓库的源文件。因此，把未发布内容保留在被忽略的草稿目录中。

新建下一篇草稿可以运行：

```sh
hugo new content drafts/another-note.md
```

检查新文件保留 `draft: true`，并设置 `type: posts`。标题和正文使用中文或英文均可。

## Markdown 与公式

正文写在文章头部之后。`##`、`###` 标题会构成文章目录；链接、列表、引用、代码块均使用普通 Markdown 语法。代码块注明语言即可高亮，例如以三个反引号和 `python` 开始。

MathJax 已启用，无须为每篇文章单独安装。以下示例可以直接粘贴到文章正文；本指南位于 `docs/`，不会作为博客文章发布。

行内公式：

```markdown
我们最小化损失 $L(\theta)$，学习率记作 \(\eta\)。
```

独立成行的公式：

```markdown
$$
\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)
$$
```

也可以使用 `\[` 与 `\]`：

```markdown
\[
\mathbb{E}[X] = \sum_x x\,p(x)
\]
```

多行对齐放在块公式内，使用 `aligned`、`&` 和 `\\`：

```markdown
$$
\begin{aligned}
L(\theta) &= \frac{1}{n}\sum_{i=1}^{n}(y_i-f_\theta(x_i))^2 \\
\theta_{t+1} &= \theta_t - \eta\nabla L(\theta_t)
\end{aligned}
$$
```

文章正文中不要把需要渲染的公式放入反引号或代码块；上面的代码块仅用于展示写法。MathJax 支持数学公式语法，不是完整的 LaTeX 文档编译器，无须写 `\documentclass` 或 `\begin{document}`。脚本从 CDN 加载，首次访问需要联网；保存后页面刷新，公式会重新排版。

## 发布一篇完成的文章

先将草稿移动到公开文章目录：

```sh
mkdir -p content/posts
mv content/drafts/first-post.md content/posts/first-post.md
```

编辑移动后的文件，把 `draft: true` 改为 `draft: false`，检查标题、日期、摘要和标签。`type: posts` 可以保留。继续用本地预览检查正文、公式和移动后的文章链接。

然后执行不包含草稿的生产构建。`--cleanDestinationDir` 会清理旧页面，避免已删除或移动的内容残留在生成目录：

```sh
hugo --gc --minify --panicOnWarning --cleanDestinationDir
python3 scripts/check_site.py public
```

检查通过后，只加入并提交这篇文章，再推送：

```sh
git add -- content/posts/first-post.md
git diff --cached -- content/posts/first-post.md
git commit -m "Publish first post" -- content/posts/first-post.md
git push origin main
```

这些命令以当前仓库使用 `main` 为前提。若文章引用新图片，也需检查并明确加入对应图片文件。不要提交 `public/`；它会由 GitHub Actions 重新生成。

推送后，在仓库 **Actions** 中确认构建和部署成功，再访问 [线上网站](https://crystaluv23.github.io/)。本地浏览器自动刷新不代表线上已更新；线上版本只会在推送触发部署并成功完成后改变。上线还要求仓库已配置 GitHub Pages，且发布来源为 **GitHub Actions**。

## 预览没有变化时

- 确认文件已保存，终端中的 Hugo 服务仍在运行，浏览器地址是 `localhost:1313`。
- 查看终端是否报告 YAML 或 Markdown 构建错误；文章头部的缩进和引号需要有效。
- 草稿应保留 `draft: true`，启动方式使用 `./scripts/dev.sh`；检查 `date` 没有设为未来。
- 公式没有排版时，检查定界符是否成对、是否误放在代码块中，以及浏览器能否加载 MathJax CDN。
- `1313` 端口已占用时，先在之前启动预览的终端按 `Ctrl+C`，再重新运行脚本。
