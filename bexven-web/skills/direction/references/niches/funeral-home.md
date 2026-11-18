# Niche: funeral home

Status: first pass · 2026-11-18 · slug for `niche_log.py`: `funeral-home`
Constraints and content only. **This file never supplies a palette, font, hero type or section order**; those come from the direction (client's world + seeded pick). Two Bexven funeral sites may not share display font, palette family, hero type or section order.

## Audience

- **Primary:** a family arranging a funeral in the first 24-72 hours after a death. Often on a phone, often at night or early morning, often an older relative or someone helping one. Tired, distracted, possibly unfamiliar with the process.
- **Secondary:** people pre-planning their own funeral calmly, weeks or years ahead, often 60+, often on a tablet or desktop.
- **Third:** mourners looking up a service time, location or condolence page, usually from a shared link.

## Emotional register

Calm, plain, dignified, warm without being sentimental. Quiet confidence. Never sales energy, never cheerful, never urgent. Respect comes from clarity and restraint, not from ornament.

## Must-have content

- Phone number reachable 24/7, in the header on every page, tappable (`tel:`).
- "Someone has just died: what to do now" - a short step list (who to call, what happens next) plus the phone number.
- Current funeral notices / obituaries with name, dates, service time and place, and a link for flowers or condolences where offered.
- Services: burial, cremation, memorial or celebration services, repatriation if offered.
- Pre-planning (pre-arranged funerals), explained plainly.
- Costs: a "how costs work" page or price list (where local rules require a published price list, link it prominently).
- Location: address, parking, step-free access, chapel or viewing rooms.
- Staff introduced by name (with real photos only if the client supplies them).
- Contact form (short) plus phone and email beside it.

## Task paths (each within one tap or click of the homepage)

1. Someone has just died → what to do now → call.
2. Find a service time and place for a named person.
3. Send flowers or condolences.
4. Plan ahead / request information about pre-planning.
5. Understand costs.

## Trust signals

- Years serving the town, only if verified.
- Licence, registration or association memberships the client actually holds.
- Real named staff, the real building and rooms.
- Real reviews with source and date (e.g. from the Google profile); none invented, no stock faces.
- Family ownership only if true and stated by the client.

## Readability floor

- Body text ≥18px; body contrast aims for 7:1; line-height ~1.55; no thin display weights for running text.
- Tap targets ≥48px for call and primary actions.

## Imagery rules

- Priority: the client's own photos of building, rooms, grounds, vehicles and named staff.
- Stock: no identifiable people (no grieving families, no smiling staff). Prefer hands, flowers, light, architecture, landscape, details. Never imply a real family endorses the business.
- No sunset-over-water, doves, candles-on-black or lily close-ups as the hero (the rut).
- No filters, no rounded corners on place photos, no text over photos except the hero.

## Motion

Minimal: no hero entrance theatre, no scroll reveals, no autoplaying video, no parallax. A single quiet hover idea is enough.

## Schema and local SEO

- JSON-LD type `FuneralHome` (a LocalBusiness subtype) with real name, address, geo, telephone, opening hours (24/7 phone noted), URL, `sameAs` (Google profile, Facebook), image.
- NAP identical on site, schema and Google profile.
- Obituary / notice pages are crawlable HTML (not PDFs, not iframes from a third-party notices widget unless there is an HTML fallback), each with its own URL and title "Name - funeral notice - Town".
- Title pattern: "<Business> - funeral director in <Town>". Local names (town, district, cemetery, crematorium) used in copy.

## Copy no-gos

- Euphemism stacks ("passed on to their heavenly journey"); "celebration of life" as a slogan.
- Urgency or discount language ("limited offer", "save 20%").
- Condolence clichés as headings ("In loving memory", "Forever in our hearts" as section titles).
- Emoji, exclamation marks, countdowns.
- "Compassionate care you can trust", "Honoring lives with dignity" (the rut headlines).

## Design no-gos

- Popups, chat bubbles that open by themselves, cookie walls covering the phone number.
- Script fonts for headings; tracked all-caps Trajan-style headings.
- Experimental or novelty display faces.
- Saturated violet; gold-foil gradients; dark mode by default.
- Auto-rotating testimonial sliders.
- Deep low-chroma plums, aubergines, greens or greys **are** allowed when taken from the client's world.

## The rut (the page this niche always ships)

Full-width sunset, lilies or candle photo with a dark overlay; centred serif headline "Honoring lives with dignity and compassion"; cream or white ground with gold, burgundy or navy accent; Playfair Display or a script face plus a stock sans; sections Welcome → Services (3 icon cards: burial, cremation, pre-planning) → Testimonials slider → Obituaries link → Contact; dove or candle icons; "Contact us" and "Learn more" buttons; fade-in on every section. Its obvious opposite (black, bold, edgy) is also a category guess and wrong for this audience.
