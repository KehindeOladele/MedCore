# MedCore Project Workflow (Stages, Deliverables, KPIs)

<aside>
🧭

**How to use this page**

- Each stage ends with a **Stage Gate** (go/no-go).
- Keep deliverables as pages inside MedCore, and link them here.
- Track KPIs weekly during execution-heavy stages (Build/Test).
</aside>

### 0) Project setup & governance (Week 0)

**Goal:** Align scope, roles, cadence, and tooling before deep work.

**Key activities**

- Confirm problem space, target users, and success definition.
- Define team roles and decision-making.
- Create a single source of truth for docs.

**Deliverables (by end of stage)**

- [Project Charter](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Week%200%20-%20Project%20setup%20%26%20governance/Project%20Charter.md)
- [RACI / Roles & Responsibilities](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Week%200%20-%20Project%20setup%20%26%20governance/RACI%20Roles%20%26%20Responsibilities.md)
- [Communication Plan (Meeting cadence, channels)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Week%200%20-%20Project%20setup%20%26%20governance/Communication%20Plan%20(Meeting%20cadence%2C%20channels).md)
- [Risk Register (Initial)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Week%200%20-%20Project%20setup%20%26%20governance/Risk%20Register%20(Initial).md)
- [High-level Timeline & Milestones](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Week%200%20-%20Project%20setup%20%26%20governance/High-level%20Timeline%20%26%20Milestones.md)

**KPIs (stage health)**

- Charter approved (Yes/No)
- Stakeholder alignment score (simple 1–5 survey)
- Risks identified (count) with owners assigned (percentage)

**Templates**

- Project Charter (template)
    - **Project name:** MedCore
    - **Owner:**
    - **Problem statement (1–2 sentences):**
    - **Target users:**
    - **Goals (3–5):**
        - 
    - **Non-goals (3–5):**
        - 
    - **Scope (in):**
        - 
    - **Scope (out):**
        - 
    - **Assumptions:**
        - 
    - **Constraints (time/budget/tech/regulatory):**
        - 
    - **Success metrics (top 3):**
        - 
    - **Milestones:**
        - 
    - **Approval:**

---

### 1) Discovery: Research & data landscape

**Goal:** Build evidence about the domain (interoperability, regulation, security, competitors) and define what data is needed.

**Key activities**

- Desk research: FHIR basics, typical healthcare data flows, interoperability patterns.
- Compliance scan: local regulations + global references (HIPAA-like principles), privacy and consent.
- Security/governance scan: access control, audit trails, encryption, data minimization.
- Competitor/alternative analysis.
- Define data sources and data requirements.

**Deliverables (by end of stage)**

- [Research brief (problem space overview)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%201%20-%20Discovery%20Research%20%26%20data%20landscape/Research%20brief%20(problem%20space%20overview).md)
- [Competitive landscape doc](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%201%20-%20Discovery%20Research%20%26%20data%20landscape/Competitive%20landscape.md)
- [Interoperability notes (FHIR resources and integration approach)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%201%20-%20Discovery%20Research%20%26%20data%20landscape/Interoperability%20notes%20(FHIR%20resources%20%2B%20integration%20approach).md)
- [Compliance & privacy checklist (initial)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%201%20-%20Discovery%20Research%20%26%20data%20landscape/Compliance%20%26%20privacy%20checklist%20(initial).md)
- [Data inventory + data requirements](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%201%20-%20Discovery%20Research%20%26%20data%20landscape/Data%20inventory%20%2B%20data%20requirements.md)
- [Insights summary (top 10 findings + implications)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%201%20-%20Discovery%20Research%20%26%20data%20landscape/Insights%20summary%20(top%20findings%20%2B%20implications).md)

**KPIs**

- 

# credible sources reviewed (target: 15–30)

- 

# stakeholder/user pain points identified (target: 10+)

- 

# competitors/alternatives analyzed (target: 5–10)

- “Unknowns list” reduced (baseline vs end)

**Templates**

- Research Brief (template)
    - **Research question:**
    - **What we already believe:**
        - 
    - **Methods:** desk research / expert calls / surveys / interviews
    - **Sources reviewed (links):**
        - 
    - **Key findings (bullets):**
        - 
    - **Implications for MedCore:**
        - 
    - **Open questions:**
        - 
- Competitive Landscape (template)
    - **Competitor name:**
    - **What they do (1–2 lines):**
    - **Target users:**
    - **Key features:**
        - 
    - **Strengths:**
        - 
    - **Weaknesses / gaps:**
        - 
    - **Pricing (if known):**
    - **Differentiation opportunities for MedCore:**
        - 

---

### 2) Empathize: User research

**Goal:** Understand user needs, context, jobs-to-be-done, and constraints.

**Key activities**

- Define research plan (who, why, how many).
- Conduct interviews and/or surveys.
- Create personas and empathy maps.
- Extract themes and prioritize needs.

**Deliverables (by end of stage)**

- [Research plan + screener](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%202%20-%20Empathize%20User%20research/Research%20plan%20%2B%20screener.md)
- [Interview guide + survey form](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%202%20-%20Empathize%20User%20research/Interview%20guide%20%2B%20survey%20form.md)
- [Interview notes/transcripts (organized)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%202%20-%20Empathize%20User%20research/Interview%20notes%20transcripts.md)
- [Personas (2-4)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%202%20-%20Empathize%20User%20research/Personas.md)
- [Empathy maps (per persona)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%202%20-%20Empathize%20User%20research/Empathy%20maps.md)
- [User needs list + ranked pain points](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%202%20-%20Empathize%20User%20research/User%20needs%20list%20%2B%20ranked%20pain%20points.md)

**KPIs**

- 

# interviews completed (target: 8–15)

- 

# survey responses (target: 30–100)

- Persona coverage (percentage of target segments represented)
- % of insights mapped to evidence (each insight links to a quote/response)

**Templates**

- User Interview Guide (template)
    - **Goal of interview:**
    - **Participant profile:**
    - **Warm-up:** role, daily workflow, tools used
    - **Context questions:**
        - Walk me through a recent case/workflow.
        - What data do you need and where does it come from?
    - **Pain points:**
        - Where do delays or errors happen?
        - What is most frustrating or risky?
    - **Workarounds:**
        - What do you do today to solve it?
    - **Security/privacy/compliance prompts:**
        - What approvals or policies affect you?
    - **Success definition:**
        - If this was solved, what would improve?
    - **Wrap-up:** willingness for follow-up, preferred contact
- Persona (template)
    - **Name:**
    - **Role / setting:**
    - **Goals:**
        - 
    - **Jobs to be done:**
        - 
    - **Pain points:**
        - 
    - **Constraints (time, policy, tools):**
        - 
    - **Motivations:**
        - 
    - **Quotes (evidence):**
        - 

---

### 3) Define: Problem framing & requirements

**Goal:** Turn research into a clear problem statement, measurable outcomes, and solution requirements.

**Key activities**

- Synthesize insights into themes.
- Write problem statement and “how might we” prompts.
- Define scope and requirements.
- Identify risks and assumptions.

**Deliverables (by end of stage)**

- [Problem statement (final)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%203%20-%20Define%20Problem%20framing%20%26%20requirements/Problem%20statement%20(final).md)
- [Solution statement / value proposition](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%203%20-%20Define%20Problem%20framing%20%26%20requirements/Solution%20statement%20%2B%20value%20proposition.md)
- [Success metrics (North Star + supporting metrics)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%203%20-%20Define%20Problem%20framing%20%26%20requirements/Success%20metrics%20(North%20Star%20%2B%20supporting%20metrics).md)
- [Requirements (functional + non-functional)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%203%20-%20Define%20Problem%20framing%20%26%20requirements/Requirements%20(functional%20%2B%20non-functional).md)
- [Assumptions & risks log (updated)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%203%20-%20Define%20Problem%20framing%20%26%20requirements/Assumptions%20%26%20risks%20log%20(updated).md)
- [Prioritized backlog (MVP vs later)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%203%20-%20Define%20Problem%20framing%20%26%20requirements/Prioritized%20backlog%20(MVP%20vs%20later).md)

**KPIs**

- Problem statement clarity (stakeholder score 1–5)
- Requirements completeness (coverage of top pains, percentage)
- MVP scope size (small enough to ship in planned timeframe)

**Templates**

- Problem Statement (template)
    - **For**
    - **Who**
    - **The problem is**
    - **Because**
    - **The impact is**
    - **We will know it is solved when** (measurable)
- Requirements (template)
    - **Functional requirements**
        - FR1:
        - FR2:
    - **Non-functional requirements**
        - Security:
        - Privacy:
        - Performance:
        - Reliability:
        - Auditability:
        - Compliance notes:
    - **Out of scope:**
        - 

---

### 4) Ideate: Solution design & prioritization

**Goal:** Generate solution options, select an approach, and define the MVP experience.

**Key activities**

- Brainstorm and sketch flows.
- Evaluate options (impact vs effort, risk).
- Map user journey and key workflows.
- Define MVP feature set and acceptance criteria.

**Deliverables (by end of stage)**

- [Idea bank (divergent list)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%204%20-%20Ideate%20Solution%20design%20%26%20prioritization/Idea%20bank%20(divergent%20list).md)
- [Prioritization matrix (impact/effort)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%204%20-%20Ideate%20Solution%20design%20%26%20prioritization/Prioritization%20matrix%20(impact%20%2B%20effort).md)
- [User journey map](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%204%20-%20Ideate%20Solution%20design%20%26%20prioritization/User%20journey%20map.md)
- [MVP scope (features + exclusions)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%204%20-%20Ideate%20Solution%20design%20%26%20prioritization/MVP%20scope%20(features%20%2B%20exclusions).md)
- [UX flows + information architecture](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%204%20-%20Ideate%20Solution%20design%20%26%20prioritization/UX%20flows%20%2B%20information%20architecture.md)
- [Acceptance criteria for MVP features](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%204%20-%20Ideate%20Solution%20design%20%26%20prioritization/Acceptance%20criteria%20for%20MVP%20features.md)

**KPIs**

- 

# solution options considered (target: 10+)

- % MVP features tied to validated user needs
- Time-to-value in main workflow (estimated steps/time)

**Templates**

- Impact vs Effort (template)
    - **Idea:**
    - **User problem it solves:**
    - **Expected impact (1–5):**
    - **Effort (1–5):**
    - **Risks/unknowns:**
    - **Decision:** Keep / Park / Drop
- MVP Scope (template)
    - **MVP goal (1 sentence):**
    - **In scope (features):**
        - 
    - **Out of scope (explicit):**
        - 
    - **Key workflows:**
        - 
    - **Definition of Done:**
        - 

---

### 5) Plan & architecture (pre-build)

**Goal:** Convert the MVP design into an executable build plan with architecture and delivery milestones.

**Key activities**

- Define technical architecture (data model, services, integrations).
- Define API + interoperability approach (FHIR mapping).
- Threat model and security controls.
- Delivery plan: milestones, sprints, release criteria.

**Deliverables (by end of stage)**

- [Architecture overview (diagrams + components)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%205%20-%20Plan%20%26%20architecture/Architecture%20overview%20(diagrams%20%2B%20components).md)
- [Data model + FHIR mapping notes](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%205%20-%20Plan%20%26%20architecture/Data%20model%20%2B%20FHIR%20mapping%20notes.md)
- [Security plan (authn/authz, audit logs, encryption)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%205%20-%20Plan%20%26%20architecture/Security%20plan%20(authn%20%2B%20authz%2C%20audit%20logs%2C%20encryption).md)
- [Threat model (basic)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%205%20-%20Plan%20%26%20architecture/Threat%20model%20(basic).md)
- [Sprint plan / milestone plan](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%205%20-%20Plan%20%26%20architecture/Sprint%20plan%20%2B%20milestone%20plan.md)

**KPIs**

- Architecture review pass rate (stakeholder/tech review Yes/No)
- 

# critical risks mitigated before build

- Delivery plan confidence (1–5)

**Templates**

- Architecture Overview (template)
    - **Components:**
        - Client apps:
        - Backend services:
        - Data storage:
        - Integrations:
    - **Data flow (bullets):**
        - 
    - **Key decisions:**
        - 
    - **Open questions:**
        - 

---

### 6) Prototyping / Build (MVP)

**Goal:** Build the MVP (or high-fidelity prototype) that can be tested with real users.

**Key activities**

- Implement prioritized workflows.
- Create test data and environments.
- Instrument product analytics and logging.
- Prepare demo script.

**Deliverables (by end of stage)**

- [Working MVP build (or hi-fi prototype)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%206%20-%20Prototyping%20Build%20(MVP)/Working%20MVP%20build%20(or%20hi-fi%20prototype).md)
- [Release notes (what is included)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%206%20-%20Prototyping%20Build%20(MVP)/Release%20notes%20(what%20is%20included).md)
- [QA checklist + test results](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%206%20-%20Prototyping%20Build%20(MVP)/QA%20checklist%20%2B%20test%20results.md)
- [Analytics plan + instrumentation events](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%206%20-%20Prototyping%20Build%20(MVP)/Analytics%20plan%20%2B%20instrumentation%20events.md)
- [Demo script + walkthrough](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%206%20-%20Prototyping%20Build%20(MVP)/Demo%20script%20%2B%20walkthrough.md)

**KPIs**

- Sprint velocity / throughput (planned vs delivered)
- Defect rate (bugs per week, severity)
- Build stability (crash rate, uptime if applicable)
- Coverage of MVP acceptance criteria (percentage)

**Templates**

- QA Checklist (template)
    - Critical path works end-to-end
    - Permissions and access control verified
    - Audit log entries recorded for key actions
    - Data validation and error states covered
    - Performance smoke test completed
    - Security checks (basic) completed

---

### 7) Testing & validation

**Goal:** Validate usability, value, and feasibility; decide whether to iterate, pivot, or scale.

**Key activities**

- Usability testing with target personas.
- Pilot testing (if possible) in a controlled setting.
- Collect quantitative and qualitative feedback.
- Iterate based on findings.

**Deliverables (by end of stage)**

- [Test plan + participant list](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%207%20-%20Testing%20%26%20validation/Test%20plan%20%2B%20participant%20list.md)
- [Usability test notes + recordings/links](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%207%20-%20Testing%20%26%20validation/Usability%20test%20notes%20%2B%20recordings%20links.md)
- [Findings report (themes + severity)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%207%20-%20Testing%20%26%20validation/Findings%20report%20(themes%20%2B%20severity).md)
- [Prioritized fix list / iteration backlog](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%207%20-%20Testing%20%26%20validation/Prioritized%20fix%20list%20%2B%20iteration%20backlog.md)
- [Decision memo (ship / iterate / pivot)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%207%20-%20Testing%20%26%20validation/Decision%20memo%20(ship%20%2B%20iterate%20%2B%20pivot).md)

**KPIs**

- Task success rate (percentage)
- Time on task (median)
- System Usability Scale (SUS) or simple satisfaction score
- Net value signal: “Would you use this weekly?” (percentage yes)
- 

# critical issues found and resolved

**Templates**

- Usability Test Script (template)
    - **Scenario:**
    - **Tasks:**
        - Task 1:
        - Task 2:
    - **Success criteria:**
    - **Questions:**
        - What was confusing?
        - What did you expect to happen?
        - What would make this essential?

---

### 8) Launch readiness & handover

**Goal:** Package the work for release, adoption, and ongoing improvement.

**Key activities**

- Documentation, onboarding, and support readiness.
- Define monitoring and incident process.
- Plan next roadmap items.

**Deliverables (by end of stage)**

- [Launch checklist](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%208%20-%20Launch%20readiness%20%26%20handover/Launch%20checklist.md)
- [User documentation / onboarding guide](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%208%20-%20Launch%20readiness%20%26%20handover/User%20documentation%20%2B%20onboarding%20guide.md)
- [Operational plan (monitoring, support, incident response)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%208%20-%20Launch%20readiness%20%26%20handover/Operational%20plan%20(monitoring%2C%20support%2C%20incident%20response).md)
- [Roadmap v1 (next 4-8 weeks)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%208%20-%20Launch%20readiness%20%26%20handover/Roadmap%20v1%20(next%204-8%20weeks).md)
- [Post-launch metrics dashboard (definition)](MedCore%20Project%20Workflow%20(Stages%2C%20Deliverables%2C%20KP/Stage%208%20-%20Launch%20readiness%20%26%20handover/Post-launch%20metrics%20dashboard%20(definition).md)

**KPIs**

- Documentation completeness (checklist percentage)
- Support readiness (owners assigned + response times defined)
- Adoption metrics (active users, retention) once launched

**Templates**

- Launch Checklist (template)
    - Scope locked and signed off
    - Data privacy review completed
    - Security review completed
    - User onboarding materials ready
    - Monitoring/alerts configured
    - Rollback plan documented
    - Feedback channel defined

[Project setup & governance (Week 0)](MedCore%20Project%20Workflow%20(Stages,%20Deliverables,%20KP/Project%20setup%20%26%20governance%20(Week%200).md)

[Discovery: Research & data landscape (Stage 1)](MedCore%20Project%20Workflow%20(Stages,%20Deliverables,%20KP/Discovery%20Research%20%26%20data%20landscape%20(Stage%201).md)

[Empathize: User research (Stage 2)](MedCore%20Project%20Workflow%20(Stages,%20Deliverables,%20KP/Empathize%20User%20research%20(Stage%202).md)

[Define: Problem framing & requirements (Stage 3)](MedCore%20Project%20Workflow%20(Stages,%20Deliverables,%20KP/Define%20Problem%20framing%20%26%20requirements%20(Stage%203).md)

[Ideate: Solution design & prioritization (Stage 4)](MedCore%20Project%20Workflow%20(Stages,%20Deliverables,%20KP/Ideate%20Solution%20design%20%26%20prioritization%20(Stage%204).md)

[Plan & architecture (Stage 5)](MedCore%20Project%20Workflow%20(Stages,%20Deliverables,%20KP/Plan%20%26%20architecture%20(Stage%205).md)

[Prototyping / Build (MVP) (Stage 6)](MedCore%20Project%20Workflow%20(Stages,%20Deliverables,%20KP/Prototyping%20Build%20(MVP)%20(Stage%206).md)

[Testing & validation (Stage 7)](MedCore%20Project%20Workflow%20(Stages,%20Deliverables,%20KP/Testing%20%26%20validation%20(Stage%207).md)

[Launch readiness & handover (Stage 8)](MedCore%20Project%20Workflow%20(Stages,%20Deliverables,%20KP/Launch%20readiness%20%26%20handover%20(Stage%208).md)
