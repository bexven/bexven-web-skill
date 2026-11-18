# 27 — Fontshare
https://www.fontshare.com · Website (free foundry library by Indian Type Foundry) · ITF Free Font License (FFL) · Stars n/a · read 2026-11-18 (homepage + /licenses/itf-ffl returned only the title, JS-rendered; terms below are from prior knowledge and must be verified against the FFL text in the download zip)

## 1. What it is
A free library of roughly 100 professional families from Indian Type Foundry: Satoshi, General Sans, Clash Display, Cabinet Grotesk, Switzer, Supreme, Gambetta, Erode, Zodiak, Sentient, Boska, Chillax, Tanker and others.
## 2. How it works
Download the zip (OTF/TTF/WOFF/WOFF2, often variable) or use the CSS embed from api.fontshare.com.
## 3. Rules
- [type] As I understand the ITF FFL: free for personal and commercial use, including websites, apps, print and logos. You can't redistribute, share, sell or rehost the font files as fonts, and you can't add them to other font libraries or services. It is not OFL. Re-check the FFL text before relying on any point.
- [wp] Self-hosting the WOFF2 on the client's own site counts as use, not redistribution (my reading). Upload to Elementor Custom Fonts per site. Don't put the files in a public repo, a theme sold to third parties, or a downloadable starter kit.
- [wp] The api.fontshare.com CDN has the same visitor-IP/GDPR concern as Google's CDN, so self-host.
## 4. AI tells / anti-patterns it bans
Satoshi, Clash Display, General Sans and Cabinet Grotesk are now heavily used in AI and "startup" builds. Treat them as tells unless they're chosen for a reason.
## 5. Data, assets and scripts it ships
Font files plus a licence PDF/TXT in each zip. No scripts.
## 6. Area
design (type)
## 7. Take / skip
Take: the less-used families (Gambetta, Erode, Zodiak, Sentient, Boska, Bespoke Serif, Pally, Telma) for the shortlist, with the licence column marked "ITF FFL – no redistribution". Store the files in our private repo only. Skip: CDN embeds, and bundling the files in anything public.
## 8. Open questions
- Retry failed: the licence page body didn't load. Get the exact FFL wording (self-hosting, client-work and logo clauses) from a downloaded zip before shipping.
