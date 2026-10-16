# Methodology Passport Card - Task 2

## 1. Project information

**Title:** The Impact of Generative AI on University Students' Learning Performance and Critical Thinking

**Author:** David Yakubov. Individual project. Course: Research Methods.

**Repository:** https://github.com/davidyakubov-glitch/genai-learning-study

**Status:** Prospective protocol and working measurement pipeline. The 10 sample rows are synthetic software-test fixtures. No real study has been conducted or results inferred from these rows.

**Continuity:** Based on the author's Task 1 submitted on 27 September 2026. The topic, three research questions and structured GenAI-versus-traditional comparison are preserved. Gain scores, numeric scales, guardrails and session details below are proposed Task 2 refinements, not previously observed results or claims of instructor approval.

## 2. Research type and design

Quantitative, controlled, two-group pilot experiment. Numeric learning outcomes, time and critical-thinking scores allow direct comparison between learning methods. Target: 40 consenting adult university volunteers, 20 per arm, subject to feasibility and required course/institutional approval. This is a pragmatic pilot target, not a power-derived sample size; lack of significance will not establish absence of an effect.

Measure initial knowledge using a 10-minute pre-test. Within lower/higher pre-test strata, allocate participants in shuffled pairs (one per arm; seed 20261017), with odd participants assigned to balance arm sizes. Keep the allocation record privately. Both groups receive the same 20-minute learning period and a maximum of 40 minutes for an equivalent academic practice task. Record elapsed practice-task time with the same timer procedure. A participant reaching 40 minutes is recorded at the limit; report how many reach the cap and interpret mean time as restricted to this window, not uncensored completion time.

The treatment group uses one chosen GenAI model and a fixed prompt protocol: request an explanation, verify claims against course material, identify weaknesses, and write an improved answer. The control group follows equivalent self-check steps using only the supplied course materials. No GenAI is permitted during either group's pre-test, post-test or critical-thinking assessment. Use a 15-minute post-test and 15-minute critical-thinking task. Freeze task wording, scoring keys and the model/version before recruitment; record the actual model label and date because online models may change.

## 3. Questions and hypotheses

Let G be post-test minus pre-test score (percentage points), T be recorded practice-task time (minutes, capped at 40), and C be critical-thinking score (0-20). D is the treatment mean minus control mean.

| Research question | Null hypothesis | Alternative hypothesis |
|---|---|---|
| RQ1: Does structured GenAI improve academic performance? | H0: D(G) = 0 | H1: D(G) != 0; expected direction positive |
| RQ2: Does structured GenAI reduce task time? | H0: D(T) = 0 | H1: D(T) != 0; expected direction negative |
| RQ3: Does structured GenAI improve critical thinking? | H0: D(C) = 0 | H1: D(C) != 0; expected direction positive |

Task 1 used raw post-test performance; Task 2 makes learning gain primary to explicitly account for starting knowledge. Raw post-test scores remain a reported supporting outcome. Two-sided alternatives permit detection of harm as well as benefit; an effect opposite to the expected direction would not support the anticipated benefit.

## 4. Variable matrix

| Type | Variable | Operational definition |
|---|---|---|
| Independent | Learning method | Structured GenAI versus traditional independent learning |
| Dependent, primary | Learning gain | Post-test minus pre-test; both scales 0-100 |
| Dependent, supporting | Raw academic performance | Post-test score, 0-100 |
| Dependent, secondary | Task time | Timer-based elapsed practice-task minutes; >0 to 40 |
| Dependent, secondary | Critical thinking | Four dimensions scored 0-5, total 0-20 |
| Controlled | Assessment and learning conditions | Same topic, task difficulty, instructions, materials, learning period, time limits and scoring keys |
| Controlled / balanced | Prior knowledge | Same pre-test, stratified allocation; report baseline means |
| Controlled | Technology and grading | Same device class/network conditions; fixed AI protocol/model in treatment; blinded grading |

Critical-thinking dimensions: evidence verification, identification of assumptions/errors, quality of reasoning, and justified revision/conclusion. Each dimension: 0 absent; 1 unsupported assertion; 2 partially relevant but major gaps; 3 mostly correct with some evidence; 4 well-supported with a minor gap; 5 accurate, explicit and well-justified. Two blinded raters score independently; average their total scores and document disagreements before unblinding. This is a project rubric, not a validated psychometric instrument.

## 5. Metrics, guardrails and baseline

**Primary metric:** Difference in mean learning gain, in percentage points, between GenAI and traditional groups. A positive value indicates a descriptive advantage, not proof of causation or significance by itself.

**Secondary metrics:** Difference in mean task time (negative is faster) and critical-thinking score (positive is higher). Also report group sizes, pre-test and post-test means, and number of time-capped tasks.

**Guardrails:** (1) Critical-thinking mean must not be more than 1 point lower in the GenAI arm (D(C) >= -1, on the 0-20 scale). The one-point margin is a proposed project tolerance, not a published standard; passing a sample mean check is not statistical proof of non-inferiority. (2) Zero duplicate IDs, missing required values, out-of-range scores or non-finite values in the analysis input. (3) Zero use of AI during outcome assessments; record protocol deviations privately and report their counts. The script checks numeric/data guardrails only; it cannot verify participant adherence.

**Baseline:** Traditional independent learning with the same supplied learning materials, task and self-check prompts, but no generative AI. Equal learning opportunity and blinded common assessment make this a fair comparison. The contrast estimates the effect of this structured GenAI package, not every possible AI use.

## 6. Measurement pipeline and analysis plan

The executable `src/benchmark.py` loads `configs/config.json`, validates CSV records and writes a JSON summary and run log. It consumes manually collected/scored participant measurements. The sample confirms that this processing path works; it does not recruit participants, administer assessments or call a model API.

For real data, preserve raw records privately. Resolve data-entry errors against source records; never invent missing measurements. Report participant flow, withdrawals, missing outcomes and protocol deviations by arm. The current runner fails on missing values; a complete-case analysis would require a documented de-identified export and explicit reporting of exclusions and possible attrition bias.

Before inspecting real outcomes, finalize assessment materials and the analysis plan. For the real pilot, report group estimates, treatment-minus-control differences and uncertainty intervals; use a two-sided primary comparison at alpha 0.05, with appropriate checks of assumptions. The two secondary questions are exploratory; any formal secondary tests should use Holm correction. The present Task 2 skeleton implements descriptive metrics only, so inferential tests and confidence intervals remain work for the analysis phase. Do not interpret smoke-test differences as evidence for the hypotheses.

## 7. Reproducibility, privacy and remaining preparation

Python 3.12.14; no third-party Python dependencies. Configuration, synthetic sample and executable runner are versioned. Store only pseudonymous IDs in analysis files and keep real data/consent documents outside the public repository. Participation must be voluntary with informed consent and any required institutional approval; no recruitment or data collection has occurred as part of this deliverable.

Before Week 7: finalize the concrete course topic, pre/post test forms, answer key, critical-thinking task, model/version and participant procedure; confirm the feasibility/approval of the pilot; freeze configuration and commit the protocol before collection. These are remaining study-preparation actions, not completed experimental results.

## 8. Basis

Yakubov, David (2026). Task 1: Research Proposal, Zotero Base & Literature Synthesis. Submitted to Research Methods on 27 September 2026. The present card operationalizes that submitted proposal; it does not add unverified literature claims.
