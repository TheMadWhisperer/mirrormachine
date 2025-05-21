# Mirrormachine

A transparent, entropy-reactive encryption engine designed to resist structure, defy modeling, and leave nothing useful for attackers.

## Intent

This project was created as an exploration of structureless, post-comprehension encryption.
It aims to provide:

- Full transparency of implementation
- No dependency on corporate, government, or cloud infrastructure
- Resistance to future mathematical and quantum advances
- A system that cannot be analyzed, only experienced

It is **not designed for mass-market adoption** — it is a gift for those who *need* it, not those who market it.

## Basic Principles

- The system derives a long entropy string via Argon2, tuned to high memory and time cost.
- This entropy string is then used to **dynamically generate a mutation machine** — a transformation engine that shifts based on internal entropy.
- The machine mutates an instance specific key (naturally sourced entropy) in a non-linear, non-reversible manner.
- Incorrect input (i.e. wrong password) yields output that looks *plausibly correct* but is *entirely false* — eliminating brute-force guidance.
- The non-reversible result of transformation can be used as an encryption key.

This is not encryption with failure detection.
This is encryption with **false success** on every failure.

## Patent Intent

This system is intended to remain free, open, and unpatentable — forever.

# NO_PATENTS.md

This system — its design, logic, and behavior — is released with the intent to remain **unpatentable** and **universally available**.

I do not claim a patent on this system, and I **explicitly prohibit** any individual or entity from patenting this or any direct variant of its entropy-reactive encryption mechanism.

## What I welcome:
- Use by researchers, activists, artists, non-profits
- Use by for-profit organizations that uphold open-source values
- Forks and adaptations that respect the original spirit

## What I reject:
- Proprietary forks hidden behind walls
- Corporate attempts to lock or license what was given freely
- Any misuse of this work for surveillance, gatekeeping, or exploitation

You are free to use this system. But do not **try to own it**.
It belongs to those who understand it.

## Acknowledgements

I would like to very sincerely thank creators of those technologies and libraries for making experiments
like this one possible and safe to use:

- Argon2
- Python programming language

## Philosophy

Not all safety must be structured.
Not all encryption must be measured.
Some defenses are stronger when they're unreadable — even by those who write them.

This system is not designed to be trusted.
It is designed to be **undecipherable** to all but the one who holds the correct invocation.

In an age of structure-breaking algorithms,
this is a structureless ghost.

No assumptions. No oracles. No signal.

Only mirrors.

— *TheMadWhisperer*
