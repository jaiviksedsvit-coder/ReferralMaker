# Product Requirements Document (PRD): ReferralCraft AI (ReferralMaker 2.0)

**Product Name:** ReferralCraft AI (v2.0)  
**Status:** In Development / Product Redesign  
**Owner:** Jaivik Chauhan  
**Last Updated:** October 2026  

---

## 1. Executive Summary & Vision

### Vision Statement
*To empower every job seeker—regardless of background, network size, or writing proficiency—to secure high-conversion employee referrals through hyper-personalized, etiquette-checked, multi-channel AI outreach.*

### Core Value Proposition
Job applicants who secure employee referrals are **4x more likely to be interviewed** and **8x more likely to be hired**, yet over **85% of cold outreach messages fail** because they are either:
1. Generic copy-pasted templates ("Please refer me to this job ID..."),
2. Overly long essays that busy professionals ignore,
3. Desperate/transactional in tone ("I am begging for a referral"), or
4. Violating channel constraints (e.g., exceeding LinkedIn's strict 300-character connection request limit).

**ReferralCraft AI 2.0** transforms raw candidate resumes, target job descriptions, and referral recipient profiles into an omni-channel referral campaign suite:
- Strict **LinkedIn Connection Requests (<300 characters)**,
- High-converting **LinkedIn InMails & DMs**,
- Professional **Cold & Warm Emails** with curated subject lines,
- Automated **Follow-Up Nudges**, and
- An **AI "Cringe & Etiquette Audit"** that grades tone, desperation, and value alignment.

---

## 2. Problem Statement & Market Landscape

### The Asymmetry in Job Referrals
1. **The Seeker's Dilemma**:
   - Job boards are overcrowded (hundreds of applicants within hours).
   - Writing personalized messages to 20–30 potential referrers is exhausting and time-consuming.
   - Most seekers don't know how to frame their ask without sounding transactional or awkward.
2. **The Referrer's Dilemma**:
   - Busy professionals receive dozens of generic LinkedIn messages weekly.
   - They risk their professional reputation if they refer low-quality or pushy candidates.
   - If an outreach doesn't clearly demonstrate *why* the candidate is qualified within 5 seconds, it gets archived or ignored.
3. **The Channel Constraint Gap**:
   - LinkedIn allows only 300 characters for connection notes for non-premium users. Existing AI tools generate 150-word walls of text that cannot physically be sent as connection invites.

---

## 3. User Personas & Pain-Point Solution Matrix

### Persona 1: "The New Grad / Career Starter" (Aarav, 22)
- **Profile**: Final-year CS / Business student; applying to 50+ roles; zero warm network at top tech companies.
- **Pain Points**:
  - Feels intimidated reaching out to senior engineers and managers.
  - Doesn't know what common ground to use except "we went to the same college".
  - Messages sound overly apologetic or copy-pasted.
- **Tailored Solution**:
  - *Alumni Hook Generator*: Highlights shared alma mater, faculty, or club.
  - *Confidence Calibrator*: Rephrases apologetic language into confident, curiosity-driven inquiries.
  - *Strict <300 char Connection Note*: Fits directly into free LinkedIn connection requests.

### Persona 2: "The Mid-Career Transitioner" (Elena, 31)
- **Profile**: Product Manager transitioning from FinTech to HealthTech or AI; 7 years experience.
- **Pain Points**:
  - Needs to bridge domain gaps and explain transferable skills concisely.
  - Reaching out to 2nd-degree connections or former colleagues without seeming purely transactional.
- **Tailored Solution**:
  - *Transferable Skills Synthesizer*: Extracts top 3 overlapping strengths between past resume and target JD.
  - *Warm Outreach Mode*: Nuanced scripts for ex-colleagues, past clients, or mutual friends.

### Persona 3: "The Busy Executive / Senior Leader" (Marcus, 42)
- **Profile**: Senior Director / Staff Engineer seeking discrete, high-level executive referrals.
- **Pain Points**:
  - Reaching out directly to VPs, CTOs, and Head of Talent.
  - Requires authoritative, peer-to-peer tone that respects executive time.
- **Tailored Solution**:
  - *Executive Peer Mode*: Focuses on business impact, strategic alignment, and frictionless exploratory chats.

### Persona 4: "The International / Visa Candidate" (Priya, 26)
- **Profile**: International graduate needing sponsorship; anxious about cultural etiquette in outreach.
- **Pain Points**:
  - Unsure how or when to mention sponsorship without triggering immediate rejection.
  - Overly formal or archaic phrasing ("Respected Sir/Madam").
- **Tailored Solution**:
  - *Modern Tech Etiquette Filter*: Replaces stiff honorifics with contemporary, friendly conversational norms.

---

## 4. Product Solutions & Core Features

| Feature | Description | Target Persona | Priority (MoSCoW) |
| :--- | :--- | :--- | :--- |
| **Smart Resume & JD Parser** | Upload PDF/Docx or paste text; AI extracts core skills, impact metrics, and overlaps. | All | **Must Have** |
| **Omni-Channel Suite** | Generates: (1) Connection Note (<300 char), (2) InMail/DM, (3) Email w/ Subject, (4) Follow-up. | All | **Must Have** |
| **Relationship Calibrator** | Modes: Cold Stranger, College Alumni, Ex-Colleague, Mutual Connection, Recruiter. | All | **Must Have** |
| **AI Cringe & Etiquette Audit** | Rates draft on: Desperation Index, Value-to-Ask Ratio, Clarity, and Likelihood of Response. | Persona 1, 4 | **Must Have** |
| **Interactive Rewrite Tools** | 1-Click modifiers: "Make Punchier", "Warmer Tone", "Under 280 chars", "More Senior". | Persona 2, 3 | **Should Have** |
| **1-Click Copy & Export** | Quick copy with visual feedback; export full campaign to Markdown/Text. | All | **Must Have** |
| **BYOK (Bring Your Own Key) & Privacy** | Client-side API key handling; no resume data persisted to external servers. | All | **Must Have** |
| **Referral Tracker / CRM Lite** | Track contacted referrers, response dates, and statuses. | Persona 1, 2 | **Could Have (v2.1)** |
| **Browser Extension** | One-click extract from open LinkedIn tab. | Persona 1, 2 | **Won't Have (v3.0)** |

---

## 5. Feature Prioritization Framework (RICE Scoring)

| Feature | Reach (1-10) | Impact (1-3) | Confidence (%) | Effort (Person-days) | RICE Score | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Multi-Channel Generation (<300 char, DM, Email)** | 10 | 3.0 | 95% | 2 | **142.5** | **P0 (Phase 1)** |
| **Resume PDF Parsing & JD Extraction** | 9 | 2.5 | 90% | 2 | **101.2** | **P0 (Phase 1)** |
| **AI Cringe & Etiquette Scorecard** | 8 | 2.5 | 85% | 1.5 | **113.3** | **P0 (Phase 1)** |
| **Tone & Relationship Selectors** | 10 | 2.0 | 95% | 1 | **190.0** | **P0 (Phase 1)** |
| **Interactive Tone Rewriter Chips** | 7 | 1.5 | 85% | 1.5 | **59.5** | **P1 (Phase 2)** |
| **Campaign Export (MD/Text)** | 8 | 1.0 | 95% | 0.5 | **152.0** | **P0 (Phase 1)** |
| **Mini Outreach Tracker (Local CRM)** | 6 | 1.5 | 80% | 3 | **24.0** | **P2 (Phase 3)** |

---

## 6. Key Performance Indicators (KPIs)

### 6.1 North Star Metric
- **Referral Engagement Rate (RER)**: % of outreach messages sent that receive a positive reply or referral submission (Target: >35%, compared to industry baseline of 8–12%).

### 6.2 Product Health & Activation Metrics
1. **Activation Rate**: % of new visitors who generate their first referral suite within 3 minutes of landing (Target: >75%).
2. **Copy / Export Rate**: % of generated messages copied to clipboard or downloaded (Target: >85%).
3. **Character Compliance Rate**: % of LinkedIn connection notes strictly meeting the ≤300 character constraint (Target: 100%).
4. **Cringe Reduction Score**: Average improvement in Etiquette/Desperation score after AI polishing (Target: ≥4.5/5.0).
5. **Generation Latency**: Time to generate full multi-channel suite with Gemini 2.5 Flash (Target: < 4 seconds).

---

## 7. Data Privacy & Ethical Guidelines
- **Zero Data Rentention**: Uploaded resumes and contact notes are processed transiently in-memory and never stored on third-party servers.
- **Anti-Spam Ethos**: System actively blocks robotic, spammy mass-pitch language; every prompt forces authentic, contextual alignment.
- **Transparency**: Clear disclosures that AI drafts are starting points that users should review before sending.
