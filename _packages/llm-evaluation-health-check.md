---
# One consulting package = one file. This file becomes the page
# /services/llm-evaluation-health-check/ and feeds the homepage and /services/.
# Set `published: false` to hide the package everywhere.
published: true
featured: true
order: 1
anchor: health-check
enquiry: health_check   # key under `enquiries` in _data/profile.yml

title: LLM Evaluation Health Check
description: >-
  A fixed-price evaluation of one RAG or agent workflow by Samira Korani:
  agreed test cases, baseline results, failure analysis and prioritised fixes
  in about five working days. EUR 2,950.
tagline: Find out where one RAG or agent workflow fails, why, and what to fix first.

fee: EUR 2,950
fee_note: Fixed project fee
price_eur: 2950
duration: About 5 working days
duration_note: After access and scope are agreed
scope_short: One RAG or agent workflow, up to 50 test cases

for: >-
  Engineering teams with a RAG or agent feature in production, or close to
  release, who are seeing answers they can't fully trust, or who need evidence
  before a model change, a launch or a customer's due-diligence questions.
audience:
  - Startups and mid-sized businesses shipping AI features to customers, wherever they are based
  - Fintech and insurtech teams, where answers must stay grounded in policy, product or regulatory documents
  - Teams about to change model, prompts or retrieval, who want a baseline first

problem: >-
  When outputs are unreliable, it is rarely obvious whether the cause is
  retrieval, context assembly, prompting, the model or the source data.
  Without a baseline, every fix is a guess and every model or prompt change is
  a risk you can't measure.

approach_title: What I assess
approach:
  - Correctness and groundedness of answers against agreed expectations
  - The failure modes that matter for your workflow, such as missed retrieval, unsupported claims, wrong tool calls or prompt sensitivity
  - Latency and cost, where the necessary measurements are available

deliverables:
  - Agreed evaluation cases (up to 50), written with your team
  - Baseline results across the agreed measures
  - A failure analysis showing where and why the workflow fails
  - Prioritised fixes, ordered by likely impact and effort
  - A 60-minute handover with your team

scope:
  - One existing RAG or agent workflow
  - One agreed evaluation environment
  - Up to 50 representative test cases

limits: >-
  Fifty well-chosen cases can expose systematic failures, but they are a
  sample. The results describe how the workflow behaved on those cases; they
  are not a statistical guarantee of behaviour in production. The Health Check
  is not a security audit or certification. Implementing fixes is scoped
  separately.

process:
  - title: Discovery
    text: A short call about the workflow, what's going wrong and what a useful result would look like. If the Health Check isn't the right fit, I'll say so.
  - title: Agreed scope
    text: A written scope and fixed-fee quotation covering the workflow, the environment, the test cases, access and timing.
  - title: Assessment
    text: Once access is in place, I build the evaluation cases with your team, run the baseline and analyse the failures.
  - title: Handover
    text: A 60-minute session to walk through the results and priorities. You keep the evaluation cases and the report.

faq:
  - q: What do you need from us?
    a: >-
      Access to the workflow in one agreed environment (often staging), a set
      of real or realistic questions or tasks, any examples of bad outputs you
      have already seen, and a technical contact who can answer questions
      during the week.
  - q: Are 50 test cases enough?
    a: >-
      Enough to find systematic failures and decide what to fix first, if the
      cases are chosen well. Not enough to make statistical claims about
      production behaviour, and I won't present the results as if they were.
      The cases are yours to extend afterwards.
  - q: Do you also fix what you find?
    a: >-
      The Health Check ends with prioritised fixes and a handover. If you'd
      like help implementing them, I'll scope that separately, so you can
      decide with the results in hand.
  - q: Does it depend on our framework or model provider?
    a: >-
      No. The Health Check evaluates your workflow as it runs, so it works
      with whatever framework, model provider and vector store you use.
  - q: How do you handle confidential data?
    a: >-
      Access, data handling and confidentiality terms are agreed in writing
      as part of the scope, before any work starts. I only ask for the access
      the agreed work needs.

next_step: >-
  Send me a few lines about the workflow and what's going wrong. I'll reply to
  arrange a short discovery call and confirm whether the Health Check is the
  right fit.
---
