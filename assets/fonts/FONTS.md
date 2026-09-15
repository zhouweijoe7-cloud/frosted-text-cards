# Font setup

This repository does not redistribute third-party font files.

The renderer searches common font folders on macOS, Windows, and Linux. For consistent typography, set these environment variables to locally licensed font files:

```bash
export FROSTED_FONT_CN_BOLD="/path/to/chinese-display-font.ttf"
export FROSTED_FONT_CN_BODY="/path/to/chinese-body-font.ttf"
export FROSTED_FONT_LATIN="/path/to/latin-font.ttf"
export FROSTED_FONT_LATIN_DISPLAY="/path/to/latin-display-font.ttf"
export FROSTED_FONT_SERIF="/path/to/serif-font.ttf"
```

Local font aliases are also supported:

- `FrostedCNDisplay.ttf`
- `FrostedCNBody.ttf`
- `FrostedLatin.ttf`
- `FrostedLatinDisplay.ttf`
- `FrostedSerif.ttf`

Place aliases in this directory. Confirm each font license before committing or distributing a font file.
