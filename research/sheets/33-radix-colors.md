# 33 — Radix Colors
https://www.radix-ui.com/colors · Open-source colour system (npm @radix-ui/colors, by WorkOS) · MIT · 1.7k stars (radix-ui/colors) · Read 2026-11-18

## 1. What it is
Set of 12-step colour scales (30-ish hues + 6 tinted grays), each with light/dark and alpha versions, designed so step numbers mean the same job in every hue.
## 2. How it works
Each step has a fixed UI role; swap hue or theme and components stay correct. Gray families are tinted (mauve/purple, slate/blue, sage/green, olive/lime, sand/yellow, plain gray).
## 3. Rules
- [colour] Steps 1–2 app/subtle backgrounds; 3/4/5 component bg normal/hover/pressed-selected
- [colour] Step 6 borders on non-interactive surfaces (cards, separators); 7 borders on interactive; 8 strong borders + focus rings
- [colour] Step 9 solid fills (purest, highest chroma, brand colour); step 10 its hover
- [a11y] Step 11 low-contrast text (APCA Lc 60 on step 2), step 12 high-contrast text (Lc 90)
- [colour] White text on step 9 except sky, mint, lime, yellow, amber, which need dark text
- [colour] Pair the gray whose hue is nearest the accent (sage with green) for warmth, or plain gray for neutral; tinted dark grays can clash with colourful badges
- [colour] Accent-scale text feels marketing-like, gray-scale text feels app-like
- [brand] Radix scales aren't meant to be customised; add a custom brand scale beside them, keep Radix for grays and semantic colours (error red/tomato, success green/teal, warning amber, info blue/sky)
## 4. AI tells / anti-patterns it bans
n/a
## 5. Data, assets and scripts it ships
npm package with CSS custom properties and JS objects (light, dark, alpha, P3). No runtime needed beyond CSS.
## 6. Area
design / development
## 7. Take / skip
Take: the 12-step role semantics as our token contract (name tokens by role, generate any client hue into 12 steps), the step-9 foreground rule, gray-pairing rule, and semantic-hue lists. MIT, so values may be copied into themes or Elementor global colours. Skip: using stock Radix hues as the brand colour on every site — that would make all sites look the same; derive niche-specific scales instead.
## 8. Open questions
Radix has a custom-scale generator (radix-ui.com/colors/custom) — not read; could be the human-side way to make a 12-step scale from a brand hex. Latest commit date not shown.
