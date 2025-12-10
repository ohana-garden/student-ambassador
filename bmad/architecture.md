# Student Ambassador Platform - Architecture Document

## 1. System Overview

```
┌────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                              │
├────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   Hume EVI   │  │  SMS/RCS     │  │  Web Chat    │  │   Email    │ │
│  │   (Voice)    │  │  (Twilio)    │  │  (WebSocket) │  │  (SendGrid)│ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘ │
│         │                 │                 │                 │        │
│         └─────────────────┴────────┬────────┴─────────────────┘        │
│                                    │                                   │
│                            ┌───────▼───────┐                           │
│                            │ Message Router │                          │
│                            └───────┬───────┘                           │
└────────────────────────────────────┼───────────────────────────────────┘
                                     │
┌────────────────────────────────────┼───────────────────────────────────┐
│                              AGENT LAYER                               │
├────────────────────────────────────┼───────────────────────────────────┤
│                            ┌───────▼───────┐                           │
│                            │  Ambassador   │                           │
│                            │    Agent      │                           │
│                            │ (Agent Zero)  │                           │
│                            └───────┬───────┘                           │
│                                    │                                   │
│         ┌──────────────────────────┼──────────────────────────┐       │
│         │                          │                          │        │
│  ┌──────▼──────┐  ┌───────────────▼───────────────┐  ┌───────▼──────┐ │
│  │ Scholarship │  │      Appeal Strategist        │  │   Deadline   │ │
│  │    Scout    │  │                               │  │   Sentinel   │ │
│  └──────┬──────┘  └───────────────┬───────────────┘  └───────┬──────┘ │
│         │                         │                          │        │
│         └─────────────────────────┴──────────────────────────┘        │
│                                   │                                    │
│                           A2A Protocol (anonymized)                    │
└───────────────────────────────────┼────────────────────────────────────┘
                                    │
┌───────────────────────────────────┼────────────────────────────────────┐
│                              DATA LAYER                                │
├───────────────────────────────────┼────────────────────────────────────┤
│  ┌────────────────────┐   ┌───────▼───────┐   ┌────────────────────┐  │
│  │   DEVICE           │   │    SERVER     │   │     EXTERNAL       │  │
│  │                    │   │               │   │                    │  │
│  │  Sparksee Mobile   │   │   FalkorDB    │   │    Greenlight      │  │
│  │  (Personal Graph)  │   │   (Commons)   │   │    (Banking)       │  │
│  │                    │   │               │   │                    │  │
│  │  - PII             │   │   Graphiti    │   │    Nanobanana      │  │
│  │  - Documents       │   │   (Temporal)  │   │    (Images)        │  │
│  │  - Financials      │   │               │   │                    │  │
│  └────────────────────┘   └───────────────┘   └────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Tech Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Agent Framework | Agent Zero | Latest | Multi-agent coordination, tool creation, hierarchical delegation |
| Personal Graph | Sparksee Mobile | Latest | <50KB, AES-256, iOS/Android native, graph queries on device |
| Commons Graph | FalkorDB | Latest | Cypher queries, Redis-based, 500x faster than Neo4j |
| Temporal Layer | Graphiti | Latest | Bi-temporal facts, episodic memory, native FalkorDB support |
| Voice | Hume.ai EVI | Latest | Emotion detection, prosody control, low latency |
| Image Gen | Nanobanana | Latest | Gemini 2.5 Flash, on-demand generation |
| Banking | Greenlight MCP | TBD | KYC, disbursement detection |
| Messaging | Twilio | Latest | SMS/RCS, reliability |
| API | FastAPI | 0.100+ | Async, Pydantic validation, auto docs |
| Runtime | Python | 3.11+ | Agent Zero requirement |

---

## 3. Component Design

### 3.1 Ambassador Agent

```python
# Agent Zero configuration
ambassador_config = {
    "name": "StudentAmbassador",
    "model": "claude-sonnet-4",
    "fallback_model": "claude-haiku-4",
    "memory": {
        "type": "graphiti",
        "backend": "falkordb",
        "episodic": True,
        "temporal": True
    },
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
        "win_card_generate",
        "debt_compare"
    ],
    "proactive_triggers": [
        {"condition": "deadline_within_days < 7", "action": "send_reminder"},
        {"condition": "deadline_within_days < 1", "action": "send_urgent"},
        {"condition": "new_scholarship_match", "action": "queue_conversation"},
        {"condition": "days_since_interaction > 5", "action": "check_in"},
        {"condition": "disbursement_detected", "action": "process_commission"}
    ]
}
```

### 3.2 Specialist Agents

```python
# Scholarship Scout
scholarship_scout_config = {
    "name": "ScholarshipScout",
    "model": "claude-haiku-4",  # Cost optimization
    "tools": [
        "scholarship_db_search",
        "criteria_match",
        "legitimacy_verify",
        "deadline_track"
    ],
    "schedule": "continuous",  # Always crawling
    "output": "anonymized_matches"  # Never sees PII
}

# Appeal Strategist
appeal_strategist_config = {
    "name": "AppealStrategist",
    "model": "claude-sonnet-4",  # Needs reasoning
    "tools": [
        "commons_query",
        "success_pattern_analyze",
        "letter_draft",
        "tactic_recommend"
    ],
    "input": "anonymized_profile",  # Never sees PII
    "output": "strategy_recommendations"
}

# Deadline Sentinel
deadline_sentinel_config = {
    "name": "DeadlineSentinel",
    "model": "claude-haiku-4",
    "tools": [
        "calendar_manage",
        "reminder_schedule",
        "deadline_scrape"
    ],
    "schedule": "hourly"
}

# Document Analyst
document_analyst_config = {
    "name": "DocumentAnalyst",
    "model": "claude-sonnet-4",
    "tools": [
        "pdf_parse",
        "award_letter_extract",
        "transcript_analyze",
        "completeness_validate"
    ],
    "execution": "on_device"  # Never leaves device
}
```

### 3.3 Message Router

```python
class MessageRouter:
    """Routes incoming messages to appropriate handler."""
    
    async def route(self, message: IncomingMessage) -> Response:
        # Identify channel
        channel = self.identify_channel(message)
        
        # Get or create ambassador for user
        ambassador = await self.get_ambassador(message.user_id)
        
        # Route based on channel capabilities
        if channel == Channel.VOICE:
            return await self.handle_voice(ambassador, message)
        elif channel == Channel.SMS:
            return await self.handle_sms(ambassador, message)
        elif channel == Channel.WEB:
            return await self.handle_web(ambassador, message)
        elif channel == Channel.EMAIL:
            return await self.handle_email(ambassador, message)
```

---

## 4. Data Models

### 4.1 Personal Graph (Sparksee Mobile)

```cypher
// Node types
(:Student {
    id: String,
    created_at: DateTime,
    encryption_key_hash: String
})

(:Document {
    id: String,
    type: String,  // transcript, award_letter, tax_return, etc.
    content_hash: String,
    encrypted_content: Bytes,
    uploaded_at: DateTime
})

(:TestScore {
    id: String,
    type: String,  // SAT, ACT, AP, etc.
    score: Float,
    date: Date
})

(:Activity {
    id: String,
    name: String,
    role: String,
    hours_per_week: Int,
    years: [Int]
})

(:Essay {
    id: String,
    school_id: String,
    prompt: String,
    version: Int,
    content_hash: String,
    status: String  // draft, final
})

(:Recommendation {
    id: String,
    recommender_name: String,
    recommender_role: String,
    status: String,  // requested, received, submitted
    requested_date: Date
})

(:Financial {
    id: String,
    year: Int,
    efc: Float,
    household_income_range: String,
    household_size: Int
})

// Relationships
(:Student)-[:HAS_DOCUMENT]->(:Document)
(:Student)-[:HAS_SCORE]->(:TestScore)
(:Student)-[:HAS_ACTIVITY]->(:Activity)
(:Student)-[:HAS_ESSAY]->(:Essay)
(:Student)-[:HAS_RECOMMENDATION]->(:Recommendation)
(:Student)-[:HAS_FINANCIAL]->(:Financial)
```

### 4.2 Commons Graph (FalkorDB)

```cypher
// Node types
(:AnonymizedProfile {
    id: String,
    gpa_range: String,  // "3.5-4.0"
    test_range: String,  // "1400-1500"
    income_bracket: String,
    first_gen: Boolean,
    region: String
})

(:School {
    id: String,
    name: String,
    type: String,  // public, private, community
    location: String,
    selectivity: String
})

(:ScholarshipSource {
    id: String,
    name: String,
    amount_min: Float,
    amount_max: Float,
    criteria: String,
    deadline: Date,
    verified: Boolean
})

(:Strategy {
    id: String,
    type: String,  // appeal, negotiation, application
    description: String,
    success_rate: Float,
    sample_size: Int,
    last_updated: DateTime
})

(:Outcome {
    id: String,
    type: String,  // scholarship_won, appeal_success, admission
    amount: Float,
    verified: Boolean,
    timestamp: DateTime
})

(:BehaviorType {
    id: String,
    pattern: String,  // negotiates_with_competing_offers, etc.
    description: String
})

// Relationships
(:AnonymizedProfile)-[:APPLIED_TO {
    status: String,
    timeline: Map
}]->(:School)

(:AnonymizedProfile)-[:MATCHED_TO {
    score: Float,
    reasons: [String]
}]->(:ScholarshipSource)

(:AnonymizedProfile)-[:RECEIVED]->(:Outcome)

(:Strategy)-[:EFFECTIVE_FOR {
    success_rate: Float,
    sample_size: Int
}]->(:AnonymizedProfile)

(:Strategy)-[:TARGETS]->(:School)

(:School)-[:EXHIBITS_BEHAVIOR {
    confidence: Float,
    sample_size: Int
}]->(:BehaviorType)

(:ScholarshipSource)-[:AWARDED_TO {
    year: Int,
    amount: Float
}]->(:AnonymizedProfile)
```

### 4.3 Graphiti Temporal Schema

```python
# Episodic memory
Episode = {
    "id": str,
    "name": str,  # "scholarship_discussion_2025_01_15"
    "body": str,  # Full conversation transcript
    "source": str,  # "voice_session", "sms", "web"
    "reference_time": datetime,
    "entities_extracted": List[str],
    "relationships_extracted": List[tuple]
}

# Temporal facts
Fact = {
    "subject": str,
    "predicate": str,
    "object": str,
    "valid_from": datetime,
    "valid_to": datetime | None,  # None = currently valid
    "source": str,
    "confidence": float
}

# Example facts
facts = [
    {
        "subject": "Stanford",
        "predicate": "average_aid_package",
        "object": "$58,000",
        "valid_from": "2024-01-01",
        "valid_to": None
    },
    {
        "subject": "Gates_Scholarship",
        "predicate": "deadline",
        "object": "2025-09-15",
        "valid_from": "2024-08-01",
        "valid_to": None
    }
]
```

---

## 5. API Design

### 5.1 Ambassador API (Internal)

```yaml
openapi: 3.0.0
info:
  title: Student Ambassador Internal API
  version: 1.0.0

paths:
  /students:
    post:
      summary: Create student profile
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/StudentCreate'
    get:
      summary: List students (admin only)
      
  /students/{student_id}:
    get:
      summary: Get student profile
    put:
      summary: Update student profile
    delete:
      summary: Delete student and all data
      
  /students/{student_id}/scholarships:
    get:
      summary: Get scholarship matches
      parameters:
        - name: min_score
          in: query
          schema:
            type: number
            
  /students/{student_id}/deadlines:
    get:
      summary: Get upcoming deadlines
      
  /students/{student_id}/appeals:
    post:
      summary: Generate appeal letter
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AppealRequest'
              
  /conversations:
    post:
      summary: Send message to ambassador
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ConversationMessage'
              
  /disbursements:
    post:
      summary: Record disbursement (webhook from Greenlight)
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Disbursement'
```

### 5.2 MCP Server Configuration

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
      "auth": {
        "type": "oauth2_pkce",
        "scopes": ["read:transactions", "read:account"]
      }
    },
    "nanobanana": {
      "endpoint": "https://api.nanobanana.ai/mcp",
      "capabilities": [
        "text_to_image",
        "infographic_generation"
      ],
      "auth": {
        "type": "api_key"
      }
    },
    "scholarship_db": {
      "endpoint": "internal://scholarship-scout/mcp",
      "capabilities": [
        "search",
        "match",
        "verify"
      ]
    }
  }
}
```

---

## 6. Sequence Diagrams

### 6.1 Scholarship Discovery Flow

```
Student          Ambassador       Scout           Commons
   │                 │              │               │
   │  "Find me       │              │               │
   │  scholarships"  │              │               │
   │────────────────>│              │               │
   │                 │              │               │
   │                 │  Request     │               │
   │                 │  (anonymized)│               │
   │                 │─────────────>│               │
   │                 │              │               │
   │                 │              │  Query        │
   │                 │              │  patterns     │
   │                 │              │──────────────>│
   │                 │              │               │
   │                 │              │  Success      │
   │                 │              │  rates        │
   │                 │              │<──────────────│
   │                 │              │               │
   │                 │  Matches     │               │
   │                 │  + reasons   │               │
   │                 │<─────────────│               │
   │                 │              │               │
   │  "I found 12    │              │               │
   │  matches..."    │              │               │
   │<────────────────│              │               │
   │                 │              │               │
```

### 6.2 Commission Collection Flow

```
Greenlight       Ambassador       Student         Stripe
    │                │               │               │
    │  Disbursement  │               │               │
    │  webhook       │               │               │
    │───────────────>│               │               │
    │                │               │               │
    │                │  Classify     │               │
    │                │  (grant/loan/ │               │
    │                │   scholarship)│               │
    │                │               │               │
    │                │  Calculate    │               │
    │                │  commission   │               │
    │                │               │               │
    │                │  "You received│               │
    │                │  $5,000 from  │               │
    │                │  Rotary. My   │               │
    │                │  fee is $250" │               │
    │                │──────────────>│               │
    │                │               │               │
    │                │               │  Approve      │
    │                │               │  (or dispute) │
    │                │<──────────────│               │
    │                │               │               │
    │                │  Deduct       │               │
    │                │───────────────────────────────>
    │                │               │               │
```

---

## 7. Security Architecture

### 7.1 Data Classification

| Data Type | Location | Encryption | Access |
|-----------|----------|------------|--------|
| PII | Device only | AES-256, user key | User only |
| Documents | Device only | AES-256, user key | User + Document Analyst (on-device) |
| Anonymized profile | Server | TLS in transit | Ambassador + Specialists |
| Commons data | Server | None (public) | All agents |
| Conversation logs | Graphiti | TLS in transit | Ambassador only |

### 7.2 Key Management

```python
class KeyManager:
    """User holds sole keys. We never see them."""
    
    def generate_user_key(self) -> bytes:
        """Generate on device, never transmitted."""
        return secrets.token_bytes(32)
    
    def encrypt_document(self, doc: bytes, key: bytes) -> bytes:
        """AES-256-GCM encryption on device."""
        cipher = AESGCM(key)
        nonce = secrets.token_bytes(12)
        return nonce + cipher.encrypt(nonce, doc, None)
    
    def decrypt_document(self, encrypted: bytes, key: bytes) -> bytes:
        """Decryption on device only."""
        cipher = AESGCM(key)
        nonce = encrypted[:12]
        return cipher.decrypt(nonce, encrypted[12:], None)
```

### 7.3 Anonymization Pipeline

```python
class Anonymizer:
    """Irreversible anonymization for commons contributions."""
    
    def anonymize_profile(self, student: Student) -> AnonymizedProfile:
        return AnonymizedProfile(
            id=self.generate_anonymous_id(),  # No link to original
            gpa_range=self.bucket_gpa(student.gpa),
            test_range=self.bucket_score(student.test_scores),
            income_bracket=self.bucket_income(student.financial.income),
            first_gen=student.first_gen,
            region=self.generalize_region(student.location)
        )
    
    def bucket_gpa(self, gpa: float) -> str:
        """Round to ranges to prevent re-identification."""
        if gpa >= 3.75: return "3.75-4.0"
        if gpa >= 3.5: return "3.5-3.75"
        if gpa >= 3.25: return "3.25-3.5"
        # etc.
```

---

## 8. Deployment Architecture

### 8.1 Container Structure

```yaml
# docker-compose.yml
services:
  ambassador-api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - FALKORDB_URL=redis://falkordb:6379
      - GRAPHITI_URL=redis://falkordb:6379
    depends_on:
      - falkordb
      
  falkordb:
    image: falkordb/falkordb:latest
    ports:
      - "6379:6379"
    volumes:
      - falkordb_data:/data
      
  scholarship-scout:
    build: ./agents/scout
    environment:
      - FALKORDB_URL=redis://falkordb:6379
      
  appeal-strategist:
    build: ./agents/strategist
    environment:
      - FALKORDB_URL=redis://falkordb:6379
      
  deadline-sentinel:
    build: ./agents/sentinel
    environment:
      - FALKORDB_URL=redis://falkordb:6379

volumes:
  falkordb_data:
```

### 8.2 Mobile SDK (Sparksee)

```swift
// iOS integration
import SparkseeKit

class PersonalGraph {
    private let db: Database
    private let session: Session
    private let graph: Graph
    
    init(encryptionKey: Data) throws {
        let config = SparkseeConfig()
        config.setEncryptionKey(encryptionKey)
        db = try Sparksee.open(config)
        session = db.newSession()
        graph = session.getGraph()
    }
    
    func addDocument(_ doc: Document) throws {
        let node = graph.newNode(graph.findType("Document"))
        graph.setAttribute(node, "type", doc.type)
        graph.setAttribute(node, "content_hash", doc.contentHash)
        graph.setAttribute(node, "encrypted_content", doc.encryptedContent)
    }
}
```

---

## 9. Monitoring & Observability

### 9.1 Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Voice latency p95 | <500ms | >750ms |
| Scholarship search p95 | <2s | >3s |
| Ambassador response time | <1s | >2s |
| Commons query time | <100ms | >200ms |
| Commission collection rate | >95% | <90% |

### 9.2 Logging

```python
# Structured logging for all agent actions
logger.info(
    "scholarship_match",
    extra={
        "student_id_hash": hash(student_id),  # Never log real ID
        "matches_found": len(matches),
        "top_match_score": matches[0].score if matches else None,
        "duration_ms": duration
    }
)
```

---

## 10. Testing Strategy

### 10.1 Unit Tests
- Agent tool functions
- Anonymization pipeline
- Commission calculation
- Scholarship matching algorithm

### 10.2 Integration Tests
- Ambassador → Specialist communication
- Graphiti temporal queries
- FalkorDB graph operations
- Greenlight webhook handling

### 10.3 End-to-End Tests
- Complete user flows (onboarding, scholarship discovery, appeal)
- Voice conversation simulation
- Commission collection flow

### 10.4 Security Tests
- PII never leaves device
- Anonymization irreversibility
- Key isolation
