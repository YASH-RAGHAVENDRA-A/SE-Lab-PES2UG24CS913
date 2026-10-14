# Lab 5: Static Code Analysis — Issue Report

## Identified Issues and Fixes

The line numbers below refer to the original starter file
provided in the assigned repository, before corrections.

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Hard-coded FTP credentials | Security | 60 | The FTP username and password are embedded in the source code. | Read credentials from environment variables. |
| Insecure FTP communication | Security (High) | 2, 60-64 | The original code uses ordinary FTP for transmitting credentials and files. | Replace FTP with SFTP over SSH and use verified SSH host keys. |
| Unsafe persistence format | Security / Reliability | 3, 47-59 | The original program saves and loads records using marshal without validating the record structure. | Use JSON persistence and validate loaded records. |
| Mutable default argument | Bug | 17-18 | The default list is shared between calls and is modified by the function. | Remove the mutable default argument. |
| Eligibility validation bypass | Logic error | 21-28 | An early return can approve an applicant before checking existing EMI and loan type. | Validate every mandatory eligibility condition first. |
| Incorrect EMI demonstration | Calculation error | 84 | The 9% annual interest rate is passed as 9 instead of 0.09. | Use 0.09 as the decimal annual interest rate and handle zero-interest loans. |
| Incorrect maximum-loan calculation | Logic error | 29-34 | The original calculation sums monthly payment capacity without accounting for interest. | Calculate the loan principal using the present-value formula. |
| Incorrect prepayment savings | Calculation error | 68-71 | The original calculation compares total repayments without correctly accounting for the principal reduction. | Calculate interest before and after prepayment and compare the two. |
| Invalid credit-score classification | Logic error | 72-82 | Scores above 900 are classified as low risk. | Validate the score range before assigning a risk band. |
| File handling and random identifiers | Code quality | 45-59, 63 | Files are opened manually, and identifiers use the standard random module. | Use context managers and a suitable secure identifier generator. |

## Verification

The corrected implementation was compiled and executed successfully
during development.

Pylint, Bandit and Flake8 were used to analyse the corrected code.
The original and final reports are stored in the reports directory.

The initial findings are based on the assigned starter code. Not
every code-review finding is necessarily reported by every tool.
