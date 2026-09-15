# 渲染规范

## 输入

渲染脚本接收符合 `card-schema.md` 的 JSON 文件。示例位于 `references/example-series.json`。

## 命令

```bash
python3 scripts/render_cards.py --input references/example-series.json --output <output-directory>
python3 scripts/render_cards.py --input references/example-series.json --output <output-directory> --palette P09
```

如果当前 Python 缺少 Pillow，运行 `python3 -m pip install -r requirements.txt`。

字体通过 macOS、Windows 和 Linux 常见目录自动发现。需要固定字体时，可设置：

- `FROSTED_FONT_CN_BOLD`
- `FROSTED_FONT_CN_BODY`
- `FROSTED_FONT_LATIN`
- `FROSTED_FONT_LATIN_DISPLAY`
- `FROSTED_FONT_SERIF`

环境变量的值应为本机合法授权字体文件的绝对路径。也可以把字体放入 `assets/fonts/` 并使用 `FrostedCNDisplay.ttf` 等约定文件名。

## 输出

- 每张卡为 1080 × 1350 px 的 RGBA PNG。
- 文件名格式为 `01-l03-find-music.png`。
- 同时生成 `contact-sheet.png`，用于检查系列节奏。
- Alpha 通道必须同时包含 0、半透明值和接近不透明的值。
- 卡片文字通过本地字体绘制，中文内容必须与输入 JSON 完全一致。

## 视觉检查

- 标题不得越过安全边距或被磨砂边缘截断。
- 辅助文字最多两行，行间距保持疏朗。
- 玻璃层与背景字景之间需要有可辨识的折射与透明关系。
- L04 的两种状态、L09 的多个节点必须清晰区分。
- 联系表缩小后，每张卡仍能看出不同结构和共同的 P12 系列基因。
- 公共仓库不附带第三方字体文件；发布者与使用者需要自行确认字体许可证。
