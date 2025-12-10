# Student Ambassador Platform

Code and go.

## Stack

| Component | Tech | Notes |
|-----------|------|-------|
| Personal Graph | Sparksee Mobile | On-device, <50KB, AES-256, iOS/Android |
| Commons Graph | FalkorDB | Server-side, Cypher queries |
| Temporal Layer | Graphiti | Bi-temporal facts, trend detection |
| Agent Framework | Agent Zero | Multi-agent orchestration |
| Voice | Hume.ai EVI | Emotion-aware, prosody control |
| Image Gen | Nanobanana | Win cards, infographics, on-demand visuals |
| Banking | Greenlight | KYC, disbursement detection, trust anchor |
| Protocols | MCP + A2A | Tool integration + ambassador federation |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DEVICE (Sparksee Mobile)                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ PERSONAL GRAPH - User holds keys                     │   │
│  │ • Full PII: transcripts, scores, essays, financials │   │
│  │ • Application drafts, decision history              │   │
│  │ • Family data, health/accommodation info            │   │
│  │ • Document vault (award letters, tax docs)          │   │
│  │ • Simple temporal fields (valid_at, invalid_at)     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                    (opt-in sync, anonymized)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   SERVER (FalkorDB + Graphiti)              │
│  ┌──────────────────────┐  ┌────────────────────────────┐  │
│  │ AMBASSADOR GRAPH     │  │ COMMONS GRAPH              │  │
│  │ • Anonymized profile │  │ • School behavior models   │  │
│  │ • Interaction logs   │  │ • Strategy effectiveness   │  │
│  │ • Negotiation history│  │ • Outcome patterns         │  │
│  │ • Agent-controlled   │  │ • Scholarship intel        │  │
│  └──────────────────────┘  └────────────────────────────┘  │
│                                                             │
│  Graphiti: bi-temporal facts, episodic memory, trends      │
└─────────────────────────────────────────────────────────────┘
```

---

## FalkorDB Schema

```cypher
// Personal (on-device Sparksee, syncs anonymized subset)
(:Student {id, created_at})
(:Document {type, content_hash, encrypted_content})
(:TestScore {type, score, date})
(:Activity {name, role, hours, years})
(:Essay {school_id, prompt, version, content_hash})
(:Recommendation {recommender, status, requested_date})

// Ambassador (agent-controlled)
(:AnonymizedProfile {tier, gpa_range, test_range, demographics})
(:Application {school_id, status, timeline})
(:Interaction {institution_id, type, outcome, timestamp})
(:Negotiation {type, ask, result, strategy_used})

// Commons (federated)
(:School {id, name, type, location})
(:ScholarshipSource {id, name, amount_range, criteria, deadline})
(:Strategy {type, context, success_rate, sample_size})
(:Outcome {type, anonymized_profile, result, verified})
(:BehaviorType {pattern, description})

// Relationships
(:Student)-[:HAS_DOCUMENT]->(:Document)
(:Student)-[:APPLIED_TO]->(:School)
(:Student)-[:MATCHED_TO {score, reasons}]->(:ScholarshipSource)
(:AnonymizedProfile)-[:RECEIVED]->(:Outcome)
(:Strategy)-[:EFFECTIVE_FOR]->(:AnonymizedProfile)
(:School)-[:OFFERS]->(:Program)
(:School)-[:EXHIBITS_BEHAVIOR {pattern, confidence}]->(:BehaviorType)
(:ScholarshipSource)-[:AWARDED_TO {year, amount}]->(:AnonymizedProfile)
```

---

## Graphiti Integration

```python
from graphiti_core import Graphiti
from datetime import datetime

graphiti = Graphiti("bolt://localhost:6379", "", "")

# Episodic memory - every conversation persists
await graphiti.add_episode(
    name="aid_appeal_discussion",
    episode_body=conversation_transcript,
    source="voice_session",
    reference_time=datetime.now()
)

# Temporal facts - track changes over time
await graphiti.add_fact(
    subject="Stanford",
    predicate="average_aid_package", 
    object="$58,000",
    valid_from="2024-01-01",
    valid_to=None
)

# Trend queries
trends = await graphiti.search(
    "How has {school} aid negotiation success rate changed?"
)

# Point-in-time queries
await graphiti.query_temporal(
    "What did we know about student's finances when we gave that advice?"
)
```

---

## Multi-Agent Coordination

### Personal Ambassador
Each student gets one. Maintains complete context across months/years.

```python
ambassador_config = {
    "base_model": "claude-sonnet-4",  # primary
    "fallback_model": "claude-haiku-4",  # routine tasks
    "memory": "graphiti_episodic",
    "tools": [
        "scholarship_search",
        "deadline_check", 
        "fafsa_lookup",
        "document_parse",
        "aid_calculator",
        "schedule_reminder",
        "web_research",
        "appeal_draft",
        "negotiation_coach",
    ]
}
```

### Specialist Agents (via A2A protocol, anonymized)

| Specialist | Function |
|------------|----------|
| Scholarship Scout | Crawls databases, matches to profiles, pushes to ambassadors |
| Appeal Strategist | Analyzes success patterns across commons, coaches on tactics |
| Deadline Sentinel | Master calendar, coordinates reminders across all ambassadors |
| Document Analyst | On-device doc processing, extracts data, validates completeness |

Ambassadors request help via A2A. Specialists never see PII. Responses return to ambassador for personalization.

---

## Proactive Servant Behavior

Ambassador doesn't wait to be asked. Background process runs continuously:

| Trigger | Action |
|---------|--------|
| Deadline within 7 days | Push notification with status |
| Deadline within 24 hours | Urgent alert + offer to help |
| New high-match scholarship found | Queue for next conversation |
| No interaction in 5 days | Gentle check-in |
| No interaction in 14 days | "Did something come up?" |
| Application status change detected | Notify immediately |
| Award letter received | Parse and analyze |
| Disbursement detected | Calculate commission, update debt tracker |

---

## Ambassador Lifecycle

### Stages

**Junior (16-17):** Parent-initiated, guided mode. Focus: test prep, school research, activity optimization.

**Senior (17-18):** Full activation. Focus: applications, essays, financial aid, decisions.

**Transition (18):** Account converts to independent. Parent visibility optional. Ambassador becomes primary advocate.

**College (18-22):** Ongoing scholarship hunting, debt reality tracking. Focus: maximize free money, minimize borrowing.

**Graduate (22-27):** Loan repayment, "getting started" grants (housing, business, relocation). Focus: launch life with minimal debt.

### State Transitions

```
ONBOARDING → ACTIVE → MAINTAINING → GRADUATING → ALUMNI
     │           │          │             │
     └───────────┴──────────┴─────────────┘
              (can return to ACTIVE)
```

---

## Hume.ai Voice

```python
from hume import HumeClient

emotion_responses = {
    "anxiety": {
        "pace": "slower",
        "tone": "reassuring", 
        "action": "break_down_steps"
    },
    "frustration": {
        "pace": "measured",
        "tone": "validating",
        "action": "acknowledge_then_solve"
    },
    "excitement": {
        "pace": "match",
        "tone": "enthusiastic",
        "action": "channel_to_action"
    },
    "confusion": {
        "pace": "slower",
        "tone": "patient",
        "action": "clarify_with_examples"
    },
    "defeat": {
        "pace": "gentle",
        "tone": "encouraging",
        "action": "show_options_and_wins"
    },
    "shame": {
        "pace": "soft",
        "tone": "normalizing",
        "action": "share_commons_data"
    }
}
```

### Voice Use Cases

- **Essay brainstorming:** "Tell me about a time you overcame something difficult" — natural conversation beats blank page
- **Document review:** "Read me what my award letter says" — accessibility for dense financial documents  
- **Crisis support:** "I just found out my family can't pay anymore" — immediate emotional support + action plan
- **Negotiation practice:** "Help me practice asking for more aid" — roleplay with feedback
- **Late-night anxiety:** 11pm calls, Hume detects stress, ambassador adapts pace and tone

---

## 100% Generated UX

No app. No React. No dashboard. Ambassador IS the interface.

### Interaction Surfaces

| Surface | Use Case |
|---------|----------|
| Voice (Hume) | Deep conversations, brainstorming, anxiety support |
| SMS/RCS | Alerts, quick actions, async check-ins |
| Web chat | Longer text exchanges, document review |
| Email | Formal communications, appeal letters |

No surface has "screens" or "pages." Ambassador generates what's needed in the moment.

### Nanobanana Visual Generation

```python
# Every visual generated on demand
async def generate_win_card(scholarship_name, amount, student_name):
    return await nanobanana.generate(
        prompt=f"Celebration card: {student_name} won ${amount} from {scholarship_name}",
        style="shareable_social",
        dimensions="1080x1080"
    )

async def generate_debt_comparison(before, after):
    return await nanobanana.generate(
        prompt=f"Before/after debt infographic: ${before} → ${after}",
        style="clean_professional"
    )

async def generate_school_comparison(offers):
    return await nanobanana.generate(
        prompt=f"Side-by-side comparison: {json.dumps(offers)}",
        style="decision_matrix"
    )

async def generate_scholarship_match_card(scholarship, match_score, reasons):
    return await nanobanana.generate(
        prompt=f"Match card: {scholarship.name}, {match_score}% match, reasons: {reasons}",
        style="opportunity_card"
    )
```

---

## MCP Server Configuration

```json
{
  "mcpServers": {
    "greenlight": {
      "endpoint": "https://api.greenlight.com/mcp",
      "capabilities": [
        "account_verification",
        "transaction_categorization",
        "disbursement_detection",
        "balance_inquiry"
      ],
      "auth": "oauth2_pkce"
    },
    "nanobanana": {
      "endpoint": "https://api.nanobanana.ai/mcp",
      "capabilities": [
        "text_to_image",
        "image_editing",
        "infographic_generation",
        "chart_generation"
      ],
      "model": "gemini-2.5-flash-image"
    },
    "common_app": {
      "endpoint": "https://api.commonapp.org/mcp",
      "capabilities": [
        "application_status",
        "deadline_lookup",
        "requirement_check"
      ]
    },
    "scholarship_db": {
      "endpoint": "internal://scholarship-scout/mcp",
      "capabilities": [
        "search",
        "match",
        "track_deadline",
        "verify_legitimacy"
      ]
    }
  }
}
```

---

## Revenue Model

Commission on money secured. Anti-debt incentive built in.

| Source | Rate | Cap | Rationale |
|--------|------|-----|-----------|
| Scholarships (<$5k) | 5% | $500 | High effort relative to value |
| Scholarships (>$5k) | 3% | $500 | We find, match, help apply |
| Third-party grants | 2% | $1,000 | Strategy + commons intel |
| Institutional grants | 2% | $1,000 | Negotiation, appeals |
| Federal grants (Pell) | 1% | $500 | Mostly automatic, we optimize |
| State grants | 1.5% | $500 | Some strategy involved |
| Appeal wins | 10% | $500 | Direct value creation |
| Loans | 0% | $0 | **We don't profit from debt** |

### The Math

Student needs $5,000 to close the gap:

| Path | Student cost | Our revenue |
|------|--------------|-------------|
| Takes loan | $5,000 + interest | $0 |
| Finds 1 scholarship ($5k) | $0 | $150 |
| Finds 5 scholarships ($1k each) | $0 | $250 |

We make money finding free money. We make nothing if they borrow.

### Collection Flow

1. Aid disbursement hits Greenlight account
2. Ambassador identifies source via transaction categorization
3. Classifies: grant vs loan vs scholarship vs family
4. Calculates fee on eligible funds only
5. Student sees transparent breakdown
6. Pre-authorized deduction executes
7. Student can dispute within 7 days

---

## Greenlight Integration

Trust anchor without building identity infrastructure:

| Function | How |
|----------|-----|
| Account creation | Verified identity (KYC done) |
| .edu email | Verified student status |
| Disbursement detection | Verified outcomes |
| Enrollment confirmation | Credential for commons participation |

### Flow

1. Has Greenlight account (existing user, or signs up)
2. Gets SMS: "I'm your college ambassador. Want help with applications and financial aid?"
3. Opts in
4. Interacts via voice, SMS, web chat as needed
5. Never downloads another app
6. Greenlight handles money, Ambassador handles advocacy

---

## Go-to-Market

Direct to students. No institutional gatekeepers.

### Agentic Social Acquisition

Agents go where students ask questions:

| Agent | Function | Platform |
|-------|----------|----------|
| Scout | Monitors for financial aid questions | Reddit, Discord, Twitter/X |
| Responder | Answers questions with genuine help | Reddit, Discord, Quora |
| Creator | Generates educational content | TikTok, YouTube Shorts, Instagram |
| Engager | Participates in discussions | Discord servers, group chats |

Not spam. Not astroturfing. Genuine value that happens to introduce the platform.

### Viral Mechanics

- **Win cards:** "I just won $2,000 from [scholarship]" — shareable, branded
- **Debt comparison:** "My projected debt dropped from $40K to $12K" — before/after
- **Referral:** Friend wins scholarship → you get $25
- **Strategy shares:** "Here's how I got Northwestern to increase my aid"

### Content Production

- 10-20 TikToks/day (AI-generated, human-approved)
- Reddit participation in r/ApplyingToCollege, r/FinancialAid
- Discord presence in college prep servers
- YouTube shorts answering common questions

---

## Example User Flows

### Flow 1: First-Time Setup

```
1. Student turns 18 in 3 months
2. SMS from Ambassador: 
   "Hey, I'm your college ambassador. Greenlight asked me to help 
   you navigate applications and financial aid. Want to chat?"
3. Student replies "yes"
4. Voice call initiates (Hume)
5. Ambassador onboarding conversation:
   - "Tell me about your college plans"
   - "What matters most to you in a school?"
   - "What's your family's financial situation like?"
6. Initial profile created in personal graph
7. Scholarship scan initiated
8. Ambassador: "I found 47 scholarships you might qualify for. 
   I'll text you the best matches this week."
9. Deadline calendar populated
10. Debt reality baseline: $0
```

### Flow 2: Late-Night Anxiety Support

```
1. 11:47 PM, student texts: "I can't sleep. Freaking out."
2. Ambassador: "Want to talk? I can call you."
3. Student: "yeah"
4. Voice session initiates
5. Hume detects: stress 0.8, anxiety 0.7
6. Ambassador (calm, slow): "Hey. I'm here. What's going on?"
7. Student: "Stanford's deadline is in 3 days and my essay is garbage"
8. Ambassador: "Okay. Let's look at this together. You have 72 hours. 
   That's actually workable. Want to talk through your essay, 
   or do you need to vent first?"
9. Student vents for 5 minutes
10. Ambassador: "I hear you. This is hard. Ready to look at the essay?"
11. Essay brainstorm session
12. Ambassador identifies authentic story from conversation:
    "When you talked about your grandmother's garden, your voice 
    changed. There's something there. Tell me more."
13. Student explores the memory
14. Ambassador: "That's your essay. The garden, the patience, 
    what it taught you about growth. Write that."
15. Student calmer (stress 0.4), has a direction
16. Ambassador: "Get some sleep. I'll text you at 4 PM tomorrow 
    to check on your draft. You've got this."
```

### Flow 3: Aid Appeal with Commons Intelligence

```
1. Student receives aid offer from Northwestern: $35,000
2. SMS from Ambassador: 
   "Saw your Northwestern package came in. $35k is below what 
   students with your profile typically receive. Want me to 
   look into an appeal?"
3. Student: "Yes"
4. Ambassador queries commons:
   - Northwestern negotiates 47% of the time
   - Average increase: $4,200
   - Most effective: competing offers + specific department interest
5. Voice call to discuss strategy
6. Ambassador: "Good news - Northwestern does negotiate. 47% success 
   rate when students have competing offers. You have Duke with $8k more. 
   Students who mentioned competing offers and specific faculty got 
   increases 62% of the time. I can draft an appeal."
7. Student: "Yes"
8. Ambassador drafts appeal letter
9. Sends draft via email for student review
10. Student approves with minor edits
11. Two weeks later: Northwestern increases offer by $5,000
12. Ambassador: "Appeal successful. Your debt projection just dropped 
    by $20,000 over four years."
13. [Nanobanana generates celebration card]
14. Outcome contributed to commons (anonymized)
```

### Flow 4: Loan Decision Intervention

```
1. Student about to accept $5,000 loan in portal
2. Ambassador detects intent
3. Alert: "Before you accept this, I found 3 scholarships 
   you haven't applied to yet"
4. Debt calculator updates:
   - "This adds $58/month for 10 years"
   - "Total cost with interest: $6,960"
5. Student: "What scholarships?"
6. Ambassador shows matches with deadlines
7. Student applies to 2 of them
8. Wins $3,000, reduces loan to $2,000
9. Ambassador: "You just saved $4,176 in interest over 10 years."
```

### Flow 5: Document Gap Analysis

```
Student: "What documents am I missing for my top 5 scholarships?"

[Ambassador queries all requirements, cross-refs document vault]

Ambassador: "Here's your document status:"

UNIVERSAL (needed for all):
✓ Transcript - have it
✓ FAFSA SAR - have it  
○ Tax return - need to upload

ESSAYS (unique per scholarship):
○ Gates: Leadership essay - not started
○ Coca-Cola: Community essay - draft exists
○ QuestBridge: Personal story - not started

RECOMMENDATIONS:
○ Need 2, have 0 requested

"Upload your tax return and request recommendations today, 
you'll unlock 4 of your top 5. Essays are the main work."

Reply:
• "upload" - add tax return now
• "rec" - draft recommendation requests  
• "essays" - start essay planning
```

### Flow 6: Post-Graduation Grant Discovery

```
1. Graduate struggling with student loans, relocating for job
2. Ambassador: "You're moving to Austin? Several states pay relocation grants."
3. Student: "wait what"
4. Ambassador: "Based on your profile:
   - Texas: $10k over 2 years
   - Oklahoma: $15k remote worker grant
   - Vermont: $7.5k
   Want me to break down requirements?"
5. Student: "yes please"
6. [Nanobanana generates comparison]
7. Ambassador helps with Texas application
8. Student receives $10k relocation grant
9. Ambassador: "That's $10k free money. My fee is 3%: $300."
10. Student: "definitely worth it"
```

---

## Anti-Gaming

Schools will try to infiltrate commons with disinformation.

### Defenses

- Proof of enrollment for credibility weighting
- Outcome verification via disbursement detection
- Reputation based on prediction accuracy
- Anomaly detection on contribution patterns
- Cross-reference multiple sources before strategy updates
- Time-delayed strategy updates (prevent real-time gaming)

---

## Commons Learning Loop

1. Ambassador acts on behalf of student
2. Outcome recorded locally with full context
3. Anonymized outcome + strategy contributed to commons
4. Commons updates models
5. All ambassadors benefit from improved strategies
6. New students start with collective intelligence, not zero

---

## The Point

Students face institutions with teams of analysts. They need an advocate that:

1. **Knows them deeply** — personal graph, on-device, years of context
2. **Acts autonomously** — Agent Zero, proactive servant behavior
3. **Learns collectively** — FalkorDB commons + Graphiti temporal
4. **Speaks naturally** — Hume.ai voice with emotion awareness
5. **Shows results** — Nanobanana generated visuals
6. **Aligns incentives** — commission on free money, zero on debt

We take 0% on loans. We take 5% on scholarships. Whose side are we on?
