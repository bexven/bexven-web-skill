# 34 — OKLCH picker
https://oklch.com · Website + open source (evilmartians/oklch-picker, by Andrey Sitnik and Roman Shamin) · MIT · 2.0k stars · Read 2026-11-18

## 1. What it is
Colour picker/converter for OKLCH (Lightness, Chroma, Hue, Alpha) that shows sRGB, P3 and Rec2020 gamut edges and an sRGB fallback for out-of-gamut colours.
## 2. How it works
Sliders for L/C/H/A; paste HEX/RGB/HSL to convert; 3D gamut view; "closest fallback by chroma in sRGB". Companion article "OKLCH in CSS: why we moved from RGB and HSL" and the Harmonizer tool (OKLCH + APCA palettes).
## 3. Rules
- [colour] Build palettes in OKLCH, not HSL: its L is perceptual, so equal L steps look equally light across hues and contrast stays predictable
- [colour] Same-weight colour set = fix L and C, rotate H; shades = vary L only
- [colour] Max chroma depends on hue and lightness — check every colour is inside sRGB (or provide one) before use
- [code] Write an sRGB-safe value first, then override with wider P3 values inside @media (color-gamut: p3)
- [code] Derive hover/secondary variants with relative colour syntax, e.g. oklch(from var(--accent) calc(l + 0.1) c h); use decimals, not %, in calc
- [code] Keep colours as role-named CSS custom properties; swap values per theme
- [tooling] Lint with stylelint-gamut to flag out-of-gamut or unguarded P3 colours
- [perf] oklch() and relative colours work in current major browsers; check support data for older targets (Elementor client audiences)
## 4. AI tells / anti-patterns it bans
n/a (implicitly: HSL-generated scales with uneven perceived lightness)
## 5. Data, assets and scripts it ships
Source of the picker (Node/JS web app); conversion maths also available via libraries such as culori (not checked).
## 6. Area
design / development / tooling
## 7. Take / skip
Take: OKLCH as the agent's working colour space — the agent can compute 12-step scales (Radix roles) from a brand hue by setting L targets per step and capping C to the sRGB gamut, then emit hex fallbacks. This is an agent-usable method; the website itself is a human check tool. Skip: shipping raw P3/oklch-only values without hex fallbacks in WordPress/Elementor global colours (Elementor colour pickers store hex).
## 8. Open questions
Browser-support link points to a CSSWG issue, not a support table. SUGGESTED: Harmonizer - https://harmonizer.evilmartians.com - generates OKLCH+APCA consistent-contrast palettes, close to our need. Whether Elementor accepts oklch() in globals unverified.
