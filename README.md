# L’s Log

基于 **Hugo + PaperMod + GitHub Pages** 的个人博客，参考 [Lil’Log](https://lilianweng.github.io/) 的阅读排版和页面结构。公开文章从空白开始；Markdown 草稿在本地编写、预览，完成后再发布。

## 本地写作

在项目根目录运行：

```sh
# 首次准备环境；已有 Hugo 和主题时可以跳过
brew install hugo
git submodule update --init --recursive

# 启动包含草稿的实时预览
./scripts/dev.sh
```

打开 [本地预览](http://localhost:1313/)，用 VS Code 或任意编辑器打开 `content/drafts/first-post.md`。保存 Markdown 后浏览器会自动刷新；开启编辑器自动保存可获得接近实时的预览。公式支持 `$...$`、`$$...$$`、`\(...\)`、`\[...\]` 和 `aligned`。

`content/drafts/` 被 Git 忽略，草稿不会随正常提交上传。这里的预览仅在本机运行；线上网站在推送后由 GitHub Actions 更新。完整步骤见 [写作与发布指南](docs/WRITING.md)。

## 构建与发布

```sh
hugo --gc --minify --panicOnWarning --cleanDestinationDir
python3 scripts/check_site.py public
```

Hugo 版本由 `.hugo-version` 和 CI 固定为 **0.164.0**；PaperMod 固定在 Git submodule 记录的 commit。`public/` 是生成产物，不提交到仓库。

`.github/workflows/hugo.yml` 在 pull request 中构建检查，在推送 `main` 后部署。仓库 **Settings → Pages → Source** 应选 **GitHub Actions**。当前生产地址配置为 [crystaluv23.github.io](https://crystaluv23.github.io/)；是否已上线以 Actions 的实际部署结果为准。

## 配置与来源

- `hugo.yaml`：站名、简介、菜单、地址和主题选项。
- `content/posts/`：正式文章；`content/faq.md`：FAQ。
- `assets/css/extended/lillog.css`：排版补充；`static/`：站点图标。
- `layouts/_partials/extend_head.html`：MathJax 公式渲染。

这是基于官方 [PaperMod](https://github.com/adityatelange/hugo-PaperMod) 的外观与行为复现，并非 Lil’Log 私有源码的副本。保留 Hugo / PaperMod 署名，不沿用原作者身份、文章或统计代码。主题采用其目录内的 MIT LICENSE。部署方式参照 [Hugo 官方文档](https://gohugo.io/host-and-deploy/deploy-to-github-pages/)。
