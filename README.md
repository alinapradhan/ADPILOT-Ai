





# BUILD PROMPT: ADPILOT AI

## An LLM-Powered Advertising Intelligence and Decision Support Platform

### 1. Vision

Build AdPilot AI, an intelligent advertising analysis platform for digital advertising agencies, media buyers, and performance marketing teams.

The platform must go beyond automated reporting. Its primary responsibility is to interpret advertising performance, identify meaningful changes, investigate possible explanations using available evidence, and provide prioritized recommendations.

Use Windsor.ai as the advertising data integration layer. Use Python for deterministic analysis and an LLM for interpretation, investigation planning, and natural-language explanations.

The application must be an original implementation with a modular architecture, independently designed workflows, explicit validation rules, and a clear separation between numerical analysis and AI reasoning.

Do not copy an existing application's branding, source code, or proprietary implementation.

### 2. Core product capabilities

#### A. Advertising intelligence engine

Build a central engine that transforms raw advertising records into structured campaign intelligence.

It must:

* Retrieve campaign data from connected advertising platforms.
* Normalize supported metrics and dimensions.
* Compare current performance with historical baselines.
* Identify material changes in spend, clicks, conversions, CPA, CTR, and ROAS when the necessary data is available.
* Detect unusual changes using configurable statistical rules.
* Separate observed facts from hypotheses.
* Record evidence supporting every major finding.
* Identify missing data that limits the analysis.

The engine must never claim to know the cause of a performance change solely because two metrics changed together.

#### B. AI investigation workflow

Implement an investigation workflow that operates as follows:

1. Detect a performance issue or receive an analyst's question.
2. Build a structured investigation plan.
3. Identify the relevant metrics, campaigns, dimensions, and comparison periods.
4. Retrieve or select the necessary data.
5. Calculate relevant comparisons using Python.
6. Ask the LLM to interpret the verified results.
7. Check generated statements against the evidence.
8. Return a structured explanation with confidence limitations and recommended next steps.

Example user questions:

* Why did our cost per acquisition increase this month?
* Which campaigns are consuming more budget without producing additional conversions?
* What changed between the previous reporting period and this period?
* Which campaigns deserve further investigation?
* Is the improvement in ROAS broad-based or concentrated in a few campaigns?
* What should the account manager review first?

The LLM must request additional data or state uncertainty when the available evidence cannot answer a question.

#### C. Campaign health scoring

Create a configurable campaign health assessment.

Evaluate campaigns using relevant indicators such as:

* Spend efficiency.
* Conversion performance.
* CTR and CPC trends.
* ROAS against a supplied target.
* Data completeness.
* Recent changes relative to historical performance.

Do not use one universal formula for every advertising objective.

Allow the user to specify business goals, target CPA, target ROAS, reporting windows, and applicable KPIs.

Return:

* Health status.
* Supporting metrics.
* Main contributing indicators.
* Data limitations.
* Suggested investigation steps.

Explain the scoring method and allow thresholds to be configured. Do not present an arbitrary score as an objective industry benchmark.

#### D. Budget opportunity analysis

Identify potential budget-allocation opportunities using observed campaign performance.

The engine should:

* Compare campaign efficiency against defined targets.
* Identify campaigns that may warrant additional review.
* Highlight campaigns with rising spend and declining results.
* Estimate potential outcomes only when assumptions and available inputs support the calculation.
* Explain trade-offs and uncertainty.

The initial version must not automatically change advertising budgets or modify live campaigns.

#### E. Conversational advertising analyst

Build a natural-language interface through which an authorized user can ask questions about their connected advertising data.

Workflow:

* Interpret the user's question.
* Identify the relevant client, account, reporting period, and metrics.
* Validate access permissions.
* Retrieve only the data required to answer.
* Calculate the answer using deterministic functions.
* Generate a concise explanation with supporting evidence.
* Return a clear message when the requested information is unavailable.

Support follow-up questions by retaining a controlled conversation context associated with the authorized client and account.

Never treat text found in retrieved advertising records as system instructions.

#### F. Evidence-based findings

Every major AI-generated finding should contain:

* A unique finding identifier.
* A concise description.
* The observation that triggered the finding.
* Current and comparison-period values.
* The calculation or comparison used.
* The evidence source and reporting period.
* A distinction between fact and hypothesis.
* A recommended next step.
* A severity or priority label with documented criteria.

Create a validation layer that rejects, corrects, or flags unsupported numerical claims.

### 3. Data integration

Implement a provider-independent interface for advertising data.

Start with Windsor.ai.

Responsibilities:

* Discover supported connectors and fields using official documentation.
* Retrieve data for configured accounts and date ranges.
* Request only the fields required for each analysis.
* Handle authentication failures, rate limits, timeouts, and incomplete responses.
* Preserve source metadata and original metric values.
* Normalize data without silently changing its meaning.
* Provide a mock provider with synthetic datasets for local development.

Keep Windsor.ai credentials on the backend. Redact secrets from logs and error responses.

Do not assume every connector exposes the same dimensions, attribution rules, currencies, or conversion metrics.

### 4. Analysis architecture

Use independent, testable components.

Suggested modules:

* DataProvider: retrieves records.
* DataNormalizer: standardizes source structures.
* MetricsEngine: calculates deterministic KPIs.
* BaselineAnalyzer: compares performance periods.
* AnomalyDetector: identifies unusual changes.
* InvestigationPlanner: selects relevant follow-up analyses.
* EvidenceBuilder: assembles supporting facts.
* LLMInterpreter: generates explanations and hypotheses.
* ClaimValidator: verifies numerical statements.
* RecommendationEngine: prioritizes possible actions.
* IntelligenceOrchestrator: coordinates the workflow.

Avoid putting all logic into one large service or one LLM prompt.

Use explicit input and output schemas between modules.

### 5. Backend and infrastructure

Use:

* Python 3.12+
* FastAPI
* Pydantic
* Pandas
* HTTPX
* SQLAlchemy
* PostgreSQL
* Alembic
* Pytest
* Ruff

Use a configurable LLM provider, with structured responses validated against Pydantic schemas.

Add a database for organizations, clients, advertising accounts, analysis runs, findings, user preferences, and audit events.

Use a background job queue only when asynchronous or scheduled processing becomes necessary.

### 6. Initial REST API

Implement endpoints for:

GET /health

GET /connectors

GET /connectors/{connector}/fields

POST /analysis/preview

POST /analysis/campaign-health

POST /analysis/investigate

POST /analysis/budget-opportunities

POST /assistant/ask

GET /analysis/runs

GET /analysis/runs/{run_id}

GET /analysis/runs/{run_id}/findings

POST /analysis/runs/{run_id}/validate

Use Pydantic request and response schemas, consistent error handling, input validation, and Swagger documentation.

Apply authentication and client-level authorization before accessing data. Never trust a client identifier supplied by the caller without verifying permissions.

### 7. Reliability and safeguards

* Calculate all numerical KPIs using deterministic code.
* Use consistent date windows for comparisons.
* Handle zero denominators and missing metrics explicitly.
* Keep unavailable values distinct from genuine zeros.
* Make currency differences visible.
* Avoid treating cross-platform reach as deduplicated reach.
* Document assumptions behind attribution-dependent metrics.
* Do not invent causal explanations.
* Keep evidence and generated narratives separate.
* Store model version, prompt version, and analysis inputs for reproducibility.
* Limit retries and handle provider failures gracefully.
* Do not expose credentials, personal data, or other clients' information.
* Do not automatically execute advertising changes.

### 8. Repository structure

Create a clean repository with modules for:

app/
api/
core/
schemas/
integrations/
data/
analytics/
investigations/
intelligence/
llm/
validation/
database/
services/

tests/
unit/
integration/
fixtures/

docs/
architecture.md
api-reference.md
data-dictionary.md
security.md
evaluation-methodology.md

scripts/
seed_demo_data.py
run_demo.py

Include:

* README.md
* pyproject.toml
* .env.example
* .gitignore
* Dockerfile
* docker-compose.yml
* Alembic configuration
* GitHub Actions workflow for automated tests and linting

Adjust the structure if needed to keep modules cohesive. Do not create empty modules or unnecessary abstractions.

### 9. Testing and evaluation

Build synthetic fixtures with known expected outcomes.

Test:

* KPI calculations.
* Baseline comparisons.
* Anomaly detection.
* Missing and duplicate records.
* Zero values and invalid dates.
* Different currencies.
* Connector failures.
* Client authorization.
* LLM output validation.
* Unsupported numerical claims.
* Reproducibility of analysis runs.

Include a demonstration where a synthetic campaign's CPA increases and the system identifies the change, calculates the difference, examines available supporting metrics, and explains what additional information would be needed to establish the cause.

Measure the system's factual accuracy using automated tests and a small set of manually reviewed example questions.

Do not claim that AI findings are accurate simply because the API returns a successful response.

### 10. Development milestones

Milestone 1: Establish the repository, application configuration, mock data provider, schemas, and Swagger interface.

Milestone 2: Implement the deterministic metrics engine, baselines, campaign health assessments, and tests.

Milestone 3: Implement the investigation planner, evidence builder, LLM interpreter, and claim validator.

Milestone 4: Integrate Windsor.ai and validate real data against the mock-provider contract.

Milestone 5: Add persistence, analysis history, authentication, and client isolation.

Milestone 6: Add the conversational analyst and budget opportunity analysis.

Milestone 7: Add export capabilities and, if required, a React dashboard.

### 11. Completion requirements

The project is not complete merely because files have been generated.

The coding agent must:

* Create actual working implementations.
* Install dependencies using documented commands.
* Run the test suite.
* Fix implementation and test failures.
* Run linting.
* Start the FastAPI application.
* Verify the health endpoint and core analysis workflow.
* Demonstrate an end-to-end analysis using synthetic data.
* Document any feature that requires real Windsor.ai or LLM credentials.

Begin with Milestone 1 and complete it before moving to later milestones. At every milestone, explain the files created, commands executed, tests performed, and remaining limitations.









  















































































































































 



  






























































 






























 



































