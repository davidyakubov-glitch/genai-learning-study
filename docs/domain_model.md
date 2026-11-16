# AI domain model: structured GenAI-assisted learning

This is an educational intervention model, not a trained language model. No LLM is fitted or called in this demonstration. The formal loss below describes a simple group-mean model of learning gain; it is not a claim that the study trains an AI system.

## Variables and notation

| Symbol | Definition | Unit / domain |
|---|---|---|
| i | Synthetic record index (future study: participant) | 1,...,N |
| N, n_a | Total count, count in arm a | 10 total; 5 per arm in the fixture |
| a_i | Method assignment | 0 = traditional, 1 = structured GenAI |
| x_i, y_i | Pre-test and post-test | points, 0–100 |
| g_i | Learning gain, y_i - x_i | percentage points |
| t_i | Recorded practice-task time | minutes, 0 < t_i <= 40 |
| c_i | Critical-thinking rubric total | points, 0–20 |
| theta_a | Predicted mean gain in arm a | percentage points |
| L | Mean squared prediction loss | squared percentage points |
| m | Any reported outcome g, t, or c | respective outcome unit |
| bar m_a | Sample mean of m in arm a | respective outcome unit |
| D_m | GenAI minus traditional sample mean | respective outcome unit |
| s_(m,a) | Sample standard deviation | respective outcome unit |
| delta_m | Population mean difference for a future real study | respective outcome unit |

## Formal definitions

$$g_i=y_i-x_i, \qquad \widehat g_i=\theta_{a_i}.$$

$$L(\theta_0,\theta_1)=\frac{1}{N}\sum_{i=1}^{N}(g_i-\theta_{a_i})^2.$$

Minimizing this loss gives the group means, $\widehat\theta_a=\overline g_a$.
The analysis computes these means directly; numerical optimization is unnecessary.

$$\overline m_a=\frac{1}{n_a}\sum_{i:a_i=a}m_i,\qquad D_m=\overline m_1-\overline m_0.$$

$$s_{m,a}=\sqrt{\frac{\sum_{i:a_i=a}(m_i-\overline m_a)^2}{n_a-1}}.$$

Primary target: $D_g$. Secondary descriptive targets: $D_t$ and $D_c$.
Positive $D_g$ is higher gain; negative $D_t$ is less recorded time.
Pre-test and raw post-test means remain supporting measures.

The Task 2 critical-thinking guardrail is $D_c\geq-1$ point. It is only a descriptive sample check, not a non-inferiority test. The code also rejects invalid measurements and duplicates; no-AI assessment adherence cannot be verified from these numbers.

For a future real study, retain two-sided hypotheses $H_0:\delta_m=0$ and $H_1:\delta_m\ne0$. The expected directions are positive for gain and critical thinking, negative for time. No hypothesis tests are conducted on this synthetic fixture. Equal conditions and blinded no-AI assessment remain requirements of the planned protocol, not procedures performed here.
