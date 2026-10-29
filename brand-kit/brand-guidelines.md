# Samira Korani: brand guidelines

Version 1.0, 29 October 2026. A proposed, original identity. No trademark search or clearance has been carried out.

The identity is a personal practitioner brand. It should feel **precise, approachable and technically credible**: one person who does the work, shows the evidence and is clear about limits. It is not an agency brand.

Contents: [Identity](#1-identity) · [Name and company usage](#2-name-and-company-usage) · [Logo](#3-logo) · [Colour](#4-colour) · [Typography](#5-typography) · [Spacing and layout](#6-spacing-layout-and-shape) · [Components](#7-components) · [Imagery](#8-imagery) · [Voice](#9-voice) · [Files](#10-files-and-maintenance)

To see everything together, open `brand-kit/preview.html` (instructions in [section 10](#10-files-and-maintenance)).

---

## 1. Identity

| Element | Value |
|---|---|
| Wordmark | **Samira Korani** |
| Descriptor | Knowledge Graphs · GraphRAG · LLM Evaluation |
| Symbol | The letter K drawn as a small graph: one hub node with three relationships |
| Typeface | IBM Plex Sans |
| Core colours | Warm ivory, white, deep ink, deep teal, slate, pale sage |

The descriptor may be dropped where space is tight (the mobile header, favicons, avatars, small slide footers). The name may not.

---

## 2. Name and company usage

Two names, two jobs:

- **Samira Korani** is the public identity: the practitioner, speaker, author and open-source contributor.
- **MILEAWAY AI SYSTEMS LIMITED** is the company that provides, contracts and invoices the consulting services. It is a legal name, not a brand.

### Use "Samira Korani" for

- Website header, wordmark, page titles and social sharing image
- Talks, speaker bios, slides and workshop materials
- Articles and bylines
- GitHub and LinkedIn
- Email signature (the name line)

### Name MILEAWAY AI SYSTEMS LIMITED in

- The website footer: "Consulting services are provided by MILEAWAY AI SYSTEMS LIMITED", followed by the company's registered particulars
- Service descriptions and terms, wherever services are offered or contracted: "Engagements are contracted with and invoiced by MILEAWAY AI SYSTEMS LIMITED."
- Proposals, quotations and statements of work (as the service provider)
- Invoices (as the issuer)
- Contracts (as the contracting party)
- The legal line of the email signature when emailing in a commercial capacity

### Rules

1. Write the company name exactly as registered: **MILEAWAY AI SYSTEMS LIMITED**. Do not shorten it to "Mileaway", "Mileaway AI" or an abbreviation.
2. Never use the company name as a brand, wordmark or logo. There is no company logo; do not create one. Set it in normal running text.
3. Keep the company name out of the website header, page titles, the social image and slide title areas.
4. Where the company name appears in a commercial document, include its registered particulars: place of registration, registered number, registered office and, if registered, VAT number. Irish company rules generally require these particulars on a company's website and business documents. Confirm the exact list with your accountant.
5. The particulars below are placeholders for templates only. **Never publish placeholder text.** On the website, particulars are read from `_data/company.yml`, and empty values are left out.

### Sample email signature

```text
Samira Korani
Knowledge Graphs · GraphRAG · LLM Evaluation
samira.korani@gmail.com · skorani.github.io
linkedin.com/in/samirakorani · github.com/skorani

Consulting services are provided by MILEAWAY AI SYSTEMS LIMITED.
Registered in [PLACE OF REGISTRATION – TO CONFIRM], company number [CRO NUMBER – TO CONFIRM].
Registered office: [REGISTERED OFFICE ADDRESS – TO CONFIRM].
VAT number: [VAT NUMBER, ONLY IF REGISTERED – TO CONFIRM]
```

Keep the first four lines for talks, community and recruiter emails. Add the legal block when sending proposals, quotations, invoices or anything contractual.

### Sample proposal or quotation header

```text
[Symbol]  Samira Korani
          Knowledge Graphs · GraphRAG · LLM Evaluation

QUOTATION [Q-YYYY-NNN]                          Date: [DD Month YYYY]
                                                Valid until: [DD Month YYYY]

Prepared for:      [Client company], attention [Client contact]
Consultant:        Samira Korani · samira.korani@gmail.com
Service provider:  MILEAWAY AI SYSTEMS LIMITED
Engagement:        LLM Evaluation Health Check
Fee:               EUR 2,950, fixed for the scope below
VAT:               [Rate, or "not applicable" – TO CONFIRM]
Third-party costs: [e.g. model API usage, passed through at cost / paid directly by client – TO CONFIRM]
```

### Sample proposal or quotation footer

```text
MILEAWAY AI SYSTEMS LIMITED · Registered in [PLACE – TO CONFIRM] · Company number [CRO NUMBER – TO CONFIRM]
Registered office: [ADDRESS – TO CONFIRM] · VAT number: [ONLY IF REGISTERED – TO CONFIRM]
Consultant: Samira Korani · samira.korani@gmail.com                                   Page [X] of [Y]
```

On invoices, the company is the issuer ("Invoice from MILEAWAY AI SYSTEMS LIMITED"), and Samira Korani appears as the contact. Confirm the required invoice particulars, including any VAT details, with your accountant.

---

## 3. Logo

### The symbol

The letter K drawn as a graph: a vertical relationship, a hub node and two branches. It reads as an initial and as a knowledge-graph motif without needing explanation.

Construction, on a 32 × 32 grid:

- Stem from (9.75, 6) to (9.75, 26); arms from the hub (9.75, 16) to (22.25, 6) and (22.25, 26)
- Edge stroke 2.6 units with round caps; end nodes radius 3; hub radius 3.6
- Favicon tile: teal rounded square (radius 7), ivory nodes, pale sage edges
- Below 24 px, use `favicon.svg`, the tuned variant without the hub dot and with heavier strokes. It stays legible at 16 px.

### Lockups

| Lockup | When to use |
|---|---|
| Name only (`wordmark-name-*`) | Tight spaces, slide footers, avatars with text |
| Name with descriptor (`wordmark-descriptor-*`) | Website header on desktop, title slides, documents |
| Symbol, name and descriptor (`lockup-*`) | Proposal headers, email signature image, event listings |
| Symbol alone (`symbol-*`, `symbol-tile.svg`) | Favicon, app icon, social avatar, small marks |

### Colour variants

| Variant | Use on |
|---|---|
| `light` | Ivory or white backgrounds. Name in deep ink, descriptor in slate, symbol in teal. |
| `dark-bg` | Deep ink or deep teal backgrounds. Name in ivory, descriptor and edges in pale sage. |
| `mono-ink` | Single-colour printing on light paper (switch to pure black if the printer requires it) |
| `mono-white` | Single-colour reversed out of photos or dark materials |

### Clear space and minimum size

- Keep clear space on every side at least equal to the height of the capital **S** in the wordmark. For the symbol alone, use a quarter of its height.
- Minimum widths on screen: symbol 16 px; name-only wordmark 96 px; wordmark with descriptor 200 px (below that, drop the descriptor).

### Do not

- Recolour outside the palette, add gradients, shadows, glows or outlines
- Stretch, condense, rotate or re-space the letters
- Set the name in a different typeface
- Place the logo over busy photographs
- Add the company name, "Mileaway AI" or any other brand to the lockup
- Animate the logo

---

## 4. Colour

### Palette and roles

| Colour | Hex | Role |
|---|---|---|
| Warm ivory | `#F7F5EF` | Main page background |
| White | `#FFFFFF` | Reading surfaces: cards, panels, alternate sections |
| Deep ink | `#14252B` | Primary text; inverse (dark) section background |
| Deep teal | `#075E54` | Primary buttons, links, focus rings, accent rules, the symbol |
| Slate | `#52646A` | Secondary text: labels, captions, meta |
| Pale sage | `#D8DFDA` | Decorative borders and dividers; secondary text on deep ink only |
| Teal strong (derived) | `#04463F` | Hover and pressed states for teal controls |
| Teal tint (derived) | `#E7EFEC` | Highlighted panels (fees and scope), secondary button hover |

### Measured contrast (WCAG 2.2)

| Pair | Ratio | Use |
|---|---|---|
| Deep ink on ivory | 14.49:1 | Body text: AA and AAA |
| Deep ink on white | 15.80:1 | Body text: AA and AAA |
| Slate on ivory | 5.68:1 | Secondary text: AA |
| Slate on white | 6.20:1 | Secondary text: AA |
| Slate on teal tint | 5.30:1 | Notes in fee panels: AA |
| Teal on ivory | 7.03:1 | Links and outline buttons: AA and AAA |
| Teal on white | 7.67:1 | Links: AA and AAA |
| Teal on teal tint | 6.56:1 | Links in highlighted panels: AA |
| White on teal | 7.67:1 | Primary button text: AA and AAA |
| White on teal strong | 10.75:1 | Primary button hover: AA and AAA |
| Ivory on deep ink | 14.49:1 | Inverse text and inverse buttons |
| Pale sage on deep ink | 11.65:1 | Secondary text on inverse sections |
| Teal focus ring vs ivory | 7.03:1 | Focus indicator (needs 3:1) |
| Ivory focus ring vs deep ink | 14.49:1 | Focus indicator on dark sections |
| **Pale sage on ivory** | **1.24:1** | **Decoration only.** Never for text, icons or control borders. |
| **Teal on deep ink** | **2.06:1** | **Never use.** On dark sections use ivory and pale sage. |

The website's automated checks (axe-core, plus a contrast measurement of every control in default, hover and focus states) passed on all pages. Run `tools/verify_site.py` to repeat them.

### Rules

- Pale colours are decorative. Text, icons and the boundary of any control people must find use deep ink, slate or teal on light backgrounds.
- Teal is the only accent. Do not introduce extra accent colours, gradients or neon.
- Use the inverse (deep ink) treatment sparingly: once per page, for the contact section.

---

## 5. Typography

**IBM Plex Sans** (SIL Open Font License 1.1; licence in `brand-kit/fonts/OFL.txt`). The website self-hosts a single variable Latin file (39 KB) covering weights 100 to 700.

Fallback stack: `system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`.

| Weight | Use |
|---|---|
| 400 Regular | Body text, descriptor |
| 500 Medium | Navigation |
| 600 SemiBold | Headings, the wordmark, buttons, labels, emphasis |

### Type scale

| Token | Size | Use |
|---|---|---|
| `--text-xs` | 13 px | Eyebrow labels (uppercase, +0.08em tracking), tags, legal lines |
| `--text-sm` | 15 px | Meta, captions, notes, navigation |
| `--text-base` | 17 px | Body text (line height 1.6) |
| `--text-lg` | 20 px | Lead paragraphs, card titles |
| `--text-xl` | 24 px | Subsection headings |
| `--text-2xl` | 28 to 36 px, fluid | Section headings (h2) |
| `--text-3xl` | 34 to 54 px, fluid | Page headline (h1) |

Headings use −0.015em tracking and a tight line height (1.12). Keep body lines to about 70 characters (`--width-prose`, 42 rem).

### Conventions

- Irish/British English spelling: organise, prioritise, programme.
- Prices: "EUR 2,950". Ranges with an en dash: "EUR 7,500–12,000", "2–3 weeks".
- Dates: "6 November 2025" in text, "Nov 2025" in compact lists.
- The descriptor uses middle dots with spaces: "Knowledge Graphs · GraphRAG · LLM Evaluation".

---

## 6. Spacing, layout and shape

| Token | Value | Token | Value |
|---|---|---|---|
| `--space-1` | 4 px | `--space-6` | 32 px |
| `--space-2` | 8 px | `--space-7` | 48 px |
| `--space-3` | 12 px | `--space-8` | 64 px |
| `--space-4` | 16 px | `--space-9` | 96 px |
| `--space-5` | 24 px | `--section-space` | 48 to 96 px, fluid |

- Content width: 72 rem (1152 px) container; prose 42 rem
- Side gutter: 16 px on phones, up to 40 px on wide screens
- Corner radii: 4 px (tags), 8 px (buttons, inner panels), 12 px (cards). Nothing rounder.
- Borders: 1 px pale sage dividers (decorative). A 3 px teal top rule marks featured panels.
- Generous whitespace beats more boxes. One idea per section.

---

## 7. Components

All values come from `brand-kit/tokens.css`; the website implementation is `assets/css/site.css`.

| Component | Specification |
|---|---|
| Primary button | Teal fill, white 600 text, 2 px teal border, 8 px radius, minimum 44 px tall. Hover: teal strong. |
| Secondary button | Transparent, teal text and 2 px teal border. Hover: teal tint fill. |
| Inverse buttons | On deep ink: ivory fill with ink text, or a pale sage outline with ivory text |
| Links | Teal and always underlined (1 px, 2 px on hover). Ivory on dark sections. |
| Focus | 3 px outline, 2 px offset: teal on light surfaces, ivory on dark |
| Cards | White on ivory (or ivory on white sections), 1 px sage border, 12 px radius, 24 to 32 px padding |
| Fact list | Label column in slate 15 px, value in ink 600, sage dividers. Used for fee, time and scope. |
| Checklist | Small teal node bullets, echoing the symbol |
| FAQ | Native `<details>` with a teal chevron. Works without JavaScript. |
| Motion | Colour transitions of 140 ms only; none with reduced motion. No animated backgrounds. |

---

## 8. Imagery

Use:

- Real photographs of Samira Korani: natural light, plain or softly blurred background
- Screenshots of real work (code, graphs, evaluation results) where they help
- Simple diagrams in the palette: nodes and edges, thin lines, flat colour

Avoid:

- Stock robots, glowing brains, circuit boards, neon gradients and animated backgrounds
- Third-party logos that could imply endorsement, including former employers, clients, event sponsors and conference lanyards
- Generic "team" stock photography; this is a one-person practice

The current website portrait is a crop of an existing photo, cropped to remove a sponsor lanyard. Replace it with a professional headshot when one is available (4:5, at least 960 × 1200 px).

Always give images meaningful alternative text, such as "Samira Korani". Decorative graph illustrations should be hidden from assistive technology.

---

## 9. Voice

Write as one practitioner talking to an engineering lead.

- **First person singular.** "I", not "we", unless describing a past team.
- **Plain and specific.** Name the system, the measure and the deliverable.
- **Evidence over adjectives.** Link to the talk, the code or the article instead of describing yourself.
- **Honest about limits.** Say what an assessment does not cover.
- **Calm.** No exclamation marks, urgency tricks or hype.

| Instead of | Write |
|---|---|
| We are a leading AI consultancy delivering cutting-edge solutions. | I help engineering teams find out where their RAG and agent systems fail, and what to fix first. |
| Our team of experts will transform your AI. | I do the work myself, so you deal with one person from the first call to the handover. |
| Guaranteed accuracy improvements. | You get baseline results on agreed cases, a failure analysis and a prioritised list of fixes. |
| Trusted by top brands. | (Leave it out. Link to public evidence: talks, code, writing.) |
| Revolutionise your search with GraphRAG! | GraphRAG helps when answers depend on relationships between entities. When they don't, better chunking or metadata may do more for less. |
| Book your free strategy session now! | Discuss your project. (Use "Book a call" only when a real booking link exists.) |
| Comprehensive AI security audit. | The Health Check is not a security audit or certification. |

### Speaker bio

Short (about 40 words):

> Samira Korani is a machine learning engineer in Galway, Ireland, working on LLM evaluation, knowledge graphs and GraphRAG. Samira spoke at NODES 2025 on contextual knowledge graphs for LLMs and is a Neo4j Featured Community Member.

Longer (about 80 words):

> Samira Korani is a machine learning engineer based in Galway, Ireland, who has worked in natural language processing and machine learning since 2013. Samira's work focuses on production AI: evaluating RAG and agent systems, building knowledge graphs and GraphRAG pipelines, and designing agentic workflows in Python. Samira co-founded the travel-assistant startup Tripoh, spoke at NODES 2025 on building contextual knowledge graphs to adapt and evaluate LLMs, and was recognised as a Neo4j Featured Community Member in November 2025.

---

## 10. Files and maintenance

```text
brand-kit/
  brand-guidelines.md          this document
  preview.html                 identity and website components on one page
  tokens.css                   design tokens; the website loads this file
  fonts/                       IBM Plex Sans variable (Latin) and its licence
  logo/
    symbol-{light,dark-bg,mono-ink,mono-white}.svg
    symbol-tile.svg            teal tile (app icon, avatar)
    favicon.svg                16 px-tuned tile
    favicon.ico                16, 32 and 48 px
    favicon-{16,32,48}.png, apple-touch-icon.png, symbol-tile-512.png
    wordmark-name-{light,dark-bg,mono-ink,mono-white}.svg
    wordmark-descriptor-{light,dark-bg,mono-ink,mono-white}.svg
    lockup-{light,dark-bg,mono-ink,mono-white}.svg
    lockup-{light,dark-bg}@2x.png   for email signatures and documents
  social/
    og-image.png               1200 × 630 sharing image
    og-image.html              its editable source
  tools/generate_assets.py     regenerates logo, favicon and social files
```

**Viewing the preview.** From the repository root, run `python3 -m http.server 8001`, then open <http://localhost:8001/brand-kit/preview.html>. The preview is not published with the website.

**Editing the wordmark.** The SVG wordmarks use live text with an embedded Latin subset of IBM Plex Sans, so they render consistently in browsers. To edit them in Figma or Illustrator, install IBM Plex Sans first.

**Changing colours or text.** Edit `tokens.css` (website) and the constants at the top of `tools/generate_assets.py` (logo files), then regenerate the files as described in that script.
