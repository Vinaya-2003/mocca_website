# MOCCA — Men's Wear & Wedding — Website

A Flask + HTML/CSS/JS website for **MOCCA**, split into two sub-brands —
**MOCCA Men's Wear** and **MOCCA Wedding** — each with its own page, hero,
and visual identity, joined by a landing "gateway" page.

## Structure

```
mocca_website/
├── app.py                       # Flask app: routes, form handling, JSON API
├── requirements.txt
├── data/
│   ├── products.json            # Both brand sections + all 6 stores
│   └── messages.json            # Created automatically on enquiry-form submit
├── templates/
│   ├── base.html                # Shared header/footer/nav (no rating badge)
│   ├── landing.html             # "/" — split panel: choose Men's Wear or Wedding
│   ├── menswear.html            # MOCCA Men's Wear homepage
│   ├── menswear_collections.html# Full catalog browser (casual/formal/festive/kids)
│   ├── wedding.html             # MOCCA Wedding — dedicated black & gold lookbook
│   ├── stores.html              # Store locator, all 6 branches, real data
│   ├── contact.html             # Enquiry form
│   ├── _reviews.html            # Shared "ratings at the end of the page" section
│   └── 404.html
└── static/
    ├── css/style.css            # Design system + floating animations + wedding theme
    ├── js/main.js                # Mobile nav, swatch-nav scrolling, scroll reveal
    └── images/
        ├── logo.jpg              # Real MOCCA logo (auto-detected)
        ├── hero.jpg               # Men's Wear hero photo
        ├── hero-wedding.jpg       # Wedding hero photo
        ├── collections/           # Cover photos per men's-wear collection
        ├── products/              # Individual men's-wear product photos
        ├── wedding/                # The 8-look wedding lookbook
        └── stores/                 # Optional store-front photos
```

## Running it

```bash
cd mocca_website
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** — you'll land on the gateway page.

## Routes

| Route                                   | Purpose                                       |
|-------------------------------------------|-------------------------------------------------|
| `/`                                        | Landing gateway — pick Men's Wear or Wedding    |
| `/menswear`                                | MOCCA Men's Wear homepage                       |
| `/menswear/collections` `/menswear/collections/<slug>` | Catalog browser (`casual`, `formal`, `festive`, `kids`) |
| `/wedding`                                  | MOCCA Wedding lookbook (8 looks)                |
| `/stores`                                    | Store locator, all 6 branches                   |
| `/contact` (GET/POST)                        | Enquiry form → saves to `data/messages.json`    |
| `/api/menswear` `/api/wedding` `/api/stores` | JSON endpoints for each section                 |

## What changed in this pass

- **Two brands, two pages.** Men's Wear and Wedding no longer share one
  homepage — each has its own hero, palette and content, linked from a
  shared landing gateway.
- **Wedding has its own visual identity** — black background with gold
  accents (`--gold-thread`), matching the "MOCCA WEDDING" campaign logo
  lockup, distinct from the ivory/camel Men's Wear palette.
- **No prices.** Every product/look now shows just a photo and a name —
  no price, fabric, or color metadata. Add real pricing back into
  `data/products.json` yourself when you're ready to publish it.
- **Ratings moved out of the header.** There's no more star badge in the
  nav. Every page ends with a shared reviews section (`_reviews.html`)
  showing the review-weighted average across all 6 stores, linking to
  `/stores` for the full breakdown.
- **Floating animations.** Hero photos, small overlay badges, and
  gallery/lookbook images have a slow, staggered CSS float
  (`.float`, `.float-soft`, `.float-text` in `style.css`). All of it
  respects `prefers-reduced-motion`.
- **Real store data for all 6 branches** (address, phone, hours, rating,
  review count) — sourced from the Google listings you shared, replacing
  the earlier placeholders for Edappal, Vengara, Perinthalmanna, Nilambur
  and Manjeri.

## Adding more images later

Same auto-detection as before — drop a file in with the right name and it
appears, no code changes needed:

| What it is           | Save it as                                      |
|------------------------|--------------------------------------------------|
| Logo                    | `static/images/logo.jpg` (already set)            |
| Men's Wear hero          | `static/images/hero.jpg` (already set)             |
| Wedding hero              | `static/images/hero-wedding.jpg` (already set)      |
| Men's Wear product         | `static/images/products/<product-id>.jpg`            |
| Men's Wear collection cover | `static/images/collections/<slug>.jpg`                |
| Wedding look               | `static/images/wedding/<look-id>.jpg`                  |
| Store front photo            | `static/images/stores/<store-id>.jpg`                   |

Product/look/store IDs live in `data/products.json` — add a new entry
there (with an `image` path) and drop the matching file in.

## Still to do (you mentioned you'll send these)

- Complete store information / brand copy for the MOCCA Men's Wear "About"
  content and the MOCCA Wedding page.
- Real pricing, if you want it back in — it was intentionally stripped in
  this pass.
- Phone numbers for Cherpulassery and Vengara weren't in the listing text
  you shared — `data/products.json` has them blank for now.
