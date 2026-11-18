# 45 — Pexels
https://www.pexels.com · Website / stock photos + video + API · Pexels License (custom) · Stars n/a · read 2026-11-18 (/license + API docs)

## 1. What it is
Free stock photo and video library under the Pexels License, plus a free API.
## 2. How it works
Licence: free to use and edit for websites, ads, print and social, with no attribution required. Restrictions: identifiable people can't be shown "in a bad light or in a way that is offensive". You can't sell unaltered copies (prints, posters, products), can't imply that people or brands in the photo endorse you, can't use the content in a trademark or business name, and can't redistribute it on other stock or wallpaper platforms.
API: a free key comes with a Pexels account and is sent in the `Authorization` header. Limits are 200 requests per hour and 20k per month by default (higher on request if you show attribution). Show a prominent Pexels link and credit "Photo by X on Pexels" where possible. Don't copy Pexels' core functionality. The API docs don't mention hotlinking.
## 3. Rules
- [image] Use stock only as flagged placeholders in cold-outreach mockups and replace it with the client's real photos in the final build
- [image] Funeral homes: putting an identifiable stock person on a funeral, grief or illness page can count as "bad light" or a sensitive context and suggests endorsement, so use people-free or non-identifiable imagery
- [image] Never present stock people as the client's staff, customers or testimonial authors
- [image] Self-host optimised copies in mockups. Don't put stock imagery in logos or brand marks
- [image] Short Pexels videos can be fine for hero loops, but compress them, give them a poster frame and respect reduced-motion
- [tooling] If we script the API: keep the key on the server and show the Pexels link and photographer credit
## 4. AI tells / anti-patterns it bans
n/a. Our ban: generic stock hero, smiling call-centre people, and the same top search results that every competitor in the niche uses.
## 5. Data, assets and scripts it ships
Photos, videos and a REST API (needs a key). Nothing to run.
## 6. Area
design / tooling
## 7. Take / skip
Take: its licence spells out the people and endorsement limits more clearly than Unsplash's, so we use it as our baseline rule for sensitive niches, and it has video. Skip: stock in final builds when real photos exist.
## 8. Open questions
Hotlinking isn't covered in the API docs. Assume we self-host.
