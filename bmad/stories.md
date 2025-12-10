# Student Ambassador Platform - Development Stories

## Epic 1: Core Infrastructure

### Story 1.1: FalkorDB Setup
**Description:** Set up FalkorDB instance with commons graph schema.

**Tasks:**
- [ ] Docker compose for FalkorDB
- [ ] Create commons graph schema (cypher)
- [ ] Seed with sample school data
- [ ] Seed with sample scholarship sources
- [ ] Verify queries work

**Acceptance Criteria:**
- FalkorDB running on localhost:6379
- Can create/query School nodes
- Can create/query ScholarshipSource nodes
- Can create relationships

**Dependencies:** None

---

### Story 1.2: Graphiti Integration
**Description:** Connect Graphiti to FalkorDB for temporal knowledge.

**Tasks:**
- [ ] Install graphiti-core[falkordb]
- [ ] Configure Graphiti with FalkorDB backend
- [ ] Create episode storage
- [ ] Create temporal fact storage
- [ ] Test bi-temporal queries

**Acceptance Criteria:**
- Can add episodes (conversations)
- Can add temporal facts
- Can query "what did we know at time X"
- Can detect fact invalidation

**Dependencies:** Story 1.1

---

### Story 1.3: FastAPI Scaffold
**Description:** Set up FastAPI with existing models from reference implementation.

**Tasks:**
- [ ] Copy models from student_ambassador_api
- [ ] Replace in-memory storage with FalkorDB
- [ ] Add Graphiti memory endpoints
- [ ] Add async support
- [ ] Add health check endpoint

**Acceptance Criteria:**
- API running on localhost:8000
- /health returns 200
- /students CRUD works with FalkorDB
- /docs shows OpenAPI spec

**Dependencies:** Story 1.1, Story 1.2

---

## Epic 2: Ambassador Agent

### Story 2.1: Agent Zero Base Setup
**Description:** Configure Agent Zero as ambassador agent framework.

**Tasks:**
- [ ] Install Agent Zero
- [ ] Create ambassador agent config
- [ ] Configure Claude Sonnet 4 as primary model
- [ ] Configure Claude Haiku 4 as fallback
- [ ] Connect to Graphiti for memory

**Acceptance Criteria:**
- Agent can receive message and respond
- Agent has access to conversation history via Graphiti
- Agent can delegate to sub-agents

**Dependencies:** Story 1.2

---

### Story 2.2: Ambassador Tools
**Description:** Implement core ambassador tools.

**Tasks:**
- [ ] scholarship_search tool
- [ ] deadline_check tool
- [ ] aid_calculator tool
- [ ] schedule_reminder tool
- [ ] web_research tool

**Acceptance Criteria:**
- scholarship_search returns matches from FalkorDB
- deadline_check returns upcoming deadlines
- aid_calculator computes total cost of attendance
- schedule_reminder creates scheduled messages
- web_research can fetch scholarship info

**Dependencies:** Story 2.1

---

### Story 2.3: Proactive Triggers
**Description:** Implement background monitoring and proactive outreach.

**Tasks:**
- [ ] Deadline scanner (7 day, 24 hour triggers)
- [ ] Scholarship match scanner
- [ ] Engagement tracker (5 day, 14 day inactivity)
- [ ] Notification queue
- [ ] Trigger → action mapping

**Acceptance Criteria:**
- System detects deadline within 7 days, queues reminder
- System detects new scholarship match, queues conversation
- System detects 5 days inactive, queues check-in

**Dependencies:** Story 2.2

---

## Epic 3: Specialist Agents

### Story 3.1: Scholarship Scout Agent
**Description:** Background agent that crawls and matches scholarships.

**Tasks:**
- [ ] Create Scout agent config
- [ ] Implement scholarship DB crawler
- [ ] Implement profile matcher
- [ ] Implement legitimacy checker
- [ ] A2A endpoint for ambassador queries

**Acceptance Criteria:**
- Scout runs on schedule
- Scout finds new scholarships
- Scout matches scholarships to anonymized profiles
- Ambassador can query Scout via A2A

**Dependencies:** Story 2.1

---

### Story 3.2: Appeal Strategist Agent
**Description:** Agent that analyzes success patterns and drafts appeals.

**Tasks:**
- [ ] Create Strategist agent config
- [ ] Commons query for school behavior
- [ ] Success pattern analyzer
- [ ] Letter draft generator
- [ ] A2A endpoint

**Acceptance Criteria:**
- Strategist can query commons for school negotiation patterns
- Strategist can identify effective arguments
- Strategist can generate appeal letter draft
- All inputs are anonymized

**Dependencies:** Story 2.1

---

### Story 3.3: Deadline Sentinel Agent
**Description:** Master calendar agent coordinating all deadlines.

**Tasks:**
- [ ] Create Sentinel agent config
- [ ] Master calendar data structure
- [ ] Deadline scraper (scholarship sites)
- [ ] Reminder scheduler
- [ ] A2A endpoint

**Acceptance Criteria:**
- Sentinel maintains master deadline calendar
- Sentinel can scrape deadlines from known sources
- Sentinel coordinates reminders across ambassadors

**Dependencies:** Story 2.1

---

### Story 3.4: Document Analyst Agent
**Description:** On-device document processing agent.

**Tasks:**
- [ ] Create Analyst agent config
- [ ] PDF parser
- [ ] Award letter extractor
- [ ] Transcript analyzer
- [ ] Completeness validator

**Acceptance Criteria:**
- Analyst runs on-device (no server call)
- Analyst extracts key fields from award letters
- Analyst validates document completeness
- No PII leaves device

**Dependencies:** Story 2.1

---

## Epic 4: Communication Channels

### Story 4.1: SMS/RCS Integration
**Description:** Connect Twilio for SMS/RCS messaging.

**Tasks:**
- [ ] Twilio account setup
- [ ] Incoming message webhook
- [ ] Outgoing message sender
- [ ] RCS rich card support
- [ ] Message router integration

**Acceptance Criteria:**
- Can receive SMS and route to ambassador
- Can send SMS responses
- Can send RCS cards with images
- Fallback to SMS if RCS unavailable

**Dependencies:** Story 2.1

---

### Story 4.2: Hume Voice Integration
**Description:** Connect Hume.ai EVI for voice conversations.

**Tasks:**
- [ ] Hume API setup
- [ ] WebSocket connection for streaming
- [ ] Emotion detection handler
- [ ] Response adaptation based on emotion
- [ ] Voice → ambassador routing

**Acceptance Criteria:**
- Can start voice session
- Emotion detected in real-time
- Ambassador adapts pace/tone based on emotion
- Voice transcribed and stored in Graphiti

**Dependencies:** Story 2.1

---

### Story 4.3: Web Chat Interface
**Description:** Simple web chat for testing and fallback.

**Tasks:**
- [ ] WebSocket endpoint
- [ ] Simple HTML/JS chat UI
- [ ] Message routing to ambassador
- [ ] Typing indicators
- [ ] Image display for generated visuals

**Acceptance Criteria:**
- Can chat with ambassador via web
- Messages persist in Graphiti
- Can display Nanobanana-generated images

**Dependencies:** Story 2.1

---

## Epic 5: Visual Generation

### Story 5.1: Nanobanana Integration
**Description:** Connect Nanobanana for on-demand visual generation.

**Tasks:**
- [ ] Nanobanana API setup
- [ ] Win card generator
- [ ] Debt comparison generator
- [ ] School comparison generator
- [ ] Scholarship match card generator

**Acceptance Criteria:**
- Can generate win card with scholarship name, amount, student name
- Can generate debt before/after comparison
- Can generate school comparison chart
- Images deliverable via RCS

**Dependencies:** Story 4.1

---

## Epic 6: Revenue & Banking

### Story 6.1: Greenlight Integration
**Description:** Connect Greenlight for disbursement detection.

**Tasks:**
- [ ] Greenlight MCP server setup (or mock)
- [ ] Webhook for transaction events
- [ ] Disbursement classifier (grant/loan/scholarship/family)
- [ ] Account verification flow

**Acceptance Criteria:**
- Can detect aid disbursement
- Can classify source type
- Can verify student account

**Dependencies:** Story 1.3

---

### Story 6.2: Commission Calculation
**Description:** Implement commission calculation and display.

**Tasks:**
- [ ] Commission rate lookup by source type
- [ ] Cap enforcement
- [ ] Breakdown generator
- [ ] Student approval flow

**Acceptance Criteria:**
- Correct rate applied per source type
- Caps enforced ($500 scholarships, $1000 grants)
- Student sees transparent breakdown
- 7-day dispute window enforced

**Dependencies:** Story 6.1

---

### Story 6.3: Stripe Connect
**Description:** Payment collection via Stripe Connect.

**Tasks:**
- [ ] Stripe Connect account setup
- [ ] Commission collection flow
- [ ] Payout to platform
- [ ] Refund handling

**Acceptance Criteria:**
- Can collect approved commission
- Funds route to platform account
- Can process refund if disputed

**Dependencies:** Story 6.2

---

## Epic 7: Personal Graph (Mobile)

### Story 7.1: Sparksee Mobile SDK Integration
**Description:** Integrate Sparksee Mobile for on-device graph.

**Tasks:**
- [ ] Obtain Sparksee Mobile license
- [ ] iOS SDK integration
- [ ] Android SDK integration
- [ ] Encryption key generation
- [ ] Basic graph operations

**Acceptance Criteria:**
- Graph database runs on device
- Data encrypted with user key
- Can create/query nodes and relationships

**Dependencies:** None (parallel track)

---

### Story 7.2: Document Vault
**Description:** Encrypted document storage on device.

**Tasks:**
- [ ] Document upload UI
- [ ] AES-256 encryption
- [ ] Hash-based deduplication
- [ ] Document type classification
- [ ] Integration with Document Analyst

**Acceptance Criteria:**
- Documents encrypted before storage
- Duplicates detected and skipped
- Document Analyst can process without decrypting off-device

**Dependencies:** Story 7.1

---

### Story 7.3: Profile Sync
**Description:** Anonymized profile sync to server.

**Tasks:**
- [ ] Anonymization pipeline
- [ ] Consent UI
- [ ] Sync trigger
- [ ] Conflict resolution

**Acceptance Criteria:**
- Profile anonymized before sync
- User explicitly consents
- Sync happens on schedule or event
- Server never receives PII

**Dependencies:** Story 7.1

---

## Epic 8: Commons & Federation

### Story 8.1: Outcome Contribution
**Description:** Contribute anonymized outcomes to commons.

**Tasks:**
- [ ] Outcome capture (scholarship won, appeal success)
- [ ] Anonymization
- [ ] Verification (disbursement-based)
- [ ] Commons update

**Acceptance Criteria:**
- Outcomes captured automatically
- Anonymized before contribution
- Verified via disbursement detection
- Commons updated with new data

**Dependencies:** Story 6.1, Story 7.3

---

### Story 8.2: Strategy Learning
**Description:** Update strategy effectiveness from outcomes.

**Tasks:**
- [ ] Strategy → outcome linking
- [ ] Success rate calculation
- [ ] Sample size tracking
- [ ] Confidence scoring

**Acceptance Criteria:**
- Strategies linked to outcomes
- Success rates update over time
- Low sample size flagged
- High confidence strategies surfaced

**Dependencies:** Story 8.1

---

### Story 8.3: A2A Federation
**Description:** Enable ambassador-to-ambassador communication.

**Tasks:**
- [ ] A2A protocol implementation
- [ ] Anonymized query format
- [ ] Response aggregation
- [ ] Rate limiting

**Acceptance Criteria:**
- Ambassadors can query other ambassadors
- All queries anonymized
- Responses aggregated
- Rate limits prevent abuse

**Dependencies:** Story 3.1, Story 3.2, Story 3.3

---

## Epic 9: Anti-Gaming

### Story 9.1: Outcome Verification
**Description:** Verify outcomes via disbursement detection.

**Tasks:**
- [ ] Disbursement → outcome matching
- [ ] Verification status tracking
- [ ] Unverified outcome handling
- [ ] Fraud detection heuristics

**Acceptance Criteria:**
- Outcomes matched to disbursements
- Verified flag set
- Unverified outcomes down-weighted
- Suspicious patterns flagged

**Dependencies:** Story 6.1, Story 8.1

---

### Story 9.2: Anomaly Detection
**Description:** Detect gaming attempts in commons contributions.

**Tasks:**
- [ ] Contribution pattern analysis
- [ ] Statistical anomaly detection
- [ ] Source reputation tracking
- [ ] Automatic quarantine

**Acceptance Criteria:**
- Unusual contribution patterns detected
- Anomalies quarantined
- Source reputation adjusted
- Manual review queue

**Dependencies:** Story 8.1

---

## Priority Order

1. **Infrastructure:** 1.1 → 1.2 → 1.3
2. **Core Agent:** 2.1 → 2.2 → 2.3
3. **Communication:** 4.1 (SMS first for testing)
4. **Specialists:** 3.1 → 3.2 (Scout and Strategist most valuable)
5. **Voice:** 4.2
6. **Visuals:** 5.1
7. **Revenue:** 6.1 → 6.2 → 6.3
8. **Mobile:** 7.1 → 7.2 → 7.3 (parallel track)
9. **Federation:** 8.1 → 8.2 → 8.3
10. **Security:** 9.1 → 9.2
