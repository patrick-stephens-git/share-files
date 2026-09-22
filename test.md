## Problem Statement
- **What problem are we solving?** Users who search with concept-based, long tail search queries (e.g. "premium drivers," "sunscreen shirt," "feather coat") don't see relevant products (that are in our product catalog) in their search results, so engagement decreases (less clicks, lower add-to-cart rates, and lower conversion), because of lexical and vector search fail to map concept-based queries to relevant products because product data lacks concept vocabulary because merchant-authored titles and descriptions record literal attributes (material, color, size) rather than the abstract use-cases or concepts a customer's query implies.

### How do we know this is a problem?
- **Business impact:** We would expect to see purchase conversion rate on sessions containing concept-based, long-tail queries (e.g. "sunscreen shirt," "premium drivers," "feather coat") measurably lower than on sessions containing head, exact-match queries — for example, a 10+ point gap in conversion rate between the two — even though matching products exist in the catalog.
- **Behavioral signals:** We would expect to observe users reformulating or abandoning concept-based searches at a higher rate than head queries — for example, a search for "sunscreen shirt" followed within the same session by a broader reformulated query (e.g., "shirt") or by a zero-click exit. We would also expect to see users applying manual filters or facets immediately after a concept query returns poor results, as a workaround for the search engine's failure to map the concept to the catalog.
- **Voice-of-customer signals:** We would expect to hear complaints in support tickets, reviews, or user research citing phrases like "can't find," "search doesn't understand what I'm looking for," or similar, clustered around descriptive or use-case language (e.g. "sunscreen shirt," "premium drivers") rather than brand or model-number terms.
- **Market signals:** We would expect to find competitors or third-party vendors explicitly marketing "concept search," "semantic search," or "natural language search" as a differentiator against traditional keyword search, or analyst commentary calling out lexical-search limitations for long-tail e-commerce queries.
---

### Market Signals Summary
- Search vendors are actively marketing semantic, natural-language, and concept search as an explicit differentiator against traditional keyword search, naming the same failure mode described in the problem statement — that literal keyword matching cannot connect a shopper's descriptive or use-case query to product data that doesn't share those words: [Coveo](https://www.coveo.com/blog/decoding-shopper-intent-with-semantic-search/) · [Coveo via Retail Dive](https://www.retaildive.com/spons/same-query-different-intent-the-revenue-risk-of-irrelevant-search-results/749315) · [Constructor](https://constructor.com/blog/natural-language-search-engines) · [Marqo](https://www.marqo.ai/blog/semantic-search-vs-keyword-search-ecommerce) · [Bloomreach](https://www.bloomreach.com/en/products/ecommerce-search/search-intelligence).
- Independent, deployed industry research from two major retail/marketplace search teams (Best Buy and Alibaba's Taobao) confirms lexical keyword matching specifically under-serves long-tail queries because of a genuine vocabulary/semantic gap against product titles, and that closing this gap moved measurable revenue metrics (conversion, GMV): [arXiv — Best Buy](https://arxiv.org/html/2505.01946v1) · [arXiv — Alibaba/Taobao](https://arxiv.org/abs/2311.03758).
- When native site search fails on a descriptive, concept-based query, some shoppers now route around it entirely by using a third-party conversational AI shopping assistant that accepts natural-language descriptions of what they want: [9to5mac](https://9to5mac.com/2025/11/24/chatgpt-adds-ai-shopping-assistant-to-find-the-right-products-faster/) · [Engadget](https://www.engadget.com/ai/chatgpt-now-offers-a-dedicated-shopping-assistant-180000034.html).
- Technical practitioners discussing e-commerce search publicly (independent of any vendor) describe the same root cause in their own words — that shoppers search by intent, not by the literal words a search engine matches against — corroborating the problem statement's mechanism from a non-commercial, non-analyst source: [Hacker News](https://news.ycombinator.com/item?id=38771513) · [Hacker News](https://news.ycombinator.com/item?id=34391617).
---

- **New First Principle:** A customer's concept-based query can be automatically translated into the literal vocabulary and attributes that would satisfy it, before retrieval happens — so relevance no longer depends on the query and the product record sharing the same words.
---

## Hypothesis
A customer's concept-based query being automatically translated into the literal vocabulary and attributes that satisfy it, before retrieval happens, will result in concept-based, long-tail search sessions returning relevant catalog products even when the query and product record share no words, thus shoppers who search using concept-based language (e.g. "sunscreen shirt," "premium drivers," "feather coat") can find and purchase products that already exist in the catalog, and purchase conversion rate on concept-based, long-tail query sessions should close some or all of the gap to head-query conversion.
---

- **Solution Constraints:**
1. Must integrate with Elasticsearch for storing and returning ranked product documents rather than introducing a parallel retrieval store.
2. Must not add significant latency to search response time.
3. Platform: web, app, stores.
---

### Idea 1: Query Concept Expansion
- **"What if ...?"** What if we took the shopper's raw query, expanded it into the literal attribute vocabulary that already exists in the catalog, and passed that expanded query into our existing retrieval pipeline, so relevant products surface without us ever having to rewrite the catalog itself?
- **Translation:** "How might we translate what a shopper means into the words our catalog already understands?"
- **Imagine this:** Shoppers type however they naturally describe what they want, and don't need to learn or guess the exact words the catalog uses — the system meets them in their own language while nothing about how products are stored or ranked has to change.

### Idea 2: Catalog Concept Enrichment
- **"What if ...?"** What if we took each product's existing attributes, inferred the underlying concepts those attributes satisfy, and added that concept vocabulary directly onto the product record, so the catalog itself already speaks the language shoppers search in?
- **Translation:** "How might we make every product's data already contain the concepts a shopper would use to look for it?"
- **Imagine this:** A product that already exists in the catalog becomes findable by every reasonable way a shopper might describe wanting it, without a shopper's query ever needing to change.

### Idea 3: Concept-to-Attribute Bridge Table
- **"What if ...?"** What if we pre-built a lookup table connecting shopper concepts to the specific attribute values that satisfy them, computed the mapping ahead of time, and only did a simple table lookup at query time, so we close the vocabulary gap without adding latency to the moment a shopper actually searches?
- **Translation:** "How might we solve the vocabulary gap once, offline, instead of solving it fresh for every search?"
- **Imagine this:** Shoppers get concept-based results just as fast as they get results for an exact-match query, because the heavy translation work already happened before they ever typed anything.
---

### Idea 1: Live Concept Synthesis
- **"What if ...?"** What if, instead of ever expanding a query ahead of time or enriching the catalog in advance, we let a reasoning process read the raw product corpus and the raw query together at the exact moment of search, and generate a brand-new synthetic match for a concept that has never been searched before?
- **Technology Inflection:** "How might we make the system capable of understanding a concept it has never seen, the first time it's ever typed?"
- **Imagine this:** The magic is that a query which has literally never existed before — an invented concept combining two ideas no one anticipated, like "a coat that doubles as sunscreen" — still returns something coherent, because the system is reasoning about meaning live, not looking anything up in a table someone built ahead of time.
---

### Idea 2: Living Query-Translation Agent
- **"What if ...?"** What if an agent watched every concept-based query in real time, maintained its own evolving model of which concepts map to which literal attributes, tested new candidate mappings against live engagement outcomes, promoted the mappings that worked into the production query-translation layer, and retired the ones that didn't — continuously, without a human ever approving an individual mapping?
- **"How might we ...?"** How might we let the search engine's understanding of shopper language improve itself, at the pace shoppers actually invent new ways of describing things?
    - **Tools & Integrations:**
        - Real-time query stream
        - The query-translation / expansion layer this agent modifies
        - Elasticsearch and vector index (to test candidate translations against real retrieval)
        - Engagement/conversion analytics feed
        - Shadow-traffic or champion/challenger testing infrastructure
    - **Agent Loop:**
        - Step 1 — perceive: detect a new or recurring concept-based query pattern not yet covered by an existing translation mapping.
        - Step 2 — reason: generate one or more candidate literal-attribute translations for the concept.
        - Step 3 — act: run the candidate translation against a slice of live or shadow traffic for that query pattern.
        - Step 4 — observe: measure whether the candidate translation improved engagement relative to the untranslated baseline.
        - Step 5 — re-plan: promote the winning candidate into the production mapping permanently, or discard it and generate a new candidate, looping back to Step 2.
    - **Escalation Threshold:** Escalate when a candidate translation would map a concept into a regulated or sensitive product category, or when no candidate improves outcomes after a defined number of iterations.
    - **Replaced Workflow:** Replaces the manual work of a search-relevance/query-understanding team hand-curating synonym dictionaries and query-rewrite rules.
- **Imagine this:** The search engine keeps getting better at understanding shoppers on its own — no relevance-team meeting ever has to happen to decide that "sunscreen shirt" should mean UPF apparel.

### Idea 3: Preemptive Concept Taxonomy Agent
- **"What if ...?"** What if an agent continuously scanned the wider language people use to describe products, built and maintained its own evolving taxonomy of concepts, and preemptively wrote concept-level tags onto every product in the catalog that satisfies each concept — before any shopper's query ever exposes the gap?
- **"How might we ...?"** How might we make the catalog's vocabulary arrive ahead of the queries that would have exposed the gap?
    - **Tools & Integrations:**
        - External language-signal sources (search trend data, review text, social/forum language)
        - Product catalog / PIM (read attributes, write concept tags)
        - Elasticsearch and vector index (re-index updated concept tags)
        - Internal query logs (to prioritize concepts gaining real search volume)
    - **Agent Loop:**
        - Step 1 — perceive: continuously ingest external language signals and internal query trends to detect emerging or growing concept terms.
        - Step 2 — reason: for each concept, determine which existing catalog attributes would satisfy it and identify candidate qualifying products.
        - Step 3 — act: write the concept tag onto every qualifying product's record.
        - Step 4 — observe: after re-indexing, monitor whether products carrying the new tag start appearing in, and converting on, matching concept queries.
        - Step 5 — re-plan: if a tag isn't producing engagement once queried, refine the qualifying criteria for that concept and reapply; if it is working, expand concept-detection to adjacent, related concepts.
    - **Escalation Threshold:** Escalate when a concept tag would make a safety, medical, or regulatory claim (e.g., tagging a garment "sun-protective" without a verified UPF rating on file).
    - **Replaced Workflow:** Replaces the manual, periodic taxonomy-expansion work of a merchandising/catalog team researching trending terminology and manually re-tagging matching products.
- **Imagine this:** The catalog's vocabulary keeps pace with how people actually talk about wanting things — arriving ahead of the queries that would have exposed the gap, as if the catalog already knew what shoppers were about to start asking for.
---

## Success Metrics:
- [Business Outcome] Conversion Rate (CVR) on concept-based, long-tail query sessions: Directly traces to the Hypothesis's core claim — that purchase conversion rate on concept-based/long-tail sessions should close some or all of the gap to head-query conversion.
  - Success Metric Target: the CVR gap between concept-based/long-tail and head-query sessions narrows measurably, measured over the first 8 weeks post-launch, via analytics event data segmented by query type. Flag: requires instrumentation to classify sessions by query type if not already tagged.
  - Kill Threshold: zero narrowing of the CVR gap after 8 weeks.

- [Business Outcome] Revenue per Visit ($/Visit): Measures total revenue generated per site visit that included a concept-based query — a broader revenue proxy than CVR alone, capturing conversion and order value together.
  - Success Metric Target: $/Visit on sessions containing a concept-based/long-tail query increases relative to baseline, measured over the first 8 weeks post-launch, via revenue and session data segmented by query type.
  - Kill Threshold: no increase in $/Visit despite CVR improving, suggesting gains are offset elsewhere (e.g., lower AOV).

- [Business Outcome] Revenue: Total revenue attributable to concept-based/long-tail query sessions — a coarse, catalog-wide roll-up of the conversion and order-value effects above.
  - Success Metric Target: revenue from concept-based/long-tail sessions increases relative to baseline, measured over the first 8 weeks post-launch, via revenue data segmented by query type.
  - Kill Threshold: flat or declining revenue from this segment despite improved CVR, indicating the segment's volume is too small to matter or gains aren't reaching the top line.

- [Business Outcome] Profit: Measures whether the incremental revenue from closing the vocabulary gap outweighs the cost of building and running the solution.
  - Success Metric Target: profit contribution from concept-based/long-tail sessions is positive net of solution operating cost, measured over the first two quarters post-launch, via finance/revenue data combined with infrastructure cost tracking. Flag: requires a defined cost model for the solution before this can be measured.
  - Kill Threshold: operating cost exceeds incremental revenue after two quarters.

- [Business Outcome] Lifetime Value (LTV): Measures whether shoppers who complete a successful concept-based search go on to have higher long-term value, testing whether closing this gap builds durable value rather than a one-time bump.
  - Success Metric Target: LTV of shoppers with a successful concept-based query session is at or above the LTV of comparable shoppers overall, measured over a rolling 6–12 month window, via customer lifetime value modeling. Flag: requires a defined LTV model with sufficient historical window; may not be measurable until well after launch.
  - Kill Threshold: LTV for this cohort is measurably lower than baseline after the measurement window.

- [Business Outcome] Loyalty: Measures whether shoppers with a successful concept-based search experience are more likely to return and repeat-purchase, a proxy for trust in search.
  - Success Metric Target: repeat-purchase/return rate for shoppers with a successful concept-based query session exceeds the baseline return rate, measured over a rolling 90-day window, via customer repeat-purchase data. Flag: requires defining "loyalty" operationally if not already standardized internally.
  - Kill Threshold: no measurable lift in repeat-purchase rate for this cohort versus baseline after 90 days.

- [Product Outcome] Clicks on concept-based query results: An Input Metric — raw click volume on results returned for concept-based/long-tail queries, an early leading indicator of engagement ahead of any conversion or revenue effect.
  - Success Metric Target: clicks on concept-based query results increase relative to baseline, measured over the first 2 weeks post-launch, via analytics event data segmented by query type. Flag: requires instrumentation to attribute clicks back to concept-based/long-tail query sessions if not already present.
  - Kill Threshold: no increase in raw clicks after 2 weeks.

- [Product Outcome] Click-through Rate (CTR) on concept-based query results: An Input Metric leading toward Conversion Rate (Business Outcome); also reflects whether shoppers are finding relevant results, tying toward the shopper's JTBD.
  - Success Metric Target: CTR on concept-based/long-tail queries rises toward parity with head-query CTR, measured over the first 8 weeks post-launch, via analytics event data segmented by query type.
  - Kill Threshold: no measurable increase in CTR after 8 weeks despite treatment coverage being met.

- [Product Outcome] Product Detail Page Views (PDP Views): An Input Metric — how many product detail pages shoppers view after a concept-based query, a step further down the funnel than a click, leading toward Add-to-Cart and Conversion.
  - Success Metric Target: PDP Views per concept-based query session increase relative to baseline, measured over the first 8 weeks post-launch, via analytics event data segmented by query type.
  - Kill Threshold: no increase in PDP Views despite an increase in Clicks, suggesting shoppers click through but aren't convinced by the detail page — a relevance-quality issue rather than a pure recall issue.

- [Product Outcome] PDP Bounce Rate: A guardrail-adjacent Input Metric — the rate at which shoppers leave a product detail page immediately after arriving from a concept-based query; a high rate would indicate the mechanism surfaces topically related but ultimately irrelevant products.
  - Success Metric Target: PDP Bounce Rate for concept-based/long-tail query sessions is at or below the site-wide baseline bounce rate, measured over the first 8 weeks post-launch, via analytics event data segmented by query type.
  - Kill Threshold: PDP Bounce Rate for this segment meaningfully exceeds the site-wide baseline after 8 weeks.

- [User Outcome] Relevance: Measures the Target User's actual judgment of whether the returned results address the concept they searched for — the most direct measure of whether the shopper's JTBD (finding a matching product) was completed, independent of purchase.
  - Success Metric Target: human- or model-graded relevance score for concept-based/long-tail query results meets a defined quality bar, measured via periodic relevance evaluation against a pre-launch baseline, re-measured at 8 weeks post-launch. Flag: requires a defined relevance-grading process/rubric if one doesn't already exist.
  - Kill Threshold: relevance score shows no improvement over the pre-launch baseline at 8 weeks.

- [Guardrail Outcome] Latency: Protects the non-negotiable Solution Constraint that this solution must not add significant latency to search response time.
  - Success Metric Target: p95 search response latency stays within a defined margin of the pre-launch baseline, measured continuously post-launch via site performance monitoring. Flag: acceptable margin and current p95 baseline need to be defined before launch.
  - Kill Threshold: p95 latency increases by a user-perceptible margin over baseline (commonly cited: >100ms).

- [Guardrail Outcome] Model Coverage: Protects against the mechanism silently degrading to only a subset of the catalog or query space over time.
  - Success Metric Target: the mechanism's coverage (e.g., % of catalog enriched, or % of query volume within supported scope) stays at or above a defined floor, measured monthly via internal model/catalog coverage reporting. Flag: requires defining "coverage" operationally for the chosen solution before this can be tracked.
  - Kill Threshold: coverage falls below the defined floor for two consecutive measurement periods.

- [Guardrail Outcome] Site Performance: Protects against the solution degrading broader site health beyond just search-specific latency.
  - Success Metric Target: site performance metrics (e.g., page load time, error rate) on search-result and product pages hold at or above pre-launch baseline, measured continuously post-launch via site performance monitoring.
  - Kill Threshold: any measurable, sustained regression in site performance metrics attributable to the new solution.

## Excluded Metrics (Vanity):
- No vanity metrics were excluded from the kept set above.
---
