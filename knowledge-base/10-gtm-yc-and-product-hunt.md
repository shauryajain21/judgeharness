# 10 — GTM: YC + Product Hunt

Two motions, one product. YC = the pitch. Product Hunt = the launch of Layer 1.

## YC positioning

- **One-liner (≤50 chars):** *We red-team the AI graders that train other AI.*
- **Buyer:** RL/post-training + eval teams at labs and RL-infra vendors — they
  build graders and must prove they aren't gameable.
- **Traction plan (the highest-leverage move):** ship the OSS CLI, run it against
  3–5 real reward models (ideally YC RL cos — HUD, Osmosis, Refresh, Idler), and
  find real exploits. *"We found 14 ways to farm reward without solving the task"*
  is the whole application in one sentence.
- **Durability answer:** gets *more* valuable as models improve — better models
  game graders better, and there are more graders to certify.

### Application field drafts

| Field | Answer |
|---|---|
| What you make | Independent tool that stress-tests a customer's reward model / LLM-judge, finds how it can be reward-hacked, and certifies reliability. OSS CLI → hosted platform. |
| Why you | A reward model is a judge, and judges are provably broken. Reward hacking is often detectable *inside* the model before the score shows it — black-box tools can't see that. |
| What's new | We audit the grader, not the output. Detection is mechanistic, not diffing. |
| Competitors | Braintrust / Confident AI / Openlayer grade outputs, assume the grader is trustworthy. HUD / Osmosis *build* graders → they're customers. Nobody certifies the grader. |
| Money | OSS free → per-cert / per-model / seat, + enterprise continuous-certification contracts. |

## Product Hunt (launch Layer 1, not the platform)

B2B infra flops on PH; free visual micro-tools win. Launch **"Is Your LLM Judge
Biased?"** — the free grader with a shareable score.

- **Tagline (`X for Y`, ≤60 chars):** *Snyk for AI evals — scan your judge for
  bias & gaming.* (alt: "Catch reward hacking in your AI judge in 30 seconds.")
- **Stack the launch:** free grader (hero) + `npx gradecheck` (dev cred, cross-post
  to HN + Dev Hunt) + a public **Reward-Hacking Leaderboard** (ongoing PR engine).
- **Gate the platform** behind the free score (HubSpot Website Grader / Snyk motion).

### Launch mechanics (condensed)

- First gallery asset = a 30s **animated "watch it fool your judge" demo**. Motion + a number beats screenshots.
- 12:01 AM PT, Tue–Thu (or Sun for the badge with less competition).
- Maker's **first comment** matters most (+166% upvotes): problem story → fix → one question. Not a feature list.
- **Velocity > volume:** ~45–55 upvotes/hr from a *warm* community; 100+ before 4 AM PT → 82% chance top-10. Don't dump a cold list (new accounts shadow-filtered).
- One person on comments all day (89% of top-5 makers).

## Why the channels converge

The free grader is PH virality **and** YC traction **and** design-partner bait
**and** the moat's data flywheel — one artifact, every channel. See `09`.
