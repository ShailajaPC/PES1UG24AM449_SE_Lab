# Lab 5 — Reflection

> **Note:** The README supplied with the lab refers to four questions in a separate handout, but that handout was not provided. The responses below address four relevant reflection topics based on the instructions available. If your instructor later provides the exact questions, update this file to match them.

## 1. Why is static code analysis useful?

Static code analysis checks source code without requiring the program to be executed. Pylint helps identify maintainability and code-quality problems, Flake8 checks style and formatting, and Bandit looks for common security risks. Using all three provides different perspectives on the same program.

## 2. Which issues were most important, and why?

The security-related findings were the most important because the program handles payment operations and secrets. Hardcoded credentials can be exposed, weak hashing can make PIN verification less secure, insecure temporary-file creation can create race conditions, and ordinary pseudo-random generators are unsuitable for security-sensitive OTPs. These issues should be addressed before lower-impact formatting warnings.

## 3. How did the fixes improve the program?

The cleaned version moves configuration secrets to environment variables, uses constant-time comparison for secret checks, uses `secrets` for OTP generation, replaces insecure temporary-file creation with `NamedTemporaryFile`, and improves naming, documentation, and formatting. These changes improve readability and address the specific findings recorded in the original analysis. They do not by themselves make a demonstration wallet production-ready.

## 4. What did you learn, and what would you do next?

I learned that a program can appear to work while still containing security, style, and maintainability issues. I also learned that different analysis tools detect different categories of problems and that their reports should be rerun after changes. Next, I would add automated tests for valid and invalid payments, insufficient balance, daily limits, incorrect PINs, missing secrets, and cashback calculations. For a real payment system, I would also use a dedicated password-hashing algorithm, stronger secret management, and a proper transaction/audit design.
