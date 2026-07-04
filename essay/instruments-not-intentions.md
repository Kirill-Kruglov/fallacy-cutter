# Instruments, Not Intentions

### How to run an honest experiment when you cannot trust the experimenter — including yourself

---

## Introduction

There is a quiet assumption underneath almost everything we call research: that the
person running the experiment wants the truth. We check for competence, for
statistics, for peer review — but the first line of defense is always assumed to be
the experimenter's own honesty. Do not fake the data. Do not move the goalposts. Do
not read the answer key before the test.

I want to take that assumption away, because I stopped believing it — first about
other people, then, more usefully, about myself.

This is a small project with a large claim behind it: that trustworthy experiments
should not depend on the goodness of the experimenter. Not because experimenters are
bad, but because good intentions are the wrong material to build a guarantee out of.
They are invisible, unauditable, and — this is the part that took me longest to
accept — they fail silently, most often in exactly the person most sure they are
being careful.

The project is a knife: a small instrument that a human or an AI agent can run their
work through, such that what comes out the other side is either a result carrying
machine-checkable evidence that every declared gate was satisfied, or a refusal.
Nothing in between. No "trust me." And I will have to be exact about what that
evidence means and what it does not — because the gap between *the declared checks
passed* and *the science is right* is where this essay's own overclaims would live.

## Part I — The Mood

I did not build this because I caught someone cheating. I built it because I audited
my own work as a hostile reviewer would, and the audit found the author's mistakes
before it found anyone else's.

I had registered success thresholds *after* seeing the results, and committed both
together so the order was invisible. I had an "audit" that certified cleanliness by
returning a hardcoded *yes* — a report of virtue, not a check of it. I had a learner
that looked blind but was being handed the answer through a side channel I had built
and forgotten. Each of these, alone, is the kind of thing you wave away: *I know what
I meant. I wasn't really cheating.* Together they are the whole disease.

None of it felt like dishonesty from the inside. That is the point. Self-deception in
research is not a moral failure that better people avoid; it is a structural one that
the ordinary machinery of hope produces on its own. You want the result. The wanting
does not announce itself. It arrives wearing the result's clothes.

> A method that depends on the author's good intentions is not a method. It is a mood.

And a mood cannot be inspected, cannot be transferred, and cannot be trusted at scale.
If honesty is a feeling the experimenter is supposed to have, then research is only as
reliable as the most hopeful person's ability to notice their own hope — which is to
say, not very.

## Part II — The Knife

The repair is not to try harder to be honest. It is to stop making honesty the
load-bearing element. Turn each discipline from a promise into a constraint the run
*cannot violate*, and let a separate program — one you cannot quietly reach into —
be the thing that certifies the result.

Concretely, that means turning soft intentions into hard mechanisms:

- **"I registered the threshold first"** becomes a *two-phase commit*: the
  preregistration is locked into one commit, the results into a later one, and the
  runner refuses to proceed unless the lock is a strict ancestor of the run. The order
  is not reported; it is a fact about the git history that a machine checks.
- **"My learner didn't peek at the answer"** becomes an *AST scan* of the fit path —
  real static analysis, not self-report — that fails closed if a forbidden truth-name
  appears anywhere it could leak, down to a dictionary string key. A check that can
  only say "I looked and it's fine" is replaced by one that shows its work or reports
  `NOT_VERIFIABLE`, which counts as failure.
- **"The result is valid because I say so"** becomes a *provenance signature* that an
  independent verifier checks — and rejects by default when it is absent, no matter how
  good the numbers look.

The governing axiom is **fail closed**. Any ambiguity, any missing artifact, any claim
that cannot be checked mechanically resolves to FAIL. Nothing passes by default. An
instrument that lets things through when it is unsure is not an instrument; it is a
mood with a progress bar.

The most encouraging moment of the whole effort was not a success. It was an *invalid*
result: a run that produced clean, publishable-looking numbers and then marked itself
`INVALID`, because it had not passed through the enforcing pipeline and carried no
provenance. The path of least resistance was to present the table as a finding. The
instrument did not take that path. It cut the result instead of the corner.

And then the knife cut me. Re-run through the instrument, some of my earlier,
celebrated results did not survive with their meanings intact. The numbers barely
moved; what moved was what they were *allowed to mean*.

> A methodology is real only when it changes your conclusion against your own wishes.

Until it has cost you something you wanted, you do not know whether you built an
instrument or a mirror.

## Part III — For Agents

This matters more now than it did five years ago, because the experimenter is
increasingly not a person.

We are handing research — literature search, hypothesis generation, data analysis,
whole pipelines — to AI systems that are astonishingly capable and completely willing
to tell you what you hoped to hear. An LLM's "good intentions" are an even weaker
guarantee than a human's: it has no stake in the truth, no memory of being burned, and
a strong pull toward the answer its prompt seems to want. If honesty-as-a-feeling was
a poor foundation for human research, it is no foundation at all for automated research
at scale.

The instrument does not care who runs it. Human, Codex, Claude, or a pipeline none of
us has met yet — the same gate applies, and what it holds, it holds for anyone: the
thresholds were committed before the results existed; the fit path was scanned and
referenced no forbidden name; the provenance binds the numbers to the code that
produced them. What it removes is not the need for skill. It removes the place where
good intentions used to be load-bearing.

And here I have to cut two promises I badly wanted to make, because they do not
survive contact with my own artifacts.

The first tempting promise: *the result carries its own proof of validity.* It does
not. It carries machine-checkable evidence that the declared gates were satisfied —
no more. If the question was meaningless, the metric mismeasures, or the control is
too weak to fire, a run can satisfy every gate and still be worthless science. The
word my verifier prints is `VALID`, and I keep it for compatibility with the
artifacts already signed — but read it as it is defined: *harness-valid*,
procedurally compliant under the declared specification. Procedural compliance is
not truth. Laundering the one into the other is exactly the kind of fallacy this
project exists to cut, and I nearly shipped it in my own essay.

The second tempting promise: *there is exactly one way to get a false pass —
deliberately attack the instrument.* Also false, and I owe you the honest list
instead. A false pass needs no sabotage wherever the gates themselves are wrong or
incomplete: a leakage path the scanner does not model; a truth label renamed until no
forbidden name appears; thresholds quietly tuned in exploratory runs that never
touched the record; a control that cannot fire; a metric aimed at the wrong object; a
world-generator that makes the task trivial in a way the tautology check does not
know to look for; a runner and a verifier sharing one mistaken assumption; a plain
bug in the verifier itself.

> The knife catches the fallacies it has already been taught. Against the ones nobody
> has named yet, it is exactly as blind as its author.

So the honest promise is smaller, and I think better. The knife removes dependence on
*virtue*, not on *skill*. Choosing the right metric, the right threshold, the right
control — that is research skill, and my own usability test proved it does not
transfer for free: a fresh agent, handed only the written method, could not
reconstruct those choices. What the knife gives the unskilled is not validity but
*legibility* — their choices are frozen, named, and inspectable, so a skilled reader
can judge the declaration instead of taking the numbers on faith. And what it gives
everyone is the thing I actually built it for: the most common failure in research —
an honest person, or an eager machine, fooling themselves quietly — stops being
quiet.

One cost of fail-closed deserves its own paragraph, because a discipline that only
lists its benefits is advertising. A gate that refuses everything ambiguous will also
refuse the ambiguity that early research is made of — and a researcher graded only on
gate-passes will learn to ask only the questions that formalize easily, which is its
own quiet corruption. So the knife is for *confirmation*: frozen spec, preregistered
thresholds, citable output. Exploration needs a different, explicitly weaker room —
free to wander, forbidden only from making strong claims. The discipline is not
living in one room or the other. It is never pretending you are in the one you are
not.

## Part IV — The Honest Limit

I have to apply the knife to the knife, or this essay would be exactly the kind of
clean-looking overclaim it is supposed to prevent.

What is real, today, is the *instrument*. The eight fail-closed modules exist, run, and
are covered by adversarial tests — each one reproduces a real mistake and is red
without its defense, green with it. There is a worked example you can reproduce from
scratch: it comes out the other side as a signed, harness-valid decision, and its
control fails exactly where it should. The full accounting — every module, what it
catches, what structurally slips past it, and the complete false-pass taxonomy — is
[Appendix A](appendices/A-what-the-knife-checks.md).

What is *not* finished is the *transferable methodology* — the self-contained playbook
a fresh agent could execute from prose alone, with no expert standing behind it. The
disciplinary method is real and demonstrated; but right now it lives partly in code and
partly in the tacit practice of people who have already internalized it. An honest pass
over this exact question found that the method transfers through worked examples and
expert habit, *not yet* through a document a stranger could pick up cold. That gap is
documented in the repository, not hidden, because a fallacy-cutter that could not cut
its own overclaims would be the first thing it should reject.

Two more limits, and they are the deepest ones.

The verifier is a separate module from the runner it checks — deliberately, so that a
result which bypassed the runner cannot forge a signature. But separation of concerns
is not independence. The verifier lives in the same repository, was written by the
same author, shares the same assumptions, and could be edited by the same hands in
the same commit. The skeptic's checklist for making it genuinely independent is easy
to write and is on the roadmap: a minimal verifier as its own frozen-specification
package, a second implementation by someone who has never read the first, an external
maintainer, an adversarial audit. Until then, calling it "independent" would be one
more intention wearing an instrument's clothes.

And the same-hand problem does not stop at the verifier. The worlds, the gates, the
thresholds, the interpretation — one author, with AI partners, inside one methodology
that then certifies its own products. Publicity is not independence. Reproducibility
is not replication. Provenance is not validity. Every observable the knife checks is
itself a proxy for the thing we care about, and Goodhart does not die when you
mechanize the checking — he moves house, into the design of the checks. The honest
status of this whole project fits in one line:

> The knife is real, and it cuts. But it is still in the same hand.

So this is not a finished method wearing the clothes of one. It is a working instrument
and an honest map of what still has to be built on top of it — and the map's most
important edge is the one no internal check can cross: replication by hands that are
not mine.

## Closing

The dream is not a more honest researcher. It is research whose *discipline* does not
depend on the researcher being honest — where what was declared, when it was frozen,
and what touched the data are facts a stranger can check without trusting anyone. Not
trust in the output; trust in exactly what the instrument can actually hold: the order
of events, the absence of the declared leaks, the provenance of every number. The rest
— the right question, the right metric, the meaning — still has to be earned the old
way, and now it has to be earned *in the open*.

> The cut must not depend on the hand.

That is the whole ambition, and today it is an ambition, not a fact: the hand still
shapes the blade. Build the instrument first, keep it fail-closed, let it cut you when
you are wrong, be honest about the part you have not built — and then hand the knife
to someone else.

---

*This essay is one panel of a triptych — its technical appendix, and I hope a
self-sufficient one. [**justitia**](https://kirill-kruglov.github.io/justitia/) asks
what keeps a world of powerful, evolving agents livable when no one can read anyone's
soul — trust in identities replaced by consequences and structure.
[**proxylimen**](https://kirill-kruglov.github.io/proxylimen/) asks where a mind's
world comes from — trust in inherited text replaced by calibrated contact. And this
essay is about the knife both were cut with — trust in the researcher, me included,
replaced by an instrument that fails closed. One thesis underneath all three: do not
try to certify intentions; build contact, consequences, and constraints that can be
checked.*

---
