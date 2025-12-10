# Student Ambassador Platform - Project Brief

## Project Overview

**Name:** Student Ambassador Platform
**Type:** Greenfield Full-Stack Application
**Domain:** EdTech / FinTech / AI Agents

### Vision Statement
An autonomous AI advocate that helps students navigate college applications and financial aid, making money when they find free money and nothing when they borrow.

### Problem Statement
Students face institutions with teams of analysts. They get generic advice, miss deadlines, take on unnecessary debt. The wealthy hire consultants. Everyone else doesn't.

### Target Users
- High school juniors/seniors (16-18)
- College students (18-22)
- Recent graduates (22-27)
- Parents (secondary)

### Key Differentiators
1. **Personal AI that knows you** - maintains context across months/years
2. **Proactive, not reactive** - anticipates needs, doesn't wait for commands
3. **Collective intelligence** - learns from all students, benefits all students
4. **Anti-debt incentive** - earns on scholarships, nothing on loans
5. **Voice-first** - emotion-aware conversation, not forms and dashboards

---

## Technical Constraints

### Must Use
- **Sparksee Mobile** - on-device personal graph (<50KB, AES-256)
- **FalkorDB** - server-side commons graph
- **Graphiti** - temporal knowledge layer
- **Agent Zero** - multi-agent framework
- **Hume.ai EVI** - emotion-aware voice
- **Nanobanana** - on-demand image generation
- **Greenlight** - banking/KYC trust anchor

### Architecture Pattern
- Three-layer graph (personal → ambassador → commons)
- 100% generated UX (no React, no dashboard)
- MCP for tool integration
- A2A for ambassador federation

---

## Existing Assets

### Reference Implementation
```
student_ambassador_api/
├── main.py          # FastAPI routes (CRUD for students, applications, negotiations)
├── models.py        # Pydantic models (Student, Document, TestScore, etc.)
├── database.py      # In-memory storage (placeholder)
└── requirements.txt
```

### Specification Document
`student-ambassador.md` - Complete feature spec including:
- Full FalkorDB schema
- Graphiti integration code
- Multi-agent coordination
- Hume emotion responses
- Revenue model
- User flows

---

## Success Criteria

### User Outcomes
- Average debt at graduation 30% below national average
- $5,000+ scholarships found per student annually
- <20% loan acceptance after scholarship search
- >40% aid appeal success rate

### Business Outcomes
- $400-800 revenue per student annually
- >80% gross margin
- Viral coefficient >1.2

---

## Scope Boundaries

### In Scope
- Personal ambassador agent
- Specialist agents (Scholarship Scout, Appeal Strategist, Deadline Sentinel, Document Analyst)
- Voice interface with emotion awareness
- SMS/RCS/web chat surfaces
- Scholarship search and matching
- Aid appeal drafting
- Deadline tracking
- Document parsing (award letters, transcripts)
- Win card generation
- Commission collection via Greenlight

### Out of Scope (Future)
- School partnerships
- International students
- Graduate/professional school
- Post-graduation grants

---

## Stakeholders

| Role | Responsibility |
|------|---------------|
| Steve | Product vision, architecture decisions |
| Claude | Implementation, iteration |

---

## Dependencies

| Dependency | Status | Risk |
|------------|--------|------|
| Sparksee Mobile license | TBD | Medium - need to verify pricing/terms |
| FalkorDB | Available | Low - open source |
| Graphiti | Available | Low - open source |
| Hume.ai API | Available | Low - has free tier |
| Nanobanana | Available | Low |
| Greenlight API | TBD | High - requires partnership |
| Agent Zero | Available | Low - open source |
