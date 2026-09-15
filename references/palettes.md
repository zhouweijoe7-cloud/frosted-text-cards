# 配色令牌

生成图片前向用户展示全部配色。用户已经指定配色编号时直接使用，无需重复确认。

| 编号 | 名称 | 基调 | 推荐内容 |
|---|---|---|---|
| P01 | 极光珊瑚 | 暖白、珊瑚、炭灰 | 生活方式、创意、轻知识 |
| P02 | 冰川蓝 | 冰蓝、雾白、深蓝 | 教程、效率工具、理性知识 |
| P03 | 鼠尾草 | 米白、灰绿、墨绿 | 方法论、成长、自然主题 |
| P04 | 夜紫雾 | 深紫、雾紫、冷白 | 创意、未来感、数字文化 |
| P05 | 琥珀烟 | 深棕、琥珀、奶油白 | 叙事、复古、温暖经验 |
| P06 | 翡翠夜 | 墨绿、翡翠、冷白 | 科技、音乐、沉浸氛围 |
| P07 | 黑曜红 | 黑灰、暗红、银白 | 警示、冲突、强结论 |
| P08 | 墨蓝金 | 深海军蓝、哑金、象牙白 | 商业、专业、品牌内容 |
| P09 | 银白雾 | 银白、浅灰、石墨 | 极简、作品集、轻盈知识 |
| P10 | 石墨灰 | 深灰、中灰、冷白 | 通用暗调、编辑感、纪实 |
| P11 | 纯黑冰 | 纯黑、冰白、银灰 | 高对比、展览、强视觉封面 |
| P12 | 蓝黑钢 | 蓝黑、钢灰、乳白 | 科技、剪辑、音乐、专业教程 |

## 自动推荐

- 科技、音乐、剪辑和专业教程：优先 P12，其次 P02、P08。
- 创意、未来感和数字文化：优先 P04、P06。
- 温暖叙事、经验分享和生活方式：优先 P01、P05、P03。
- 对比、警示和强结论：优先 P07、P11。
- 极简、作品集和黑白灰偏好：优先 P09、P10、P11、P12。

## 精确令牌

```yaml
P01: {background: "#ECE7E1", glass: "#F3EDEA", ink: "#262A2E", muted: "#646A70", accent: "#C77B70", edge: "#FFFFFF"}
P02: {background: "#DCE7ED", glass: "#E9F1F4", ink: "#17242E", muted: "#52636E", accent: "#4E7894", edge: "#FFFFFF"}
P03: {background: "#E7E5DA", glass: "#EEF0E7", ink: "#24302B", muted: "#606A63", accent: "#718775", edge: "#FFFFFF"}
P04: {background: "#201B2C", glass: "#393146", ink: "#F2EEF5", muted: "#B7ABBF", accent: "#8F73A7", edge: "#DCD2E4"}
P05: {background: "#2A211D", glass: "#44352B", ink: "#F1E8DC", muted: "#C1AE98", accent: "#B57B45", edge: "#E3D4C1"}
P06: {background: "#132823", glass: "#244039", ink: "#ECF3F0", muted: "#A7BBB4", accent: "#4E8B78", edge: "#C9DBD5"}
P07: {background: "#171719", glass: "#303034", ink: "#F2F2F2", muted: "#B5B5B8", accent: "#A94E50", edge: "#D7D7D8"}
P08: {background: "#17212E", glass: "#2B3847", ink: "#F2EEE3", muted: "#B9B3A4", accent: "#A58A55", edge: "#D9D1BE"}
P09: {background: "#ECEDEA", glass: "#F6F6F2", ink: "#25282B", muted: "#676C70", accent: "#92999D", edge: "#FFFFFF"}
P10: {background: "#26292D", glass: "#41454A", ink: "#F0F1F2", muted: "#B1B4B7", accent: "#737A80", edge: "#D2D5D7"}
P11: {background: "#0C0D0E", glass: "#242628", ink: "#FAFAF8", muted: "#BFC2C4", accent: "#D9DDE0", edge: "#FFFFFF"}
P12: {background: "#151A20", glass: "#28313A", ink: "#EFF2F2", muted: "#AEB7BC", accent: "#617483", edge: "#C7D2D8"}
```

所有背景 Alpha 为 236，玻璃 Alpha 为 168。卡片四角保留完全透明区域，主体内部保留半透明像素。
