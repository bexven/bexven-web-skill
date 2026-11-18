# Components

Load at build step 5. Conventional in where things are and how they behave; distinctive in type, colour, proportion and composition. All values come from tokens.

## 1. States (every interactive element)

Default, hover (gated), `:focus-visible`, `:active`, disabled; plus loading, error, empty where relevant.
- Hover/focus/active change colour, underline, border or shadow, with more contrast than rest.
- All `:hover` inside `@media (hover: hover) and (pointer: fine)`. Touch gets `:active` (`scale: 0.97`, 100–160ms).
- No lift/zoom/shadow growth on cards. The site's one hover-motion idea (named in DESIGN.md) moves a child: image inside its frame, an underline drawing in, an arrow. Never the card box.
- Unlinked things never react to hover. Anything that looks clickable is clickable.
- Same role, same style, site-wide.

## 2. Header and nav

- Logo top-left, links home. Main nav 5–6 short nouns in the customers' words (max 7), contact last. Secondary links go to the footer.
- Phone as a `tel:` link in the header on every page, same position site-wide. Funeral homes: the 24/7 number is visible in the header at every width.
- Sticky header allowed if opaque. No blur, shrink, hide-on-scroll, floating pill.
- `aria-current="page"` on the current link.
- Mobile menu: a `<button aria-expanded aria-controls>` with an accessible name; full-screen or sheet; focus moves in, is trapped, Escape closes, focus returns to the toggle. Use the APG disclosure/dialog pattern; never a hover menu.
- Mobile call/quote bar: one bar, within thumb reach, appears after the hero CTA scrolls out (IntersectionObserver), ≥48px tall, respects `env(safe-area-inset-bottom)`, never covers focused elements (add `padding-bottom` to body when shown).

## 3. Footer

Full NAP, hours, service area, legal links (privacy, imprint/KvK where relevant), one quiet photo-credit line. Same `tel:` and `mailto:` as the header. Not a sitemap dump; no newsletter box unless the client has one.

## 4. Calls to action

- One primary per viewport, at most one secondary (visually quieter: text link or outline). Never two equal primaries.
- Main action worded identically in nav, hero, closing section and phone bar ("Call 0475 12 34 56", "Request a quote").
- Key CTA in the hero and the closing section.
- Verb + object, sentence case. Never "Get started", "Learn more", "Read more", "Submit", "Click here".
- No "→" glyph on buttons unless it is the site's one hover idea.
- Mobile primary CTA and phone button ≥48px tall; all targets ≥44px with ≥8px gaps.
- Place real proof (review, credential, years if verified) next to the CTA.

## 5. Cards

- Only when the box means something (a linked item, a grouped record). Max 2 card layouts per page; no 3-equal-icon-card grid by default; no bento.
- Barely there: one surface step or a 1px rule, radius from the radius language, no resting blur shadow, no coloured left border, never card in card.
- Linked card: whole card clickable via a stretched link on the heading's `<a>` (`::after { content:""; position:absolute; inset:0 }`), not a wrapping `<a>` around block content with buttons inside.
- Align shared parts across side-by-side cards: titles, prices, buttons pinned to the bottom (`display:grid; grid-template-rows: subgrid` or flex column + `margin-top:auto`).
- Often a list with hairline dividers or a table beats cards. Spec data (tolerances, sheet sizes, materials) goes in a real `<table>` with tabular figures.

## 6. Reviews and proof

- Real quotes only: text, name or initials, date, source ("Google, March 2026"), ideally a link to the source. Never invented, never "lightly edited", never stock headshots, never a rating that is not public.
- No reviews available → leave the section out and list it under Known gaps. Never write three polished placeholder testimonials.
- No "Most popular" badges, fake logo strips, star rows without a source.
- Markup: `<figure><blockquote><p>…</p></blockquote><figcaption>Name, <cite>Google</cite>, <time datetime="2026-03">March 2026</time></figcaption></figure>`.
- Do not add `aggregateRating` to JSON-LD for self-hosted reviews.

## 7. NAP / contact block

```html
<address class="nap">
  <strong translate="no">Uitvaartzorg Peeters</strong><br>
  Kerkstraat 12<br>2440 Geel<br>
  <a href="tel:+3214123456">014 12 34 56</a><br>
  <a href="mailto:info@example.be">info@example.be</a>
</address>
```
- Name, address and phone exactly as on the prospect's site/Google profile, identical everywhere (header, footer, contact, JSON-LD). Display the local format; href in international `+` format.
- Address links to a maps search (`https://www.google.com/maps/search/?api=1&query=…`) or sits next to the map facade.
- Hours in a `<dl>` or `<table>` with `<time>` and tabular figures; en dash ranges (9:00–17:00). Note "24/7 by phone" in words where true.
- Parking and step-free access for funeral homes and anything older visitors attend.
- Placeholder email in mocks only if the real one is unknown, marked `data-assumed`.

## 8. Maps

Never an iframe on page load. Facade: a static self-hosted map image (or an illustrated location sketch) with `width/height`, the address as text, an "Open in Maps" link, and optionally a button that injects the embed on click. Reserve its box with `aspect-ratio`.

## 9. Carousels, popups, sticky UI

- No auto-rotating carousels, testimonial sliders or marquees. If content truly overflows: a horizontal `scroll-snap-type: x mandatory` row, visible prev/next buttons, keyboard scrollable (`tabindex="0"` on the region with a label), no hidden pagination dots as the only control.
- Anything moving >5s needs a pause control.
- No popups or modals before the visitor has read anything; no self-opening chat; no back-to-top clutter; no "New" pills; no theme toggle as decoration.
- Cookie banner (only if tracking exists): reserve space, never covers the CTA or pushes content after load.

## 10. Forms (contact and quote)

### Rules
1. **Fields:** only what the job needs. Contact = name, phone or email (one required, other optional), message. Quote = + service, location/town, timing; fabrication adds quantity, material, needed-by date, drawing upload. Every extra field needs a reason.
2. **Labels:** a visible `<label for>` on every field, above the field, 6–8px gap. Placeholder is never the label; if used it shows a format example ending in "…" and meets contrast.
3. **Types:** `type="email"` (+ `spellcheck="false"`, `autocapitalize="off"`), `type="tel"`, `type="date"`, `type="file"`, `<textarea>` for messages, `inputmode="numeric"` for quantities/postcodes.
4. **Autocomplete:** `name` (or `given-name`/`family-name`), `email`, `tel`, `street-address`, `postal-code`, `address-level2`, `organization`. Message and service fields `autocomplete="off"` only if a browser keeps misfilling. Do not name non-login fields `username`/`password`.
5. **Required:** mark in text. Default: mark the minority. If most fields are required, write "(optional)" after the optional ones; otherwise "(required)". Never colour or asterisk alone. Use the `required` attribute + `novalidate` on the form so our messages, not the browser bubbles, show.
6. **Sizing:** field font-size ≥16px (no iOS zoom), height ≥48px, full-width up to ~32rem; message textarea ≥6 rows.
7. **Hints** under the label, linked via `aria-describedby`. File fields state formats and size limit before the field ("PDF, DWG, DXF or STEP, up to 20 MB").
8. **Validation timing:** never pre-disable submit. Validate on submit; after a field has shown an error, re-validate it on `input`/`blur` so the error clears as soon as it is fixed. No errors while the user is still typing a field for the first time.
9. **Per-field errors:** text under the field (what is wrong + how to fix), an icon + colour + text, `aria-invalid="true"`, error id appended to `aria-describedby`. "Enter an email address like name@example.be", not "Invalid input", never "Oops".
10. **Error summary:** on submit with errors, show a summary at the top of the form (`role="alert"`, heading "There is a problem with 2 fields") linking to each field, and move focus to it (short forms: focus the first invalid field instead).
11. **Accept messy input:** spaces, dashes, brackets, `+` in phone numbers; trim; never block paste.
12. **Submitting:** button stays enabled until the request starts, then `aria-disabled="true"`, label changes to "Sending…" with a spinner, double-submit blocked.
13. **Success:** only after a real 2xx. Replace the form with a message in a polite live region (or redirect to a thank-you page) that says what happens next and when: "Thank you, Anna. We will call you back within one working day." No exclamation marks. Move focus to the message heading.
14. **Failure:** keep every value the visitor typed, say it did not send, and offer the phone and email right there.
15. **Fallback contact:** a `tel:` and `mailto:` link next to the form, always ("Prefer to talk? Call 014 12 34 56").
16. **Spam:** an off-screen honeypot (`aria-hidden="true"`, `tabindex="-1"`, `autocomplete="off"`) plus a time-to-submit check (reject under ~3s, server-side). No CAPTCHA by default; if spam persists, a privacy-friendly challenge (e.g. Turnstile) and mention it in the privacy text.
17. **Consent line:** one plain sentence under the submit button saying what the data is used for, linking the privacy policy. Checkbox only for a newsletter opt-in or where law requires it; never pre-ticked.
18. **Submit label names the result:** "Send message", "Request a quote", "Ask for a call back". Never "Submit"/"Send".
19. **Endpoint:** static Vercel mock posts to a working endpoint (form service or a Vercel function) or shows a clearly labelled demo state ("Demo: this form is not connected yet. Call 014 12 34 56."). Never `action="#"`, never a fake success. In WordPress: Elementor Pro Forms or the site's form plugin, delivery tested.
20. **Multi-step** only for long quotes: "Step 2 of 3", earlier answers visible and editable.

### Reference snippet
Token-driven and deliberately plain; the look comes from DESIGN.md tokens (type, radius language, accent), not from this file. Adapt layout to the section (e.g. form in a 3fr column, fallback contact in the 2fr column).

```html
<form class="contact-form" action="/api/contact" method="post" novalidate data-form>
  <div class="form-summary" role="alert" tabindex="-1" hidden data-summary>
    <h3 class="form-summary__title">There is a problem with <span data-count></span></h3>
    <ul data-summary-list></ul>
  </div>

  <div class="field">
    <label for="cf-name">Your name</label>
    <input id="cf-name" name="name" type="text" autocomplete="name" required>
    <p class="field__error" id="cf-name-err" hidden></p>
  </div>

  <div class="field">
    <label for="cf-phone">Phone number</label>
    <p class="field__hint" id="cf-phone-hint">We call back on working days, 9:00–17:00.</p>
    <input id="cf-phone" name="phone" type="tel" autocomplete="tel" required
           aria-describedby="cf-phone-hint">
    <p class="field__error" id="cf-phone-err" hidden></p>
  </div>

  <div class="field">
    <label for="cf-email">Email <span class="field__opt">(optional)</span></label>
    <input id="cf-email" name="email" type="email" autocomplete="email"
           spellcheck="false" autocapitalize="off">
    <p class="field__error" id="cf-email-err" hidden></p>
  </div>

  <div class="field">
    <label for="cf-msg">How can we help?</label>
    <textarea id="cf-msg" name="message" rows="6" required></textarea>
    <p class="field__error" id="cf-msg-err" hidden></p>
  </div>

  <!-- honeypot: off-screen, not display:none -->
  <div class="hp" aria-hidden="true">
    <label for="cf-website">Leave this empty</label>
    <input id="cf-website" name="website" type="text" tabindex="-1" autocomplete="off">
  </div>
  <input type="hidden" name="t0" data-t0>

  <button class="btn btn--primary" type="submit" data-submit>
    <span data-label>Ask for a call back</span>
  </button>
  <p class="form-consent">We use your details only to answer this request.
    <a href="/privacy">How we handle your data</a>.</p>
  <p class="form-status" role="status" aria-live="polite" data-status></p>
</form>
<p class="form-alt">Prefer to talk? <a href="tel:+3214123456">014 12 34 56</a>
  or <a href="mailto:info@example.be">info@example.be</a></p>
```

```css
@layer components {
  .contact-form { display: grid; gap: var(--space-6, 24px); max-width: 32rem; }
  .field { display: grid; gap: var(--space-2, 8px); }
  .field label { font: var(--text-label--weight, 500) var(--text-label, 1rem)/1.3 var(--font-body); color: var(--ink); }
  .field__hint, .field__opt { color: var(--color-text-muted); font-size: 0.9375rem; font-weight: 400; }
  .field input, .field textarea {
    font: inherit; font-size: max(1rem, 16px); color: var(--ink);
    min-height: 3rem; padding: var(--space-3, 12px) var(--space-4, 16px);
    background: var(--color-field, var(--paper));
    border: 1px solid var(--color-border-strong, var(--rule));   /* field border ≥3:1 vs ground */
    border-radius: var(--radius-field, var(--radius-sm, 0));
    transition: border-color var(--dur-press, 120ms) var(--ease-out, ease-out);
  }
  .field textarea { min-height: 9rem; resize: vertical; }
  .field input:focus-visible, .field textarea:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
  .field [aria-invalid="true"] { border-color: var(--color-danger); border-width: 2px; }
  .field__error { display: flex; gap: var(--space-2, 8px); color: var(--color-danger-text, var(--color-danger)); font-weight: 500; }
  .field__error::before { content: ""; inline-size: 1em; block-size: 1em; flex: none; margin-top: 0.2em;
    background: currentColor; mask: url("/img/icon-alert.svg") center / contain no-repeat; }
  .form-summary { padding: var(--space-4, 16px); border: 2px solid var(--color-danger); border-radius: inherit; }
  .form-summary a { color: var(--color-danger-text, var(--color-danger)); }
  .hp { position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden; }
  .form-consent, .form-alt { font-size: 0.9375rem; color: var(--color-text-muted); max-width: 60ch; }
  [data-submit][aria-disabled="true"] { cursor: progress; opacity: 0.8; }
}
```

```js
// js/site.js (defer). Progressive: without JS the form still posts normally.
document.querySelectorAll('[data-form]').forEach((form) => {
  const t0 = form.querySelector('[data-t0]'); if (t0) t0.value = Date.now();
  const summary = form.querySelector('[data-summary]');
  const status = form.querySelector('[data-status]');
  const btn = form.querySelector('[data-submit]'); const label = btn.querySelector('[data-label]');
  const idleLabel = label.textContent;
  const msgs = {
    name: 'Enter your name.',
    phone: 'Enter a phone number, for example 014 12 34 56.',
    email: 'Enter an email address like name@example.be.',
    message: 'Tell us briefly what you need.'
  };
  const check = (f) => {
    const v = f.value.trim();
    if (f.required && !v) return msgs[f.name];
    if (v && f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) return msgs.email;
    if (v && f.type === 'tel' && v.replace(/[^\d]/g, '').length < 8) return msgs.phone;
    return '';
  };
  const show = (f, msg) => {
    const err = document.getElementById(f.id + '-err');
    const ids = (f.getAttribute('aria-describedby') || '').split(' ').filter((i) => i && i !== err.id);
    if (msg) { err.textContent = msg; err.hidden = false; f.setAttribute('aria-invalid', 'true'); ids.push(err.id); }
    else { err.hidden = true; f.removeAttribute('aria-invalid'); }
    ids.length ? f.setAttribute('aria-describedby', ids.join(' ')) : f.removeAttribute('aria-describedby');
  };
  const fields = [...form.querySelectorAll('input:not([type=hidden]):not([tabindex="-1"]), textarea')];
  fields.forEach((f) => ['input', 'blur'].forEach((ev) => f.addEventListener(ev, () => {
    if (f.getAttribute('aria-invalid') === 'true') show(f, check(f));   // re-validate only after a first error
  })));

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (btn.getAttribute('aria-disabled') === 'true') return;
    const bad = fields.map((f) => [f, check(f)]).filter(([, m]) => m);
    fields.forEach((f) => show(f, check(f)));
    if (bad.length) {
      summary.querySelector('[data-count]').textContent = bad.length === 1 ? '1 field' : bad.length + ' fields';
      summary.querySelector('[data-summary-list]').innerHTML =
        bad.map(([f, m]) => `<li><a href="#${f.id}">${m}</a></li>`).join('');
      summary.hidden = false; summary.focus(); return;
    }
    summary.hidden = true;
    btn.setAttribute('aria-disabled', 'true'); label.textContent = 'Sending…';
    try {
      const res = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
      if (!res.ok) throw new Error(res.status);
      const name = form.elements.name.value.trim().split(' ')[0];
      form.outerHTML = `<div class="form-done" role="status" tabindex="-1"><h3>Thank you, ${name.replace(/[<>&"]/g, '')}.</h3>
        <p>We will call you back within one working day.</p></div>`;
      document.querySelector('.form-done').focus();
    } catch {
      status.textContent = 'Your message was not sent. Your text is still here; try again, or call 014 12 34 56.';
      btn.removeAttribute('aria-disabled'); label.textContent = idleLabel;   // values stay in the fields
    }
  });
});
```
Notes:
- Replace the success promise ("within one working day") with what the client actually does; if unknown, mark it `data-assumed`.
- Server side (Vercel function or form service): reject when `website` is filled or `Date.now() − t0 < 3000`; respond 2xx only after the email/CRM accepted it.
- Demo state (no endpoint yet): replace the `fetch` with `status.textContent = 'Demo: this form is not connected yet. Call …'` and leave the form in place. Never show the thank-you message.
- The error icon is a self-hosted SVG from the site's one icon family.
