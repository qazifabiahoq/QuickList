# QuickList by thredUP
### Bringing Listings Out of the Dark
#### Generative AI Solution for Automated Product Listing Creation

**MMAI 5090 F: Business Applications of AI II**
Noelia Cornejo · Dedan Deus · Emily Bendeck Garay · Qazi Fabia Hoq · Esha Malhi
Dr. Divinus Oppong-Tawiah | February 11, 2026

**[Live Demo](https://quicklist.streamlit.app/)**

---

## The Business Problem

thredUP - North America's largest online resale marketplace with $322M in annual revenue - operates on a managed consignment model: sellers mail in clothing, and thredUP handles listing, photography, pricing, and fulfillment. But items are sitting unsold.

The root cause is listing quality. Product titles read "Blue Top Medium" instead of "Madewell Cotton Striped Button-Front Shirt Navy Blue Medium." Descriptions are generic. Search tags are missing or inconsistent. Without keyword-rich metadata, even thredUP's search algorithm cannot surface relevant items to buyers. Sellers receive no payout and conclude the platform can't move their inventory - so they leave.

In November 2025, CEO James Reinhart acknowledged the company was losing sellers to competitors like Poshmark, Mercari, and Depop. The fix isn't operational - it's the listing quality that's broken. Creating a professional listing manually takes 5-10 minutes per item. At consignment scale, that effort produces rushed, low-quality output.

**QuickList solves this at the source.** By automating high-quality listing creation during the consignment intake process, it reduces seller churn, increases sell-through rates, and reduces time-to-sale across thredUP's entire inventory.

---

## Solution

QuickList is an internal tool used by thredUP during consignment intake. When a product photo is captured, QuickList generates a complete, SEO-optimized listing in approximately **30 seconds** - a **90% reduction** in listing time per item.

**Input:** Product photo captured during intake + optional details
**Output:** SEO title · Professional description · Feature bullets · Meta description · Primary & long-tail keywords

---

## Business Value

thredUP's core problem is invisible inventory. Items are physically in the warehouse, professionally photographed, and ready to sell - but buyers can't find them because the metadata is weak. QuickList fixes the signal, not the supply chain.

**Seller retention.** Sellers mail in inventory expecting a return. When items don't sell due to poor discoverability - not poor quality - they blame thredUP and leave. QuickList makes listings searchable and compelling from day one. Retained sellers re-list, refer others, and send higher-value inventory over time.

**Sell-through rate.** Better titles and keyword-rich descriptions improve search ranking within thredUP's platform and on external search engines. More impressions drives more buyers, which clears more inventory. Higher sell-through also reduces the cost of holding and eventually discounting unsold items.

**Time-to-sale.** Faster sales mean faster payouts to sellers, which builds trust and reinforces the platform habit. It also improves thredUP's inventory turnover, directly reducing warehouse costs tied to slow-moving stock.

**Operational efficiency.** At consignment scale, 90%+ automation means the same intake team processes significantly more inventory without added headcount. The marginal cost of listing an additional item drops dramatically, improving unit economics at scale.

**Revenue.** At thredUP's 15% transaction fee, every percentage point improvement in sell-through across millions of items compounds into material incremental revenue. Better listings also attract higher-quality, higher-value seller inventory - the segment thredUP has been losing to competitors.

**Competitive positioning.** Poshmark, Mercari, and Depop rely entirely on sellers to write their own listings - inconsistent, keyword-poor, and unverified. QuickList gives thredUP a structural listing quality advantage that is difficult to replicate without 172M items of professional training data.

| Metric | Impact |
|---|---|
| Listing time | 5-10 min → ~30 sec (90% reduction) |
| Seller churn | Reduced as items become discoverable and actually sell |
| Sell-through rate | Improved via SEO-optimized, keyword-rich listings |
| Time-to-sale | Reduced - faster payouts, faster inventory turnover |
| Operational cost | 90%+ automation, same team processes more inventory |
| Competitive position | Listing quality advantage competitors cannot easily replicate |

Initial investment: $850K-$2.1M. Estimated payback period: **18-26 months.**

---

## Why Generative AI?

Template and rule-based systems cannot solve this problem. Every listing needs **unique, persuasive, SEO-optimized copy** - duplicate content penalizes search rankings and kills buyer engagement. Only gen AI generates natural, varied descriptions at scale while staying factually grounded in detected product attributes.

Traditional AI can classify an image as "black silk dress." Gen AI writes: *"Experience timeless sophistication with this elegant black silk dress, crafted from premium fabric with a fluid drape perfect for evening wear."* That difference drives clicks, favorites, and sales.

---

## Technical Architecture

QuickList combines four AI components working in sequence:

**1. Computer Vision - Attribute Detection**
A fine-tuned CLIP model extracts structured product attributes from intake photos: category, type, color, material, style, and condition. Fine-tuned on thredUP's **172 million professionally-labeled consignment items** - verified condition grades, authenticated brands, expert material assessments - this model achieves 10-20% higher accuracy than generic vision models. Competitors relying on user-generated listings cannot replicate this data quality.

**2. Retrieval-Augmented Generation (RAG) - Grounding in What Sells**
Before generating copy, the system queries thredUP's historical listing database to retrieve similar items that sold successfully. These high-converting listings become in-context examples that guide the gen AI toward language and structure proven to drive sales. RAG ensures generated descriptions aren't just grammatically correct - they're optimized for thredUP's specific buyer behavior and conversion patterns.

**3. Generative AI - Content Creation**
The core of QuickList. Large language models transform structured vision outputs and RAG-retrieved examples into compelling product copy: SEO-optimized titles, 150-200 word descriptions in thredUP's brand voice, feature bullets, and meta descriptions. Production uses **Llama 3.3 70B via Groq** (sub-2s latency, ~93% cost savings vs GPT-4 at scale) with GPT-4 Turbo as a quality fallback for luxury and high-value items.

**4. Rule-Based Validation - Hallucination Prevention**
A validation layer scans all generated content before publishing. It checks for color hallucinations (the most common LLM failure mode), material inconsistencies, category mismatches, and policy violations. If validation fails, the system retries with the next AI tier or falls back to a template. Gen AI speed plus deterministic guardrails - quality at scale.

```
Intake Photo → Computer Vision → RAG Retrieval → Generative AI → Validation → Published Listing
                                                                       |
                                                    [Human Review: luxury / low-confidence items]
```

Total target latency: **< 5 seconds** end-to-end.

---

## Competitive Moat

thredUP's sustainable advantage is its data. **172 million items** with professional assessments - ground truth that competitors using noisy, user-generated listings cannot match. Replicating this would require $50M+ and 3-5 years minimum.

This data powers every component: vision model accuracy, RAG retrieval quality, gen AI fine-tuning on thredUP's brand voice, and pricing recommendations via XGBoost trained on 172M actual transactions. The system improves continuously through active learning - seller edits, buyer engagement, and sales outcomes feed back into weekly model retraining.

---

## Demo

This repository contains a proof-of-concept Streamlit app demonstrating QuickList's end-to-end flow using free-tier APIs. It validates the core technical approach - vision analysis, gen AI content generation, and validation - without requiring production infrastructure. RAG and pricing recommendations are not included in the demo as they require access to thredUP's proprietary transaction and listing database.

---

## Team

[Noelia Cornejo](https://www.linkedin.com/in/noeliacornejo/) · [Dedan Deus](https://www.linkedin.com/in/dedan-deus-304908177/) · [Emily Bendeck Garay](https://www.linkedin.com/in/emily-bendeck/) · [Qazi Fabia Hoq](https://www.linkedin.com/in/qazifabiahoq/) · [Esha Malhi](https://www.linkedin.com/in/esha-malhi/)

*Inspired by firsthand experience with product tagging inefficiencies in e-commerce.*

**Course:** MMAI 5090 F - Business Applications of AI II | **Instructor:** Dr. Divinus Oppong-Tawiah
