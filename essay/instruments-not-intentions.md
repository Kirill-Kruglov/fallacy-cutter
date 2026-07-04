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
work through, such that what comes out the other side is either a result that carries
its own proof of validity, or an honest refusal. Nothing in between. No "trust me."

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
us has met yet — the same gate applies. Run your work through it and you get either a
provenance-signed valid decision or a fail-closed stop, *independent of how good you
are at research*, and independent of whether you even understood the discipline you
just satisfied. That is the actual promise:

> A well-meaning novice and a careless expert, run through the same knife, both get a
> result that is either honestly valid or honestly refused.

There is exactly one way to get a false pass: deliberately attack the instrument
itself — rewrite the verifier, forge the signature, disable the hook. That is a
different and more honest kind of failure. It is no longer self-deception; it is
sabotage, and sabotage at least leaves fingerprints. The knife cannot stop a
determined liar. It can stop the far more common thing: an honest person, or an eager
machine, fooling themselves.

## Part IV — The Honest Limit

I have to apply the knife to the knife, or this essay would be exactly the kind of
clean-looking overclaim it is supposed to prevent.

What is real, today, is the *instrument*. The eight fail-closed modules exist, run, and
are covered by adversarial tests — each one reproduces a real mistake and is red
without its defense, green with it. There is a worked example you can reproduce from
scratch: it comes out the other side as a valid, signed decision, and its control
fails exactly where it should.

What is *not* finished is the *transferable methodology* — the self-contained playbook
a fresh agent could execute from prose alone, with no expert standing behind it. The
disciplinary method is real and demonstrated; but right now it lives partly in code and
partly in the tacit practice of people who have already internalized it. An honest pass
over this exact question found that the method transfers through worked examples and
expert habit, *not yet* through a document a stranger could pick up cold. That gap is
documented in the repository, not hidden, because a fallacy-cutter that could not cut
its own overclaims would be the first thing it should reject.

So this is not a finished method wearing the clothes of one. It is a working instrument
and an honest map of what still has to be built on top of it.

## Closing

The dream is not a more honest researcher. It is research whose validity does not
depend on the researcher being honest — a discipline you could hand to a stranger, or
to a machine, and still trust the output, because the trust lives in the instrument and
not in the hand that holds it.

> The cut must not depend on the hand.

That is the whole ambition. Build the instrument first, keep it fail-closed, let it
cut you when you are wrong — and be honest about the part you have not built yet.

---
