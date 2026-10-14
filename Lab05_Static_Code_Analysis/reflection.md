# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis, and why is it important?

Static code analysis examines source code without executing the
program. It helps identify potential bugs, security vulnerabilities,
poor programming practices and coding-style violations.

It is important because it identifies problems early, improves
maintainability and reduces debugging effort. It also helps
developers create more reliable and secure software.

## 2. What are the differences between Pylint, Bandit and Flake8?

Pylint evaluates overall Python code quality, including naming
conventions, documentation, unused variables and potential errors.

Bandit focuses on security vulnerabilities and unsafe coding
patterns, such as insecure communication protocols and risky
coding practices.

Flake8 checks Python style, formatting, whitespace, line length,
unused imports and other static errors.

Using all three tools provides broader coverage than relying
on a single tool.

## 3. What issues were identified and how were they fixed?

The original loan calculator contained calculation, validation,
security and code-quality problems. These included hard-coded
FTP credentials, insecure FTP communication, a mutable default
argument, an eligibility-check bypass, incorrect EMI input,
an inaccurate maximum-loan calculation and incorrect risk
classification.

The fixes included replacing FTP with SFTP over SSH, moving
credentials to environment variables, using JSON persistence,
removing the mutable default argument, validating eligibility
conditions, correcting interest-rate usage and improving the
loan and risk calculations.

## 4. What are the limitations of static code analysis?

Static analysis can identify many potential problems without
executing a program, but it cannot guarantee that the software
is free from all bugs or vulnerabilities.

Some problems depend on runtime behaviour, user input or
external systems and may not be detected. Tools can also
produce false positives or miss certain vulnerabilities.

Therefore, static analysis should be combined with functional
testing, runtime checks and code review.
