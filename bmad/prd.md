# Student Ambassador Platform - Product Requirements Document

## 1. Product Overview

### 1.1 Purpose
Autonomous AI advocate for students navigating college applications and financial aid. Makes money finding free money, nothing on debt.

### 1.2 Target Users

| Segment | Age | Primary Needs |
|---------|-----|---------------|
| Junior | 16-17 | Test prep, school research, activity optimization |
| Senior | 17-18 | Applications, essays, financial aid, decisions |
| Transition | 18 | Account independence, aid optimization |
| College | 18-22 | Ongoing scholarships, debt tracking |
| Graduate | 22-27 | Loan repayment, "getting started" grants |

### 1.3 Core Value Proposition
- **For students:** Free advocate that knows them deeply, acts autonomously, learns collectively
- **For the system:** Commission on scholarships (5%), nothing on loans (0%)

---

## 2. Functional Requirements

### 2.1 Personal Ambassador Agent

**FR-001:** System shall maintain one ambassador agent per student with persistent memory across all interactions.

**FR-002:** Ambassador shall store all PII on-device only (Sparksee Mobile), encrypted with user-held keys.

**FR-003:** Ambassador shall proactively monitor and alert on:
- Deadlines within 7 days (notification)
- Deadlines within 24 hours (urgent alert)
- New scholarship matches (queued for conversation)
- No interaction in 5 days (gentle check-in)
- No interaction in 14 days (concern check-in)
- Application status changes (immediate notification)

**FR-004:** Ambassador shall support interaction via:
- Voice (Hume.ai EVI)
- SMS/RCS
- Web chat
- Email (formal communications)

### 2.2 Specialist Agents

**FR-005:** System shall provide specialist agents accessible via A2A protocol:

| Agent | Function |
|-------|----------|
| Scholarship Scout | Crawl databases, match to profiles, push to ambassadors |
| Appeal Strategist | Analyze success patterns, coach on tactics |
| Deadline Sentinel | Master calendar, coordinate reminders |
| Document Analyst | On-device doc processing, extract data, validate |

**FR-006:** All specialist requests shall be anonymized - specialists never see PII.

### 2.3 Graph Architecture

**FR-007:** Personal Graph (Sparksee Mobile, on-device):
- Student profile
- Documents (encrypted)
- Test scores
- Activities
- Essays
- Recommendations
- Financial data

**FR-008:** Ambassador Graph (FalkorDB, server-side):
- Anonymized profile
- Interaction logs
- Negotiation history
- Application status

**FR-009:** Commons Graph (FalkorDB, federated):
- School behavior models
- Strategy effectiveness
- Outcome patterns
- Scholarship intelligence

**FR-010:** Graphiti temporal layer shall track:
- Fact validity periods (valid_from, valid_to)
- Episodic memory (conversation history)
- Trend detection
- Point-in-time queries

### 2.4 Voice Interface

**FR-011:** Voice interface shall detect emotions and adapt:

| Emotion | Pace | Tone | Action |
|---------|------|------|--------|
| Anxiety | Slower | Reassuring | Break down steps |
| Frustration | Measured | Validating | Acknowledge then solve |
| Excitement | Match | Enthusiastic | Channel to action |
| Confusion | Slower | Patient | Clarify with examples |
| Defeat | Gentle | Encouraging | Show options and wins |
| Shame | Soft | Normalizing | Share commons data |

**FR-012:** Voice use cases:
- Essay brainstorming
- Document review (accessibility)
- Crisis support
- Negotiation practice
- Late-night anxiety support

### 2.5 Generated UX

**FR-013:** System shall have no static UI. All visuals generated on-demand via Nanobanana:
- Win cards (shareable)
- Debt comparison infographics
- School comparison charts
- Scholarship match cards
- Aid breakdown visualizations

**FR-014:** Generated artifacts shall be delivered via RCS when visual, SMS when text-only.

### 2.6 Scholarship Discovery

**FR-015:** System shall search and match scholarships with:
- Profile matching against criteria
- Deadline tracking
- Legitimacy verification
- Success rate estimation (from commons)

**FR-016:** System shall calculate expected value:
```
Expected Value = Match Score × Award Amount × Historical Success Rate
```

### 2.7 Document Processing

**FR-017:** System shall parse and extract from:
- Award letters
- FAFSA SAR
- Transcripts
- Tax documents
- Scholarship requirements

**FR-018:** All document processing shall occur on-device (Sparksee Mobile).

### 2.8 Aid Appeals

**FR-019:** System shall draft appeal letters using:
- Commons success patterns for target school
- Competing offer leverage
- Student-specific circumstances
- Effective argument templates

**FR-020:** System shall provide negotiation practice via voice roleplay.

### 2.9 Revenue Collection

**FR-021:** Commission structure:

| Source | Rate | Cap |
|--------|------|-----|
| Scholarships (<$5k) | 5% | $500 |
| Scholarships (>$5k) | 3% | $500 |
| Third-party grants | 2% | $1,000 |
| Institutional grants | 2% | $1,000 |
| Federal grants | 1% | $500 |
| State grants | 1.5% | $500 |
| Appeal wins | 10% | $500 |
| Loans | 0% | $0 |

**FR-022:** Collection flow:
1. Disbursement detected via Greenlight
2. Source classified (grant/loan/scholarship/family)
3. Fee calculated on eligible funds
4. Student sees transparent breakdown
5. Pre-authorized deduction executes
6. 7-day dispute window

---

## 3. Non-Functional Requirements

### 3.1 Performance

**NFR-001:** Voice latency <500ms for emotion detection response adaptation.

**NFR-002:** Scholarship search results <2 seconds.

**NFR-003:** On-device graph queries <100ms.

### 3.2 Security

**NFR-004:** All PII encrypted at rest (AES-256) on device.

**NFR-005:** User holds sole encryption keys.

**NFR-006:** No PII transmitted to server without explicit consent.

**NFR-007:** Anonymization shall be irreversible for commons contributions.

### 3.3 Privacy

**NFR-008:** Data deletion on request within 24 hours.

**NFR-009:** Export all personal data in portable format.

**NFR-010:** Clear consent UI for each data sharing action.

### 3.4 Reliability

**NFR-011:** Ambassador available 24/7 (voice/SMS).

**NFR-012:** Graceful degradation if Hume unavailable (text fallback).

**NFR-013:** Offline capability for personal graph queries.

### 3.5 Scalability

**NFR-014:** Commons graph shall support 1M+ students.

**NFR-015:** A2A federation shall support 100K+ concurrent ambassadors.

---

## 4. User Stories

### Epic 1: Onboarding

**US-001:** As a new student, I want to connect my Greenlight account so my ambassador knows when aid arrives.

**US-002:** As a new student, I want to tell my ambassador about my college plans via voice so I don't have to fill out forms.

**US-003:** As a new student, I want to upload my transcript so my ambassador knows my academic profile.

### Epic 2: Scholarship Discovery

**US-004:** As a student, I want my ambassador to find scholarships I qualify for so I don't have to search manually.

**US-005:** As a student, I want to see why I match a scholarship so I can decide if it's worth applying.

**US-006:** As a student, I want deadline reminders so I never miss an opportunity.

**US-007:** As a student, I want to know my chances of winning based on similar students so I can prioritize.

### Epic 3: Application Support

**US-008:** As a student, I want to brainstorm my essay via voice so I can think out loud.

**US-009:** As a student, I want my ambassador to track my document status so I know what's missing.

**US-010:** As a student, I want help requesting recommendations so I send professional emails.

### Epic 4: Aid Optimization

**US-011:** As a student, I want my ambassador to analyze my aid offer so I know if it's fair.

**US-012:** As a student, I want help drafting an appeal so I can negotiate more aid.

**US-013:** As a student, I want to practice my negotiation via voice roleplay so I'm confident.

### Epic 5: Debt Prevention

**US-014:** As a student, I want a warning before accepting loans so I consider alternatives first.

**US-015:** As a student, I want to see the true cost of a loan (with interest) so I understand the burden.

**US-016:** As a student, I want scholarships suggested when I'm about to borrow so I have options.

### Epic 6: Emotional Support

**US-017:** As a student, I want my ambassador to recognize when I'm stressed so it adapts its tone.

**US-018:** As a student, I want to vent about a rejection so I feel heard before problem-solving.

**US-019:** As a student, I want late-night support so I'm not alone with anxiety.

### Epic 7: Sharing & Virality

**US-020:** As a student, I want to share my scholarship win so my friends know about opportunities.

**US-021:** As a student, I want to show my debt reduction so others see the value.

**US-022:** As a student, I want referral rewards so I benefit from helping friends.

---

## 5. Acceptance Criteria

### AC-001: Scholarship Match
- GIVEN a student profile with GPA, test scores, activities
- WHEN the system searches for scholarships
- THEN it returns matches with score >50% and reasons for match

### AC-002: Emotion Detection
- GIVEN a voice session with stressed prosody
- WHEN Hume detects anxiety >0.7
- THEN ambassador slows pace and uses reassuring tone within 500ms

### AC-003: Appeal Draft
- GIVEN a student with competing offers
- WHEN requesting an appeal letter
- THEN system generates draft using commons success patterns for that school

### AC-004: Loan Intervention
- GIVEN a student about to accept a loan
- WHEN loan >$1,000
- THEN system alerts with alternative scholarships and true cost calculation

### AC-005: Commission Calculation
- GIVEN a $5,000 scholarship disbursement
- WHEN classified as third-party (<$5k)
- THEN fee calculated as $250 (5%) capped at $500

---

## 6. Dependencies

| Dependency | Owner | Status |
|------------|-------|--------|
| Sparksee Mobile SDK | Sparsity Technologies | Need license |
| FalkorDB | Open source | Available |
| Graphiti | Zep AI | Available |
| Hume.ai EVI | Hume | Available |
| Nanobanana | Nanobanana | Available |
| Greenlight API | Greenlight | Need partnership |
| Agent Zero | Open source | Available |

---

## 7. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Greenlight partnership fails | Medium | High | Design bank-agnostic, pursue alternatives |
| Sparksee licensing cost | Medium | Medium | Fallback to SQLite with manual graph layer |
| Schools game commons | Medium | Medium | Verification via disbursement, anomaly detection |
| Low voice adoption | Medium | Low | Text-first with voice as enhancement |
| Commission model legal challenge | Low | High | Legal review, structure as service fee |
