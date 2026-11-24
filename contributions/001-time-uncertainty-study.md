# Contribution 001 — Access decisions under uncertain local time

**Original parameter study, 24 November 2026.** A disconnected system can have a locally available clock whose relationship to true time is uncertain. A timestamp's presence does not establish freshness of a grant.

## Question and hypotheses

A grant is valid on the half-open interval `[not_before, expires)`. A point-clock decision treats observed local time as exact. An interval decision permits access only when the entire verified uncertainty interval lies inside the validity window. The study asks how unsafe allows and conservative denials change under declared clock-error bounds.

The model does not synchronise a clock or estimate a site's real drift. It assumes a trusted source and known uncertainty radius. These are external requirements, not outputs of the model. [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) is the primary context for policy decisions and dynamic trust; the interval rule and test grid are this contribution's proposed model.

## Reproducible method

[The code](../tools/time_model.py) uses a 600-second grant, nine true-time values around issue/interior/expiry, five clock offsets and three error radii: 0, 15 and 60 seconds. This yields 135 computed cases. Each row records the true-time oracle, observed time, declared bound, whether the true time is inside it, both decisions, unsafe allows and conservative false denials.

All times are synthetic elapsed seconds relative to issuance. No bank authorization service, physical oscillator, NTP source or regulatory timestamp is measured. The [CSV/results](../evidence/results.json) retain the cases where a declared bound is false; they are not discarded to create a stronger conclusion.

## Result and interpretation

The actual summaries are in [execution evidence](../evidence/results.json). For the 60-second radius every selected offset is within the assumed bound. The interval rule then avoids unsafe allows on this finite grid, while causing additional denials near the issue/expiry boundaries. Smaller falsely asserted bounds can still allow outside the true grant window.

This illustrates the availability cost of conservative time handling and the dependence on a sound bound. It is not a proof that real clocks are bounded or that the model is complete. A zero local error flag is not justified simply because a time service last returned a timestamp.

## Operational design consequences

Define an owner for time-source trust, holdover behaviour, maximum offline duration and error-bound growth. Measure initial uncertainty and drift for the actual devices; record failures and any tampering. A cryptographically signed time response can authenticate its source without eliminating network delay or subsequent clock drift. Do not let an agent or untrusted log supply `clock_verified=true`.

Separate uncertain authorization from business continuity. Use a reviewed emergency-access process if the application cannot remain available with conservative checks; do not silently extend ordinary grants. Audit the exception, exact authority, scope and expiry. Clock loss is a reason for an explicit decision, not an invented current timestamp.

Future work should add a real holdover experiment, adversarial time-source tests and restored-system behaviour. Publish hardware, method, raw observations, uncertainty and deviations before claiming site freshness assurance.
