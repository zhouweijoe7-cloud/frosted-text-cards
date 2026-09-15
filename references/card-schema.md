# 卡片数据结构

每张卡使用以下字段。字段约束用于保持文案精准和视觉可排版。

```yaml
series:
  source_summary: 原文核心主题，1 句话
  audience: 主要读者
  tone: 专业、克制、清晰
  palette: 用户选择的配色编号
  canvas: 1080x1350
  format: png_rgba

cards:
  - id: 两位序号
    role: hook | concept | method | contrast | feature | process | conclusion
    eyebrow: 2-12 个字符的栏目或场景标签
    headline: 2-10 个汉字的核心标题
    support: 最多 28 个汉字，允许两行
    keywords: 1-4 个关键词
    english_anchor: 1-3 个英文单词，用作背景裁切字或技术标签
    metadata: 简短编号、音调、扩散率或栏目代码
    layout: L01 | L03 | L04 | L07 | L08 | L09 | L10
    palette: 配色编号
```

## 提炼规则

- 一张卡只保留一个可复述的重点。
- 标题优先使用名词短语、动作短语或明确结论。
- 辅助文字补充标题含义，不重复标题。
- 保留原文中的专有名词、Key、B 大调、BGM 等关键术语。
- 禁止添加原文没有提供的功能、效果、数据或承诺。
- 相邻卡片避免重复表达；需要递进时使用“问题—概念—方法—结果”的顺序。
- 口语稿中的重复词、结尾寒暄、转义字符和填充语不进入卡片正文。

## 当前示例文案的卡片规划

| ID | Role | Headline | Support | Layout |
|---|---|---|---|---|
| 01 | hook | 找歌难 | 刷到喜欢的音乐，却难确认歌名和版权 | L03 |
| 02 | feature | AI 识曲 | 识别歌名、相似音乐与整首歌的调性 | L07 |
| 03 | concept | 调性 Key | 音乐衔接是否自然，调性是关键变量 | L08 |
| 04 | method | 同调衔接 | 拼接多首 BGM，优先选择相同调性的音乐 | L01 |
| 05 | contrast | 割裂与自然 | 异调切换容易突兀，同调切换更连贯 | L04 |
| 06 | process | 一秒筛选 | 识别参考曲调性，再筛选曲库中的同调音乐 | L09 |
| 07 | conclusion | 选曲更高效 | 统一音乐、音效与氛围的调性，提升整体质感 | L10 |
