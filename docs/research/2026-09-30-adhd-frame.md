---
title: "Work framing for ADHD — plan card, appetite stop, resumption line, acceptance card"
category: research
status: proposed
created: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-09-30
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-30"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, adhd, accessibility, planning, workflow]
---

# Work framing for ADHD — the evidence behind package 1

## Result first

1. **Write the frame down where the work happens.** Time and the next step
   are weak points in ADHD; the practical answer is to externalise them at the
   point of performance. Evidence: meta-analysis for the time deficit, expert
   guidance for the remedy (2.1).
2. **An appetite is a stop, not an estimate.** Shape Up is the source; it is
   practitioner guidance, and no ADHD study of it was found (2.2).
3. **Read the clock; do not trust the feeling.** Time perception in ADHD is
   off by a medium effect, and developers misjudge their own speed even
   without ADHD (2.1, 2.2).
4. **A pre-mortem line finds more risks, not better ones.** The famous
   "30 %" measured the *number* of reasons generated, not their quality or
   any project outcome (2.3).
5. **End every stop with one resumption action.** Programmers rarely resume
   within a minute and rebuild context from notes and cues; if-then plans
   have large effects in clinical groups, but the ADHD samples were mostly
   children (2.5, 2.6).

None of the sources tests this frame on adults with ADHD using coding
agents. Every element is a reversible default, not a treatment.

## 1 · Question and scope

What does current evidence say about framing work for a person with ADHD,
for the five pieces proposed as package 1 of the Coding Harness foundation:
a plan card with a one-line pre-mortem, an appetite stop, the clock in the
"done:" line, a resumption line, and an acceptance card?

The proposal and its first evidence table come from the LakeSwitch journal
`journal/2026-09-28-product-start-and-principles.md` (lakeswitch-ai at
`09c9d62`, sections "Working well with ADHD" and "Three more lenses on the
frame"). This note re-reads the sources that carry the five pieces, adds
sources on appetite, pre-mortem, done criteria, resumption and externalised
working memory, and marks what it did not read.

It builds on two notes in this directory and does not repeat them:

- [Human planning and harness gaps](2026-09-18-human-planning-and-harness-gaps.md)
  (2026-09-18): a start page, attention and interruption defaults, W3C
  focus guidance.
- [Decision pull requests](2026-09-30-decision-pull-requests.md), §2.4
  (2026-09-30): W3C COGA, GOV.UK, AR 25-50 and NN/g on writing for readers
  with ADHD. Section 2.8 below applies those sources to the cards.

## 2 · Findings

### 2.1 Externalise time and working memory

- **The remedy's rationale.** Barkley: if regulating behaviour by internally
  represented information is impaired, people "will be best assisted by
  'externalizing' those forms of information", with physical representations
  "in the setting at the point of performance" — "that place and time in the
  natural setting of the person's life where they are failing to use what
  they know" ([barkley], expert fact sheet, undated, based on his 2012 book;
  read 2026-09-30). Strength: expert theory and guidance, not a trial of a
  specific aid.
- **The time deficit is real and medium-sized.** A meta-analysis of 824
  effect sizes across the lifespan found a mean g of 0.688, moderated by age
  and working memory; the working-memory link held only below 18
  ([metcalfe], meta-analysis, *Developmental Neuropsychology* 2024; abstract
  read 2026-09-30). An earlier meta-analysis found time estimation deficits
  of small-to-medium size over 8 studies ([marx], *JAACAP* 2021; read
  through the ADHD Evidence Project's summary of 2022-03-21, not the paper).
- **For adults the picture is thinner.** A review of a decade of adult
  studies calls them "very scarce" and the results mixed ([mette], review,
  *IJERPH* 2023-02-10; abstract read 2026-09-30).
- **Software engineers with ADHD name it themselves.** Nineteen interviews
  yielded 15 challenges, among them task organisation and estimation, and 12
  strategies, among them to-do lists ([liebel], qualitative case study,
  arXiv 2312.05029, 2023-12-08; read 2026-09-30).

Consequence for the frame: the card and the stop are the external
representation; the appetite replaces an estimate the person is measurably
worse at; the clock is read with `date`, not recalled.

### 2.2 Appetite and time-boxing

- **Appetite.** "The amount of time we want to spend on a project, as
  opposed to an estimate." "Estimates start with a design and end with a
  number. Appetites start with a number and end with a design."
  ([shapeup-3], Singer, *Shape Up*, ch. 3; read 2026-09-30; the page shows no
  date, the book is from 2019).
- **Circuit breaker.** "If they don't finish, by default the project doesn't
  get an extension." ([shapeup-8], ch. 8; read 2026-09-30.)
- **Deciding when to stop.** "Compare down to baseline"; "Scope grows
  naturally"; scope is "hammered" to fit the time box; "The fixed deadline
  motivates us to ask these questions. Variable scope enables us to act on
  them." ([shapeup-14], ch. 14; read 2026-09-30.)
- **The feeling of speed misleads.** In a randomised trial with 16
  experienced developers and 246 issues, AI tools made them 19 % slower,
  while they still believed afterwards that they had been sped up by 20 %
  ([metr], METR, 2025-07-10; read 2026-09-30). No ADHD angle; it supports
  reading the clock over the impression.

Strength: practitioner method (Shape Up), one RCT on perception (METR). No
source tests an appetite for people with ADHD. The four answers at the stop
(continue, cut, park, drop) combine the circuit breaker with scope hammering;
"drop" as a legitimate answer is Stage-Gate's "kill" (Cooper), which
`docs/WORKFLOW.md` already cites.

### 2.3 Pre-mortem

- **Procedure.** Team members "assume that the project they are planning has
  just failed" and generate plausible reasons ([klein], Klein, *HBR*,
  2007-09; the page's summary read 2026-09-30, the full article is behind a
  paywall and was not read).
- **The evidence behind it.** Mitchell, Russo and Pennington (1989): imagining
  an event as having happened raised the number of reasons generated by
  about 30 % ([mitchell], *J. Behavioral Decision Making* 2(1), 25–38; the
  paper returned HTTP 403 and was **not read**; figure confirmed through
  [collins], a teaching note read 2026-09-30).
- **The caveat.** The same note: they "did not assess the quality of the
  reasons". The popular phrasing "increases the ability to *correctly*
  identify reasons … by 30 %" overstates the study.

Consequence: one line ("suppose it failed: most likely why?") is cheap and
adds risks to the card; it is not evidence of better outcomes. No ADHD
study was found.

### 2.4 Done criteria, and a light "ready"

- **Definition of Done.** "A formal description of the state of the
  Increment when it meets the quality measures required"; an item that does
  not meet it "cannot be released or even presented"
  ([scrum], Scrum Guide 2020, November 2020; read 2026-09-30). Strength:
  practice standard.
- **Definition of Ready as guidance, not a gate.** Rules that require work
  to be finished before it may start become "a huge step towards a
  sequential, stage-gate approach"; "Favor guidelines rather than rules"
  ([cohn], Mountain Goat Software, updated 2023-06-28; read 2026-09-30).
  Strength: practitioner.

Consequence: `done: <evidence> · <time used> of <appetite>` names the
evidence, not a feeling; the card's ready points stay prose, never a gate.

### 2.5 Resumption cues and interruption recovery

- **Resuming is slow and cue-driven.** From 10,000 recorded sessions of 86
  programmers and a survey of 414: "only 10% of the sessions have
  programming activity resume in less than 1 min after an interruption";
  in about 30 % the first edit came after more than 30 minutes; programmers
  keep notes and leave "roadblock cues, such as compile errors" to force a
  reminder ([parnin], Parnin and Rugaber, *Software Quality Journal* 19,
  2011; PDF read 2026-09-30). Strength: large observational study plus
  survey; no ADHD focus.
- **Interruptions cost stress, not only time.** Interrupted people finished
  faster with no loss in quality, "but this comes at a price: experiencing
  more stress, higher frustration, time pressure and effort" ([mark], Mark,
  Gudith and Klocke, CHI 2008; PDF read 2026-09-30). Strength: experiment.
- **Memory for goals.** Altmann and Trafton (2002) model resumption as
  re-activating a suspended goal, helped by cues ([altmann], *Cognitive
  Science* 26; only a search summary was seen, the paper was **not read**).
- **Automated cues against notes alone.** Parnin and DeLine (CHI 2010)
  reportedly found a doubled success rate with automated cues
  ([parnin-deline]; HTTP 403 and 404, **not read**; not used for a claim).

Consequence: a stop ends with one line that names the first action and where
to start it — the written cue that makes resumption cheap. The "Hemingway
trick" (stop at a known next step) is practitioner lore; not read.

### 2.6 If-then plans and closing open loops

- **If-then plans work, with large effects in clinical samples.** Excluding
  one outlier: d+ = 0.99, k = 28, N = 1,636, across mental-health problems
  and goals ([toli], Toli, Webb and Hardy, *Br. J. Clinical Psychology* 55,
  2016; accepted manuscript read 2026-09-30). The ADHD samples in it are
  mainly children (Gawrilow and colleagues); one included record is a
  dissertation with ADHD adults. Strength: meta-analysis; for adults with
  ADHD, thin.
- **The general effect.** Gollwitzer and Sheeran (2006) report d = 0.65 over
  94 tests ([gollwitzer]; seen only through a search summary, the abstract
  page did not show the numbers; **not read**).
- **A plan quiets an unfinished goal.** Unfinished goals caused intrusive
  thoughts and poorer performance on other tasks; "allowing participants to
  formulate specific plans for their unfulfilled goals eliminated the
  various activation and interference effects" ([masicampo], Masicampo and
  Baumeister, *JPSP*, 2011-06-20; PDF read 2026-09-30). Strength: several
  experiments; no ADHD sample.

Consequence: the resumption line in if-then form (`when I start, I will
<one action>`) and the not-now list with a named place both close loops
the person would otherwise carry in working memory.

### 2.7 Planning skills in adult ADHD, and a written scope for the agent

- **Adults with ADHD benefit from taught time management and planning.** In
  an RCT with 88 adults, meta-cognitive group therapy (time management,
  organisation, planning) beat supportive therapy, odds ratio 5.41
  ([solanto], *Am. J. Psychiatry* 2010; seen through search results only,
  **not read**). Strength: RCT of a therapy; applying it to work packages is
  an analogy.
- **A written scope also constrains the agent.** On Claude Code, removing the
  scope ("consent") declaration from the prompt raised out-of-scope actions
  from 0.0 % to 17.1 % on paired scenarios; the ask-to-continue framework
  (OpenHands) ran at 0.2–4.5 % against 5.4–27.7 % for the permissive
  cluster ([qu], Qu et al., arXiv 2605.18583, 2026-05-18; abstract read
  2026-09-30). The second figure compares frameworks; it is not an
  intervention. Strength: preprint.

Consequence: the card's scope and not-now lines serve two readers — the
person, and the agent that would otherwise widen the change.

### 2.8 Writing the cards for the reader

The sources gathered in [Decision pull requests §2.4](2026-09-30-decision-pull-requests.md#24-cognitive-accessibility-and-adhd)
apply unchanged; the relevant patterns are:

| Card | Pattern | Source there |
|---|---|---|
| plan card, at most five lines | five or fewer main choices; important information first | W3C COGA 4.6.3 |
| every card | purpose clear at a glance, for someone coming back after a distraction | COGA 4.2.1 |
| resumption line | do not rely on memory: the step carries what is needed to act | COGA 4.7.5 |
| acceptance card, "what could break" | state the results and disadvantages, especially where an action cannot be undone | COGA 4.8.3 |
| all | main point first; readable in one rapid reading | AR 25-50 para 1-38; NN/g inverted pyramid; GOV.UK |

The same note found that 45.4 % of mismatched agent PR descriptions claimed
changes never made (Gong et al., preprint, 2026-01). The acceptance card's
"how it was checked" names a command, its result and the commit, which is
the check against that failure.

## 3 · What each proposed piece rests on

| Piece | Rests on | Strength | Caveat |
|---|---|---|---|
| plan card (effect, done, appetite, not-now, pre-mortem) | Barkley; COGA 4.6.3; Qu et al.; Scrum DoD | guidance; preprint; practice | no outcome study for adults with ADHD |
| one-line pre-mortem | Mitchell et al. 1989; Klein 2007 | lab study; practitioner | more reasons, not better ones |
| appetite stop (continue · cut · park · drop) | Shape Up ch. 3, 8, 14; Stage-Gate "kill" | practitioner | no ADHD evidence found |
| the clock in "done:" | Metcalfe 2024; METR 2025; Scrum DoD | meta-analysis; RCT; practice | the adult evidence is scarce and mixed (Mette 2023) |
| resumption line | Parnin and Rugaber 2011; Toli 2016; Masicampo and Baumeister 2011 | observational; meta-analysis; experiments | ADHD samples mostly children |
| acceptance card | COGA 4.8.3; decision-PR research §2.3 | W3C Note; preprint | — |

## 4 · What to avoid

Carried from the LakeSwitch journal of 2026-09-28 ("Anti-patterns",
"What would make it worse", "Hyperfocus"), where each has its source; not
re-read here:

- confirming everything, long reports, large diffs, many parallel threads;
- believing the agent's "done" without evidence;
- repeated nudges, counters, streaks, gamification, forced breaks; the agent
  speaks once per appetite;
- estimation rituals and fixed ceremonies;
- turning a rule into a check before it has been broken twice.

## 5 · Evidence that is missing

- Outcome studies of adults with ADHD working with coding agents.
- Any test of appetites, pre-mortems or resumption lines with ADHD samples.
- Session length and breaks for adults with ADHD; the 90-minute checkpoint
  and similar numbers are heuristics.
- Whether a visible clock helps adults with ADHD, as opposed to children.

## 6 · Not read or not verified

- Mitchell, Russo and Pennington (1989): HTTP 403; the 30 % figure and the
  quantity-not-quality caveat come from [collins].
- Klein (2007), full text: paywalled; only the summary page was read.
- Gollwitzer and Sheeran (2006): numbers seen in a search summary only.
- Altmann and Trafton (2002): search summary only.
- Parnin and DeLine (2010): HTTP 403 at the ACM, 404 at the author's site.
- Solanto et al. (2010): search results only.
- Marx et al. (2021): read through a summary, not the paper.
- `PMC9962130`, cited in the LakeSwitch journal for "g≈0.69", is the adult
  review [mette] (no pooled effect size); the 0.688 comes from [metcalfe].
  The journal's attribution is corrected here.
- The journal's other sources (Anthropic 2026-01-29 and 2026-03-25; Perry
  2023; Lee 2025; Sjøberg 2012; SmartBear 2006; Hupfeld 2019; Ashinoff and
  Abu-Akel 2021): not re-read for this note, and no claim here rests on them.

## Sources

Strength: **meta-analysis**, **RCT**, **experiment**, **observational** and
**preprint** as named; **practice** = a documented method of a named
organisation; **expert** = a named expert's guidance; **summary** = read only
through a secondary page. Read dates are 2026-09-30 unless marked not read.

- **barkley**: <https://www.russellbarkley.org/factsheets/ADHD_EF_and_SR.pdf> — expert, undated fact sheet (cites his 2012 book)
- **metcalfe**: <https://doi.org/10.1080/87565641.2023.2293712> — meta-analysis, *Developmental Neuropsychology* 49(1), 2024; abstract via Europe PMC
- **marx**: <https://www.sciencedirect.com/science/article/abs/pii/S0890856721020451> — meta-analysis, *JAACAP* 2021; summary at <https://www.adhdevidence.org/blog/time-blindness-found-to-be-a-consistent-feature-of-adhd> (2022-03-21)
- **mette**: <https://doi.org/10.3390/ijerph20043098> — review, *IJERPH* 2023-02-10 (PMC9962130); abstract via Europe PMC
- **liebel**: <https://arxiv.org/abs/2312.05029> — qualitative, 19 interviews, 2023-12-08
- **shapeup-3**: <https://basecamp.com/shapeup/1.2-chapter-03> — practice, 37signals, 2019
- **shapeup-8**: <https://basecamp.com/shapeup/2.2-chapter-08> — practice, 2019
- **shapeup-14**: <https://basecamp.com/shapeup/3.5-chapter-14> — practice, 2019
- **metr**: <https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/> — RCT, 2025-07-10
- **klein**: <https://hbr.org/2007/09/performing-a-project-premortem> — practice, *HBR* 2007-09; summary page only
- **mitchell**: <https://onlinelibrary.wiley.com/doi/abs/10.1002/bdm.3960020103> — experiment, 1989; not read (HTTP 403)
- **collins**: <https://corporate.jcx.au/premortem> — teaching note (formerly corporate.jasoncollins.blog), undated
- **scrum**: <https://scrumguides.org/scrum-guide.html> — practice, Scrum Guide 2020-11
- **cohn**: <https://www.mountaingoatsoftware.com/blog/the-dangers-of-a-definition-of-ready> — practice, updated 2023-06-28
- **parnin**: <https://chrisparnin.me/pdf/parnin-sqj11.pdf> — observational and survey, *Software Quality Journal* 19:5–34, 2011 (DOI 10.1007/s11219-010-9104-9)
- **parnin-deline**: <https://dl.acm.org/doi/10.1145/1753326.1753342> — experiment, CHI 2010; not read
- **mark**: <https://ics.uci.edu/~gmark/chi08-mark.pdf> — experiment, CHI 2008
- **altmann**: <https://www.interruptions.net/literature/Altmann-CogSci02.pdf> — theory and experiments, *Cognitive Science* 26, 2002; not read
- **toli**: <https://eprints.whiterose.ac.uk/id/eprint/94825/3/WRRO_94825.pdf> — meta-analysis, *Br. J. Clinical Psychology* 55:69–90, 2016 (accepted manuscript)
- **gollwitzer**: <https://www.socmot.uni-konstanz.de/publications/implementation-intentions-and-goal-achievement-meta-analysis-effects-and-processes> — meta-analysis, *Adv. Exp. Social Psychology* 38, 2006; numbers not read
- **masicampo**: <https://users.wfu.edu/masicaej/MasicampoBaumeister2011JPSP.pdf> — experiments, *JPSP*, online 2011-06-20
- **solanto**: <https://www.researchgate.net/publication/41968971_Efficacy_of_Meta-Cognitive_Therapy_for_Adult_ADHD> — RCT, *Am. J. Psychiatry* 167(8), 2010; not read
- **qu**: <https://arxiv.org/abs/2605.18583> — preprint, 2026-05-18
- W3C COGA, GOV.UK, AR 25-50, NN/g, Gong et al.: see the sources of [Decision pull requests](2026-09-30-decision-pull-requests.md#sources)

[barkley]: https://www.russellbarkley.org/factsheets/ADHD_EF_and_SR.pdf
[metcalfe]: https://doi.org/10.1080/87565641.2023.2293712
[marx]: https://www.sciencedirect.com/science/article/abs/pii/S0890856721020451
[mette]: https://doi.org/10.3390/ijerph20043098
[liebel]: https://arxiv.org/abs/2312.05029
[shapeup-3]: https://basecamp.com/shapeup/1.2-chapter-03
[shapeup-8]: https://basecamp.com/shapeup/2.2-chapter-08
[shapeup-14]: https://basecamp.com/shapeup/3.5-chapter-14
[metr]: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
[klein]: https://hbr.org/2007/09/performing-a-project-premortem
[mitchell]: https://onlinelibrary.wiley.com/doi/abs/10.1002/bdm.3960020103
[collins]: https://corporate.jcx.au/premortem
[scrum]: https://scrumguides.org/scrum-guide.html
[cohn]: https://www.mountaingoatsoftware.com/blog/the-dangers-of-a-definition-of-ready
[parnin]: https://chrisparnin.me/pdf/parnin-sqj11.pdf
[parnin-deline]: https://dl.acm.org/doi/10.1145/1753326.1753342
[mark]: https://ics.uci.edu/~gmark/chi08-mark.pdf
[altmann]: https://www.interruptions.net/literature/Altmann-CogSci02.pdf
[toli]: https://eprints.whiterose.ac.uk/id/eprint/94825/3/WRRO_94825.pdf
[gollwitzer]: https://www.socmot.uni-konstanz.de/publications/implementation-intentions-and-goal-achievement-meta-analysis-effects-and-processes
[masicampo]: https://users.wfu.edu/masicaej/MasicampoBaumeister2011JPSP.pdf
[solanto]: https://www.researchgate.net/publication/41968971_Efficacy_of_Meta-Cognitive_Therapy_for_Adult_ADHD
[qu]: https://arxiv.org/abs/2605.18583
