# QuickList by ThreadUp
### Generative AI Solution for Automated Product Listing Creation in Peer-to-Peer Resale

**MMAI 5090 F: Business Applications of AI II**  
*Noelia Cornejo, Dedan Deus, Emily Bendeck Garay, Qazi Fabia Hoq, Esha Malhi*  
Dr. Divinus Oppong-Tawiah | February 11, 2026

---

## Project Inspiration

This project emerged from real-world frustration experienced by team member Qazi Fabia Hoq during previous work involving product tagging and categorization. Spending 5-10 minutes per item to create proper product listings, ensure accurate categorization, and optimize for searchability revealed a critical inefficiency plaguing e-commerce platforms.

ThreadUp presented the perfect case study: North America's largest resale marketplace losing sellers to competitors due to this exact listing friction problem.

---

## Business Problem: ThreadUp's Seller Churn Crisis

### Company Background

ThreadUp generates $322 million in annual revenue operating the largest online resale marketplace for secondhand apparel in North America. The company built its business on managed consignment where sellers mail clothing and ThreadUp handles listing, photography, pricing, and fulfillment.

### The Critical Problem

In November 2025, CEO James Reinhart announced a strategic pivot toward peer-to-peer selling, acknowledging the company was losing sellers to competitors. Research revealed sellers were strategically splitting inventory across platforms based on item value.

**Low-value items** went to ThreadUp consignment because individual listing effort wasn't worthwhile. **High-value, premium pieces** went to peer-to-peer platforms like Poshmark, Mercari, and Depop where sellers controlled pricing, listed instantly, and captured higher payouts.

The fundamental issue: creating quality peer-to-peer listings requires 5-10 minutes of manual effort per item. For sellers with inventories of 50-100 items, this effort barrier becomes prohibitive.

### The Negative Spiral

ThreadUp was hemorrhaging its most profitable inventory. Without premium inventory, ThreadUp couldn't attract buyers seeking high-quality pieces. Lower inventory quality reduced buyer traffic, making the platform less attractive to sellers, perpetuating the cycle.

### Why Peer-to-Peer Will Fail Without AI

The fundamental tension persists: consignment offers convenience but low payouts, while peer-to-peer offers control but requires manual effort. No platform has solved this.

ThreadUp's pivot to peer-to-peer will fail unless they eliminate listing friction. Without solving this core problem, peer-to-peer simply replicates the same churn on a different business model.

---

## Solution: QuickList - A Generative AI Application

QuickList eliminates listing friction by automating professional-quality listing creation from a single photo in approximately 30 seconds.

### What QuickList Delivers

**Input**: One product photo and optional product details

**Output**: Complete professional listing including SEO-optimized product title, professional description (150-200 words), key feature bullet points, meta description for search engines, primary keywords, long-tail keywords, and platform-specific formatting for Shopify, Amazon, Etsy, or WooCommerce.

**Impact**: 5-10 minutes reduced to 30 seconds (90% time reduction)

---

## Why QuickList is a Generative AI Solution

### The Core Technology: Large Language Models

QuickList is fundamentally a **generative AI application** because its primary function is **content generation**. The system creates entirely new text content (product listings) that did not previously exist.

**The problem requires content creation, not just classification**:

Sellers need written product descriptions that are unique, persuasive, and SEO-optimized for each individual item. Traditional AI (computer vision classification, predictive models) can detect that an image shows a "black silk dress" but cannot write "Experience timeless sophistication with this elegant black silk dress crafted from premium fabric." That requires generative AI.

**Generative AI models used in QuickList**:

The core content generation engine uses **large language models (LLMs)** that generate human-quality text. Production deployment uses **Llama 3.3 70B** (Meta's open-source LLM) accessed through Groq's inference API, with **OpenAI GPT-4 Turbo** as fallback for quality-critical listings. These models create unique product titles, descriptions, bullet points, and meta descriptions for each item.

**Why this cannot be solved without generative AI**:

Template-based approaches fail because every product needs unique descriptions to avoid duplicate content penalties in search engines and to maintain buyer engagement. Rule-based text generation produces robotic, repetitive content that hurts conversions. Only generative AI can produce natural, varied, persuasive descriptions at scale while maintaining quality and SEO optimization.

**Supporting AI technologies**:

While generative AI is the core, QuickList combines it with computer vision (CLIP for attribute detection), traditional machine learning (XGBoost for pricing), and rule-based validation. The vision and pricing components provide structured input that feeds into the generative AI models, ensuring generated content is factually accurate.

---

## Technical Architecture: Production System

QuickList combines four core AI components with human-in-the-loop quality assurance.

### System Components

| Component | Technology | Purpose | Why This Choice |
|-----------|-----------|---------|-----------------|
| **Generative AI (CORE)** | Llama 3.3 70B via Groq + GPT-4 fallback | Generate unique product descriptions, titles, features, keywords | LLMs create natural language content; open-source reduces costs; Groq achieves <2s latency |
| **Computer Vision** | Fine-tuned CLIP model on ThreadUp's 172M items | Extract product attributes from images | Zero-shot handles fashion diversity; fine-tuning on professional labels improves accuracy dramatically |
| **Rule-Based Validation** | Custom validation rules + hallucination detection | Prevent AI errors and ensure factual accuracy | Catches color mismatches, missing fields, compliance violations before content reaches sellers |
| **Pricing ML** | XGBoost trained on 172M transactions | Recommend optimal price ranges with explanations | Interpretable feature importance builds seller trust; efficient on transaction history |
| **Human Review Queue** | Manual review workflow | Quality assurance for low-confidence predictions | Hybrid approach maintains quality while achieving scale |

### Component 1: Generative AI for Content Creation (Core Technology)

**Production Technology**: Llama 3.3 70B accessed through Groq Enterprise API as primary generative model, with OpenAI GPT-4 Turbo as fallback for quality-critical listings (luxury brands, high-value items).

**This is the core generative AI component that defines QuickList**. Large language models generate entirely new content that did not exist before, creating unique product descriptions rather than classifying or retrieving existing text. This is what makes QuickList a generative AI solution.

**Why Llama 3.3 70B for production**: 

Open-source licensing eliminates per-token costs at scale, providing significant cost advantages. Groq's custom Language Processing Unit (LPU) hardware achieves generation latency under 2 seconds, critical for mobile user experience. Quality is comparable to GPT-4 on structured content generation tasks while being significantly more cost-effective for high-volume applications. At 1.6 million listings annually, GPT-4 would cost approximately $48,000 versus $3,200 for Groq-hosted Llama. Additionally, self-hosted open-source models keep ThreadUp's proprietary product data private rather than sending it to external API providers.

**What the generative AI creates**: 

SEO-optimized product titles incorporating detected attributes and search keywords. Professional descriptions (150-200 words) balancing emotional appeal with practical benefits, written in ThreadUp's brand voice emphasizing sustainability. Bullet points highlighting key features and benefits in scannable format. Meta descriptions optimized for search engines under 160 characters. Primary and long-tail keywords for platform SEO.

**Prompt engineering to control generation quality**: 

Carefully engineered prompts establish context as expert fashion copywriter specializing in sustainable resale. Prompts specify exact output requirements including structure, length, tone, and brand voice. Critical constraints prevent hallucinations by explicitly listing forbidden attributes. For example, if computer vision detects black color, the prompt states "Use ONLY black as the color. DO NOT mention: red, blue, green, yellow, orange, purple, pink, brown, white, gray, beige, navy, burgundy, crimson." This prevents the LLM from inventing colors not present in the actual product.

**Structured output format**: 

Generative models are instructed to output valid JSON with specific fields (title, description, bullet_points, meta_description). This structured format enables automated parsing and validation before content reaches sellers.

**Production deployment infrastructure**: 

Primary generation through Groq Enterprise API with guaranteed SLA and dedicated throughput. Fallback to OpenAI GPT-4 Turbo API for approximately 5% of listings requiring highest quality or when Groq experiences issues. Response format enforced as JSON for reliable parsing. Generation parameters tuned for optimal output: temperature 0.7 balances creativity with consistency, top-p 0.9 uses nucleus sampling, max tokens 700 allows complete listings while controlling costs.

**Fine-tuning on ThreadUp's best-performing listings**: 

After initial deployment, production system would fine-tune Llama 3.3 70B on ThreadUp's highest-converting product descriptions from historical data. This creates a custom generative model that inherently writes in ThreadUp's brand voice and generates descriptions proven to drive sales. Fine-tuning dataset would include 50,000-100,000 professionally-written descriptions with associated conversion metrics, creating a model specialized for sustainable fashion resale.

### Component 2: Computer Vision for Attribute Detection

**Production Technology**: CLIP (Contrastive Language-Image Pretraining) model fine-tuned on ThreadUp's 172 million items with professional assessments, deployed on ThreadUp GPU infrastructure with Google Cloud Vision API as fallback.

**Why CLIP with fine-tuning**: 

Fashion resale involves enormous product diversity including vintage items, international brands, and niche styles impossible to comprehensively pre-label. Traditional CNNs like ResNet or EfficientNet require supervised training on every possible category. CLIP performs zero-shot classification by understanding relationships between images and text descriptions, generalizing to new items immediately without retraining. However, vanilla CLIP lacks domain expertise in fashion attribute detection and condition assessment.

**ThreadUp's critical advantage through fine-tuning**:

ThreadUp's 172 million item consignment history includes professional assessments by trained specialists. Each item has verified labels: exact category using standardized taxonomy (not user guesses), material composition verified by physical inspection (distinguishing silk from polyester from blends), condition grades using consistent criteria across all items (like new, gently used, visible wear), brand identification and authentication (verified designer vs fast fashion), and color assessment by trained eyes (navy vs black vs charcoal).

This professional ground truth data enables supervised fine-tuning of CLIP that dramatically improves accuracy on challenging attributes. Fine-tuned CLIP learns to distinguish silk from satin from polyester based on visual texture cues. It accurately assesses condition (tiny pulls vs significant wear). It recognizes designer construction details vs mass-market finishing. It handles subtle color differences critical for fashion.

**Competitors like Poshmark, Mercari, and Depop cannot replicate this** because they rely on user-generated listings with inconsistent photo quality, unverified attribute labels often containing errors, no professional verification process, and years of noisy, unreliable training data.

**Fine-tuning process and cost**:

Starting with OpenAI's pre-trained CLIP ViT-L/14 model, ThreadUp would fine-tune on their 172 million professionally-labeled images. Training infrastructure requires GPU cluster (AWS P3 instances or equivalent) for approximately 2-4 weeks. Total cost including compute, data preparation, and engineering ranges from $75,000 to $150,000 one-time investment. Result is a custom CLIP model that achieves 10-20% higher accuracy than vanilla CLIP on fashion-specific attributes, creating sustainable competitive advantage worth millions.

**What vision detects**: 

Product category (dress, jacket, pants, shoes, accessories). Specific type (evening gown, blazer, skinny jeans, ankle boots). Material composition (silk, cotton, leather, polyester, wool, blends). Color families (black, navy, burgundy, neutral tones, patterns). Style descriptors (elegant, casual, vintage, modern, bohemian). Condition indicators (new with tags, like new, gently used, visible wear, damaged). Each prediction includes confidence score (0-1 scale) determining whether human review is needed.

**Production deployment**: 

Fine-tuned CLIP model deployed on GPU instances (AWS EC2 P3 or GCP with NVIDIA T4/V100 GPUs) for real-time inference. Target latency under 2 seconds per image. Google Cloud Vision API integrated as fallback when CLIP confidence scores fall below thresholds or for redundant validation on high-value items. Confidence thresholds (typically 0.75 for critical attributes) determine when predictions route to human review queue rather than proceeding to generative AI.

### Component 3: Rule-Based Validation Layer

**Critical for production quality**. This prevents common generative AI errors and ensures content accuracy before listings reach sellers.

**Validation checks preventing hallucinations**:

Color hallucination prevention is the most critical check. After the generative AI creates content, the validation system scans all generated text for forbidden color terms. If computer vision detected "black" but generated text mentions "elegant red silk," the output is immediately rejected and the system attempts generation with the next AI tier or uses template fallback. This prevents the common LLM problem of inventing plausible-sounding but factually incorrect attributes.

Material consistency validation ensures generated descriptions only mention materials detected by computer vision. If vision detected "silk" and "premium fabric" but description mentions "cotton blend," validation fails.

Category and type consistency checks that title and description align with detected product category. A dress cannot be described as "versatile pants" even if the generative model hallucinates this.

**Content quality validation**:

Description length verification ensures 150-200 word target (not too short appearing low-effort, not too long reducing readability). Keyword density analysis prevents keyword stuffing that hurts SEO. Readability scoring using Flesch reading ease targets scores above 60 for broad accessibility. Sentiment analysis ensures positive, professional tone without overly salesy language.

**Compliance validation using ThreadUp's historical policy data**:

Scans for prohibited terms compiled from years of policy enforcement (unauthorized brand name mentions, profanity, medical claims). Checks policy violations based on ThreadUp's content guidelines (health claims, guarantees, misleading statements). Detects potential trademark infringement before listings go live. Flags sensitive categories requiring extra review (children's items, swimwear, undergarments).

**Pricing validation using transaction history**:

Compares suggested prices against historical ranges for detected category and brand using ThreadUp's 172 million transaction database. Luxury brands (Gucci, Prada, Chanel) with prices under $50 automatically flagged as likely errors. Budget brands with premium pricing flagged for verification. Outlier detection catches prices more than 2 standard deviations from category mean.

**High-value triggers routing to human review**:

Luxury brand detection (250+ designer brands) automatically routes to specialist reviewers. Damaged items or significant condition issues flagged by vision system. Content and attribute conflicts (description mentions features vision didn't detect). Confidence scores below 0.75 on any critical attribute (category, condition, brand). New product categories with limited training data.

### Component 4: Pricing Recommendation Engine

**Production Technology**: XGBoost gradient boosting model trained on ThreadUp's 172 million transaction history, retrained weekly on fresh data.

**Why XGBoost over deep learning for pricing**: 

Interpretability is critical for seller trust. Sellers need to understand why a price was suggested to feel confident accepting recommendations. XGBoost provides transparent feature importance showing which factors drive pricing: material quality contributes 23%, brand recognition 18%, condition grade 15%, seasonal demand 12%, geographic location 9%, item age 7%, and so on. Sellers see "Similar silk dresses sold for $55-75 in the past 30 days based on material, condition, and current demand."

Deep learning models function as black boxes providing no explanation. A neural network saying "list at $62" without rationale leads to sellers distrusting and overriding recommendations, defeating the tool's purpose. Additionally, XGBoost trains efficiently on structured tabular data (transaction records) while neural networks are overkill for this problem type.

**Training on ThreadUp's proprietary transaction data**:

The model trains on 172 million historical transactions including actual sale prices (what items sold for, not just asking prices which may never sell). Time-to-sale data (how many days from listing to purchase, indicating price accuracy). Seasonal patterns (winter coats sell higher November-February, swimwear peaks May-July). Geographic demand variations (designer brands command premium in urban markets, practical items in suburban). Seller tier effects (established sellers achieve higher prices than new sellers for identical items).

**How pricing recommendations work**:

For each new listing, the system queries ThreadUp's transaction database to find recent comparable sales (same category, similar brand tier, comparable condition, similar materials, same geographic region). XGBoost model processes listing attributes and comparable sales data to generate optimal price range with confidence interval, typically $X to $Y representing 25th to 75th percentile of comparable sales. Explanatory context accompanies recommendations: "Similar items sold for $45-65. Premium for silk material (+$12). Seasonal demand high (+$8). Excellent condition (+$5)."

**Weekly retraining on fresh data**:

Model retrains every week incorporating the previous week's completed transactions. This keeps pricing current with market trends (sudden demand spikes, seasonal shifts, economic changes). Monitors pricing accuracy by comparing recommended ranges to actual sale prices. Tracks seller override rates (how often sellers change prices) to detect when model confidence is misaligned. Automated alerts trigger additional retraining when accuracy degrades beyond thresholds.

**Production deployment**: 

Deployed on CPU instances since pricing prediction is not latency-critical (can take 1-2 seconds). Caching layer stores pricing for common item types to reduce database queries. Feature store maintains pre-computed category averages and seasonal factors for faster inference.

### Human-in-the-Loop Quality Assurance

**Not fully automated**. When AI confidence scores fall below thresholds or validation flags issues, the system routes listings to human reviewers. This hybrid approach combines AI efficiency (90%+ of listings fully automated) with human judgment (10% reviewed), maintaining quality while achieving scale.

**Review queue prioritization using historical risk data**:

Luxury brands reviewed first due to high financial risk (misidentified $2000 Gucci bag hurts brand). New product categories with limited training data receive extra scrutiny. Items flagged by multiple validation rules (multiple red flags indicate higher error probability). Random sampling (2-3% of all listings) for continuous quality monitoring and model calibration.

**Reviewer interface designed for efficiency**:

Displays AI-generated listing alongside detected attributes and confidence scores. Highlights validation failures and areas requiring attention. Provides dropdown menus for common corrections based on historical edit patterns. One-click approval for listings that need minor human verification but no edits.

**Active learning feedback loop powered by real usage data**:

Seller edit tracking captures every change sellers make to AI-generated listings. If sellers consistently change "silk" to "silk blend," this signals vision model needs calibration. Edits feed into weekly model retraining weighted by seller reputation (experienced sellers' edits weighted higher).

Buyer engagement metrics (clicks, views, favorites, questions asked) signal description quality. Listings generating high engagement indicate effective content. Low engagement despite competitive pricing suggests description issues. Engagement patterns train the generative model on what language drives conversions.

Sales outcomes provide ultimate validation. Items that sell quickly at recommended prices validate both description quality and pricing accuracy. Items sitting unsold for weeks signal problems. Time-to-sale data at different price points trains pricing model. Final sale prices compared to AI recommendations measure accuracy.

**Curation prevents noisy feedback**:

Not all seller edits are incorporated. Edits from high-reputation sellers (thousands of successful sales) weighted heavily. Edits from new sellers (under 10 sales) reviewed before incorporation. Contradictory edits (different sellers changing same attribute different ways) flagged for human decision. Only statistically significant patterns (20+ sellers making same edit) trigger model updates.

**Continuous improvement cycle**:

Weekly retraining incorporates curated feedback from previous week. Monthly major updates adjust model architecture or prompt engineering. Quarterly reviews analyze performance trends and plan strategic improvements. A/B testing framework validates improvements before full deployment.

---

## How ThreadUp's Proprietary Data Powers QuickList

### Data as Competitive Moat

ThreadUp's 172 million item consignment history provides multiple competitive advantages that competitors cannot easily replicate.

**Vision model training data (172 million professionally-labeled images)**:

Professional product photos shot with standardized lighting, neutral backgrounds, and consistent angles. Verified attribute labels from trained specialists following standardized criteria, not user-generated guesses. Expert annotations include exact category placement in ThreadUp's hierarchical taxonomy (evening gowns vs cocktail dresses vs casual dresses), material composition verified through physical inspection and tag reading (100% silk vs silk-polyester blend vs polyester), condition grades assessed using identical criteria across all 172 million items (like new requires zero wear signs, gently used allows minor wear, etc.), brand identification and authentication (designer logos verified, construction quality assessed, counterfeit detection).

**Generative model training data (best-performing descriptions)**:

Professional copywriting examples from years of creating consignment listings optimized for conversion. A/B test results showing which description variants drive higher engagement and sales. SEO performance data indicating which titles rank highest in search engines. Conversion metrics tied to specific language patterns (mentioning "sustainable" increases conversions, mentioning "pre-owned" decreases conversions).

**Pricing model training data (172 million actual transactions)**:

Actual sale prices, not just asking prices (many listings never sell, only completed transactions matter). Time-to-sale patterns showing how pricing affects selling speed across categories and seasons. Seasonal demand curves based on years of data (winter coats peak November, crash March). Geographic price variations (same dress sells for $85 in San Francisco, $62 in Des Moines). Seller tier effects (professional sellers achieve 15% price premium over casual sellers).

**Active learning feedback accumulating from real usage**:

As sellers use QuickList in production, the system captures what sellers edit (signals model errors and improvement areas), which listings get high buyer engagement (signals effective descriptions), which listings sell and at what prices (ultimate success validation), and how long items take to sell (pricing accuracy indicator).

**Why competitors cannot replicate this data advantage**:

Poshmark, Mercari, and Depop rely on user-generated listings with inconsistent photo quality (poor lighting, cluttered backgrounds, bad angles), unverified attribute labels often containing errors (users guess materials, misidentify conditions, make authentication mistakes), no professional verification process (no trained specialists inspecting items), and years of accumulated noisy, unreliable training data (cannot easily clean or correct historical errors).

Building equivalent data quality would require competitors to:

Hire and train hundreds of product assessment specialists. Inspect and professionally photograph millions of items. Develop and enforce standardized assessment criteria. Accumulate years of verified transaction data. Estimated cost exceeds $50 million and requires 3-5 years minimum, creating substantial barriers to entry.

**Similar to how Shopify leverages merchant data**:

Shopify's AI product tagging improves continuously using merchant correction data. When merchants edit AI-generated tags, that feedback trains the model. Shopify has tens of millions of products with merchant corrections, creating a data advantage competitors cannot easily replicate.

QuickList implements the same principle at larger scale with richer data. ThreadUp has 172 million items with professional assessments, far exceeding typical e-commerce data quality.

---

## Production System Architecture

### Infrastructure Requirements

**Cloud deployment on AWS or Google Cloud Platform**: Auto-scaling infrastructure handles variable load (peak during evenings and weekends when sellers list items). Multiple availability zones ensure reliability and disaster recovery. Load balancers distribute traffic across instances. Geographic distribution reduces latency for sellers across North America.

**Database architecture**: PostgreSQL for structured data including user accounts, listing history, transaction records, and seller profiles. Time-series database (InfluxDB or TimescaleDB) for metrics and monitoring data. Redis for caching layer reducing repeated API calls and database queries. S3 or Cloud Storage for image storage with CloudFront or Cloud CDN for fast worldwide delivery.

**AI model deployment infrastructure**: 

Fine-tuned CLIP model on GPU instances (AWS EC2 P3 or GCP with NVIDIA T4/V100 GPUs) with auto-scaling based on load. Groq API integration for Llama 3.3 70B with connection pooling and retry logic. OpenAI API integration for GPT-4 Turbo fallback. XGBoost pricing models on CPU instances (c5.2xlarge or equivalent). Model versioning system enabling A/B testing and rollback. Feature store for pre-computed values accelerating inference.

**Monitoring and observability**: Real-time dashboards tracking end-to-end latency (target under 5 seconds from photo upload to listing display), AI accuracy metrics (attribute detection correctness, description quality scores), cost per listing (API costs, infrastructure costs), human review rate (percentage requiring manual review), and seller satisfaction metrics (edit rates, adoption rates, NPS scores). Alerting triggers on anomalies or degraded performance (accuracy drops, latency spikes, cost overruns). Log aggregation and analysis for debugging and optimization.

**Security and compliance infrastructure**: User authentication and authorization with role-based access control. PCI DSS compliance for payment data handling. GDPR compliance for EU sellers (data portability, right to deletion). SOC 2 certification for enterprise security. Content moderation systems for policy enforcement. Rate limiting prevents abuse and controls costs. DDoS protection and web application firewall.

### Production Data Flow

Seller uploads product photo via mobile app or web interface. Image stored in S3/Cloud Storage, resized and optimized, CDN URL generated for fast retrieval. Computer vision analysis begins immediately with fine-tuned CLIP model processing image and outputting category, type, materials, colors, style, and condition with confidence scores for each attribute. If any critical attribute has confidence below 0.75, item flagged for human review and processing pauses. Otherwise, detected attributes packaged as structured JSON.

Generative AI receives JSON input with strict validation constraints. Llama 3.3 70B via Groq generates title, description, bullet points, and meta description following carefully engineered prompt. Generation completes in under 2 seconds. Validation layer immediately scans output for color hallucinations, material inconsistencies, category mismatches, and content quality issues. If validation detects problems, output rejected and GPT-4 Turbo attempted as fallback. If GPT-4 also fails validation, template-based generation used as guaranteed fallback.

Keyword extraction combines rule-based approach (attributes become keywords) with extractive summarization from generated description. Primary keywords (8) and long-tail keywords (12) optimized for target platform's search algorithm.

Pricing model queries transaction database for comparable sales (same category, similar brand tier, comparable condition, recent sales within 30-90 days). XGBoost processes listing attributes and comparable sales to generate price range with explanations. Pricing completes in 1-2 seconds.

Platform-specific formatting applied based on seller's target (Shopify product schema, Amazon listing format, Etsy character limits, WooCommerce fields). Complete listing presented to seller with ability to edit any field. Confidence scores displayed transparently (low confidence warns seller to review carefully). System captures all seller interactions (edits made, time spent reviewing, final approval) for feedback loop.

**Total target latency**: Under 5 seconds from photo upload to complete listing displayed to seller.

---

## Demo vs Production Implementation

### Current Streamlit Demo Application

This repository contains a proof-of-concept demonstrating QuickList's capabilities using free-tier APIs and services.

**Technologies used in demo**:

| Component | Demo Technology | Limitations |
|-----------|----------------|-------------|
| Computer Vision | Google Cloud Vision (1000/month free tier), Amazon Rekognition (5000/month free first year), CLIP via HuggingFace Inference API | Not fine-tuned on ThreadUp data; rate limited; lower accuracy than production |
| Generative AI | Groq free tier (Llama 3.3 70B), DeepInfra, Together AI, Pollinations, HuggingFace (Qwen 2.5 72B, Mistral 7B) | 6-tier fallback compensates for free tier unreliability; generic prompts not optimized for ThreadUp |
| Validation | Color hallucination prevention, basic content checks | Same validation logic as production |
| Pricing | Mock XGBoost with placeholder logic | Cannot provide accurate pricing without access to ThreadUp's transaction database |
| Infrastructure | Single Streamlit instance running locally or on Streamlit Cloud | No scaling, no database persistence, no monitoring, no user accounts |

**Purpose of demo**: Validates that the technical approach works end-to-end. Proves that multi-tier fallback AI can achieve reliability even with free APIs. Demonstrates user experience and interface flow. Provides working foundation for production build. Shows investors and stakeholders a functioning prototype.

**Why demo uses free tiers**: Proof-of-concept does not require production-grade accuracy or reliability. Free tiers provide sufficient functionality to validate approach. Demonstrates that QuickList works without requiring upfront investment in paid APIs. Multiple fallback tiers compensate for free tier rate limits and occasional failures.

### Production System Additions

**Fine-tuned models trained on ThreadUp's proprietary data**:

CLIP fine-tuning on 172 million professionally-labeled images costs $75K-150K one-time, requires 2-4 weeks on GPU cluster, improves accuracy by 10-20% on fashion attributes. Llama 3.3 70B fine-tuning on ThreadUp's 50K-100K best-performing descriptions costs $20K-40K, creates custom model writing in ThreadUp's brand voice. XGBoost training on 172 million transactions provides accurate pricing impossible without this data.

**Paid API tiers with guaranteed SLA**:

Groq Enterprise API provides dedicated throughput, guaranteed latency, and 99.9% uptime. OpenAI Enterprise tier for GPT-4 includes higher rate limits and priority access. Google Cloud Vision committed use discounts for high volume.

**Production cloud infrastructure**:

AWS or GCP deployment with auto-scaling, load balancing, multi-region redundancy. PostgreSQL database cluster for structured data, Redis for caching. S3 and CloudFront for image delivery. Monitoring via Datadog or New Relic. Costs approximately $15K-25K monthly at 1.6M listings annually.

**Human review workflows**:

Review queue system with prioritization logic. Reviewer interface and training materials. Quality assurance team (10-15 reviewers) for high-value items. Escalation procedures for edge cases.

**A/B testing framework**:

Infrastructure to test prompt variations, model versions, and UI changes. Statistical analysis of conversion impacts. Gradual rollout mechanisms (canary deployments, percentage-based routing).

**Active learning pipeline**:

Data collection capturing seller edits, buyer engagement, sales outcomes. Feedback curation removing noise and outliers. Automated retraining pipelines (weekly for pricing, monthly for generative models). Model performance monitoring triggering retraining when accuracy degrades.

**Security and compliance implementations**:

SOC 2 certification process. GDPR compliance including data portability and deletion. PCI compliance for payment handling. Penetration testing and security audits.

**Total investment required**: Initial $850K to $2.1M covering model fine-tuning ($100K-200K), infrastructure setup ($150K-300K), API costs for first year ($50K-100K), human reviewer team hiring and training ($200K-400K), engineering team (5-7 engineers for 6 months at $400K-800K), security and compliance ($50K-100K), and contingency buffer ($100K-200K). Ongoing costs scale with volume, primarily driven by API usage and infrastructure.

---

## Business Impact and Market Opportunity

### Market Size

80 million active peer-to-peer sellers in North America fragmented across Poshmark (80 million registered users), Mercari (50 million users), and Depop serving younger demographics.

### Revenue Opportunity

Capturing just 2% of the market represents 1.6 million sellers listing 10 items yearly at $25 average, generating $400 million in gross merchandise value annually. At ThreadUp's 15% transaction fee, this translates to $60 million in annual revenue, nearly doubling current quarterly revenue of approximately $80 million.

### Return on Investment

Initial investment of $850K to $2.1M with first-year revenue approximately $30 million under conservative ramp-up assumptions (reaching only 50% of target 1.6M sellers in year one). Payback period ranges from several months to 18 months depending on adoption rate. Gross profit exceeds initial investment within first year. By year three, annual revenue from QuickList-enabled sellers reaches $60M with 80% gross margin after infrastructure and API costs.

### Competitive Advantages (Porter's Five Forces)

**Threat of new entrants diminishes** because QuickList creates an operational moat requiring significant investment ($850K-$2.1M initial), proprietary training data (172 million professionally-labeled items), and time to accumulate (3-5 years minimum to build equivalent dataset).

**Supplier bargaining power decreases** as sellers become dependent on QuickList for efficient listing, creating switching costs that prevent them from leaving ThreadUp for competitors. Sellers build inventory on ThreadUp, optimize workflows around QuickList, and achieve higher sales through better listings.

**Buyer bargaining power shifts favorably** through reduced information asymmetry as AI-generated descriptions are consistent, complete, and trustworthy compared to variable-quality manual listings on competitor platforms.

**Threat of substitutes weakens** because 30-second listing process is faster than all alternatives: manual listing on Poshmark/Mercari (5-10 minutes), traditional ThreadUp consignment (wait time for processing), bulk listing services (expensive, inconsistent quality).

**Competitive rivalry shifts in ThreadUp's favor** because competitors lack meaningful listing technology differentiation and cannot easily replicate the data advantage (172M professional assessments) or the generative AI implementation quality.

---

## Implementation Timeline

### 12-Week Phased Rollout

**Phase 1 (Weeks 1-3): Technical Integration and Pilot**

500 beta sellers selected from high-volume, engaged user base. Focus on accuracy validation comparing AI-generated listings to manual listings across categories. Usability testing identifies friction points in user interface. Collect baseline metrics: listing time per item (target <30 seconds), seller satisfaction surveys (NPS score), listing quality scores (human evaluation), and attribute detection accuracy (validated against ground truth). Iterate on validation rules based on observed errors. Refine prompt engineering when descriptions miss key selling points. Adjust confidence thresholds to optimize human review rate.

**Phase 2 (Weeks 4-6): Expansion and A/B Testing**

5,000 sellers with rigorous A/B testing framework. Control group creates listings manually. Treatment group uses QuickList. Measure conversion rates (listing views to sales), sell-through rates (percentage of items selling within 30 days), time-to-sale (days from listing to purchase), and buyer engagement (clicks, favorites, questions). Validate that AI-generated listings perform at least as well as manual listings, ideally 5-10% better due to consistency and SEO optimization. Monitor seller override rates (how often sellers edit AI output) to identify systematic issues. Collect detailed feedback through surveys and interviews.

**Phase 3 (Weeks 7-9): Scale and Pricing Integration**

50,000 sellers while deploying pricing recommendations alongside description generation. Monitor pricing accuracy by comparing recommended ranges to actual sale prices. Track seller override rates on pricing (lower override rate indicates higher trust). Refine pricing model based on early results and seller feedback. Ensure infrastructure scales smoothly (latency remains under 5 seconds despite 10x traffic increase). Begin accumulating active learning data at meaningful scale.

**Phase 4 (Weeks 10-12): Full Rollout Preparation**

Complete infrastructure scaling to support 1.6 million target sellers over following 12 months. Deploy comprehensive monitoring dashboards tracking all key metrics. Implement alerting for anomalies and degraded performance. Train customer support team on QuickList features and common issues. Create help documentation and video tutorials. Launch marketing campaign promoting new capability ("List your entire closet in 30 minutes"). Begin weekly model retraining incorporating feedback from pilot and expansion phases.

---

## Why This Is Real Enterprise AI, Not Research

QuickList represents an efficiency-focused generative AI investment with clearly measurable intermediate value, not exploratory research or speculative technology deployment.

**Augments existing workflow rather than replacing humans**: QuickList reduces listing time from 5-10 minutes to 30 seconds while keeping sellers in control. Sellers review AI-generated listings and can edit any field. This human-in-the-loop approach ensures quality while achieving efficiency gains. Similar to how Shopify's AI product tagging assists merchants rather than making final decisions.

**Measurable business metrics enable early validation**: Listing time and cost per item are already tracked operational metrics at ThreadUp. Business impact can be validated within weeks through Phase 1 pilot with 500 sellers, reducing investment risk. Unlike speculative AI projects with unclear ROI timelines, QuickList shows results immediately.

**Intermediate value realization through process improvements**: Faster and more standardized listings improve operational predictability, supporting downstream functions. Consistent attribute tagging improves search and recommendation algorithms. SEO-optimized descriptions increase organic traffic. Better pricing recommendations reduce time-to-sale. Value is realized through measurable process improvements, not just eventual revenue gains.

**Continuous improvement through active learning powered by real usage data**:

System learns from every listing created in production. Seller edits provide correction signals showing where AI made mistakes. When sellers change "silk" to "silk blend," this signals vision model needs calibration on material detection. Buyer engagement provides quality signals indicating which descriptions drive conversions. Listings with high click-through rates and favorites indicate effective content. Low engagement despite competitive pricing suggests description issues. Sales outcomes provide ultimate validation. Items selling quickly at recommended prices validate both description quality and pricing accuracy. Items sitting unsold trigger investigation of potential issues.

Selected feedback is curated before incorporation. High-reputation sellers' edits weighted heavily (thousands of successful sales indicate expertise). New sellers' edits reviewed before incorporation (may reflect misunderstanding rather than AI error). Contradictory edits flagged for human decision (different sellers making opposite changes). Only statistically significant patterns (20+ sellers making same edit) trigger model updates automatically.

Periodic retraining cycles systematically improve accuracy. Weekly retraining for pricing model incorporating latest transaction data. Monthly updates for generative model refining prompts and fine-tuning. Quarterly reviews analyze performance trends and plan strategic improvements.

**Data drift monitoring ensures continued relevance**:

Fashion trends and inventory mix evolve continuously. Seasonal changes affect product mix (winter coats dominate Q4, swimwear peaks Q2). Trend cycles bring new styles (Y2K revival, cottagecore, etc.). Consumer preferences shift (sustainability messaging becomes more important). New brands emerge while others fade. Economic conditions affect pricing.

System monitors model performance continuously. Attribute detection accuracy tracked weekly. If accuracy degrades beyond threshold (e.g., drops from 92% to 88%), automated alert triggers investigation. Description quality scores from buyer engagement tracked monthly. Declining engagement rates signal need for prompt refinement. Pricing accuracy monitored by comparing recommendations to actual sales. Increasing seller override rates indicate model recalibration needed.

When monitoring detects degradation, automated retraining pipelines execute. Fresh data incorporated, model weights updated, validation performed on holdout set, gradual rollout ensures no regression, and full deployment after validation. This continuous adaptation maintains accuracy as market conditions evolve.

---

## Risk Mitigation Strategies

**Technology accuracy risks with multiple mitigation layers**:

Confidence score thresholds route uncertain predictions to human review rather than displaying potentially incorrect information to sellers. Conservative thresholds (0.75 for critical attributes) ensure high-quality automated listings while accepting higher review rates initially. Seller editing capability allows corrections when AI makes mistakes, treating sellers as final quality gate. All edits captured for active learning feedback. Validation rules prevent common generative AI errors like color hallucinations, material inconsistencies, and category mismatches before content reaches sellers. Continuous model improvement through active learning addresses accuracy issues systematically over time. Initial accuracy of 85-90% improves to 95%+ within six months as feedback accumulates.

**User adoption risks addressed through trust-building**:

Optional adoption ensures sellers aren't forced to use AI if they prefer manual listing. No penalty for opting out. Gradual migration allows sellers to test QuickList on a few items before committing. Transparent confidence scores build trust by showing sellers when AI is uncertain. Low confidence warnings prompt careful review. Sellers learn to trust high-confidence predictions over time. Extensive beta testing with 500 early adopters identifies issues before broad rollout. Beta participants tend to be enthusiastic early adopters providing constructive feedback.

A/B testing demonstrates measurable conversion improvements providing data-driven proof of value. Showing sellers that AI-generated listings achieve 5-10% higher conversion rates drives adoption better than marketing claims. Success stories from beta users shared in community forums create social proof. Onboarding tutorials and help documentation reduce friction. Video guides show how to use QuickList effectively. Customer support trained to handle questions and troubleshooting.

**Competitive response risks mitigated by sustainable advantages**:

Proprietary datasets create multi-year lead time for competitors attempting to replicate. ThreadUp's 172 million professionally-labeled items accumulated over years cannot be quickly recreated. Competitors would need to implement professional assessment operations (costly), accumulate years of verified data (time-consuming), and fine-tune models (expensive). Combined barrier estimated at $50M+ and 3-5 years minimum.

Patent protection on specific implementations of generative AI for product listings. While core technologies (CLIP, LLMs) are public, ThreadUp can patent novel approaches to validation, active learning integration, and hybrid human-AI workflows. Patents create additional barriers even if competitors acquire training data.

Continuous innovation maintains advantage as competitors eventually catch up. By the time competitors deploy basic AI listing tools, ThreadUp is already several versions ahead with superior accuracy, faster generation, and better integration. Innovation roadmap includes features like automated product photography recommendations, dynamic pricing adjusting to real-time demand, and personalized listing optimization based on seller history.

**Platform quality risks managed through multi-layer controls**:

Seller scoring systems give high-quality sellers (strong sales history, low return rates, positive reviews) less review overhead while scrutinizing new or low-rated sellers more closely. Trusted sellers' listings proceed with minimal review. New sellers get higher review rates until they establish track record. Automated quality flags catch problematic listings before they go live. Multiple validation failures trigger automatic human review. Patterns indicating potential policy violations flagged immediately. Human oversight for high-risk cases maintains quality standards. Luxury brands always reviewed to protect against counterfeits and authentication errors. Items with damage or significant condition issues reviewed to ensure accurate disclosure. Controversial categories (children's items, undergarments) get extra scrutiny for policy compliance.

Random sampling (2-3% of all listings) for continuous quality monitoring ensures even high-confidence automated listings maintain standards. Statistical process control charts detect quality degradation trends early. Quarterly audits review samples comprehensively and recommend process improvements.

---

## Success Metrics

### Primary Business KPIs

Listing creation time reduced from 5-10 minutes baseline to under 30 seconds target, representing 90%+ time savings. Measured across all sellers using QuickList, tracked automatically through application logs.

Seller adoption rate targeting 2% market capture representing 1.6 million sellers over 12 months. Measured through monthly active users of QuickList feature. Broken down by seller cohort (new vs returning, casual vs professional).

Gross merchandise value generated targeting $400 million annually from QuickList-enabled listings. Tracked through transaction data, attributed to listings created with AI assistance. Compared against control group creating manual listings.

Seller retention improvement reducing churn rate by measurable percentage. Churn defined as sellers inactive for 90+ days. Hypothesis: QuickList reduces effort burden, keeping sellers engaged longer. Measured through cohort analysis comparing QuickList users vs non-users.

### Quality and Accuracy Metrics

Attribute detection accuracy above 90% validated on holdout test set of 10,000 items with verified ground truth labels. Broken down by attribute type: category (target 95%), material (target 88%), color (target 92%), condition (target 85%). Tracked weekly with automated alerts if any metric degrades beyond threshold.

Description quality score measured through human evaluation on 1-5 scale. Random sample of 200 listings weekly evaluated by professional copywriters. Criteria include relevance to product, persuasiveness, grammatical correctness, brand voice alignment, and SEO optimization. Target average score 4.2+.

SEO performance improvement measured by search ranking increases for AI-generated listings vs manual listings. Track position in search results for target keywords. Measure organic traffic to listings. Target 15-20% improvement in search visibility.

Human review rate below 10% of total listings indicating high automation rate with quality maintenance. Initial target 15% during first month, decreasing to 10% by month three as models improve. Broken down by trigger reason (low confidence, validation failures, high-value items).

### Downstream Business Impact

Sell-through rate measuring percentage of AI-generated listings that successfully sell within 60 days. Compared against baseline sell-through rate for manual listings. Target 5-10% improvement due to better descriptions and pricing.

Time-to-sale tracking median days from listing creation to first purchase. Faster time-to-sale indicates effective pricing and descriptions attracting buyers quickly. Compared against manual listing baseline. Target 15-20% reduction in time-to-sale.

Buyer engagement metrics including click-through rate from search results, product page views, favorites added, and buyer questions asked. Higher engagement indicates compelling descriptions and accurate categorization. Track trends over time as models improve.

Seller satisfaction measured through Net Promoter Score specifically for QuickList feature. Monthly survey asking "How likely are you to recommend QuickList to other sellers?" Target NPS 50+ indicating strong satisfaction. Supplemented with qualitative feedback on improvement areas.

---

## Conclusion and Recommendation

**Proceed with QuickList implementation.**

The decision to implement QuickList represents ThreadUp's optimal path to stopping sellers from leaving the platform, recapturing premium inventory currently lost to peer-to-peer competitors, establishing defensible competitive advantages through proprietary data and generative AI implementation, and positioning as the innovation leader in AI-powered resale commerce.

QuickList is a **generative AI solution** at its core. Large language models create unique, persuasive product descriptions that cannot be generated through traditional AI approaches. This content generation capability, combined with computer vision attribute detection and machine learning pricing, solves ThreadUp's fundamental business problem: listing friction preventing sellers from efficiently listing high-value inventory.

The combination of **zero-shot computer vision fine-tuned on 172 million professional assessments**, **efficient large language models with strict validation preventing hallucinations**, **interpretable pricing models building seller trust**, and **continuous improvement through active learning on real usage data** creates a production-ready system that solves a real business problem with measurable ROI.

ThreadUp's unique competitive advantage lies in its proprietary data. Competitors cannot easily replicate 172 million professionally-labeled items accumulated through years of consignment operations. This data enables model fine-tuning that dramatically improves accuracy, creating a sustainable moat protecting ThreadUp's investment.

QuickList is not speculative AI research. It is an operational efficiency investment with clear metrics, early validation opportunities through phased rollout, measurable intermediate value through process improvements, and a realistic path to positive return on investment within 18 months. Initial investment of $850K to $2.1M generates estimated $60 million in annual revenue at full deployment, nearly doubling ThreadUp's quarterly revenue.

The phased 12-week rollout enables risk mitigation through early validation, iterative refinement based on real feedback, and gradual scaling as accuracy and reliability improve. Multiple layers of quality assurance including confidence scoring, rule-based validation, and human review maintain listing quality while achieving 90%+ automation rates.

---

## Team

Noelia Cornejo  
Dedan Deus  
Emily Bendeck Garay  
Qazi Fabia Hoq (Project Lead, inspired by personal product tagging experience)  
Esha Malhi

**Course**: MMAI 5090 F - Business Applications of AI II  
**Instructor**: Dr. Divinus Oppong-Tawiah  
**Institution**: Master of Management Analytics in AI  
**Date**: February 11, 2026

---

## Repository

This repository contains a proof-of-concept Streamlit demo application using free-tier APIs to validate QuickList's technical approach. The demo demonstrates end-to-end functionality from image upload to complete listing generation, validates multi-tier AI fallback reliability, and provides a working foundation for production implementation.

Production deployment would require paid API tiers with guaranteed SLA, fine-tuned models trained on ThreadUp's proprietary 172 million item dataset, production cloud infrastructure with auto-scaling and monitoring, human review workflows and quality assurance processes, A/B testing framework for continuous optimization, and active learning pipelines incorporating real usage feedback as detailed throughout this document.

**License**: Academic project for educational purposes.
