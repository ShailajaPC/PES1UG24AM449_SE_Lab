# Lab 5 — Static Code Analysis Issues

The line numbers below refer to the original version of `digital_wallet.py` represented by the supplied BEFORE-analysis reports. Line numbers may differ in the cleaned version.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Weak SHA-1 hashing for PIN | Security — High | 14 | The original implementation used SHA-1 to hash the PIN. SHA-1 is not recommended for security-sensitive hashing. A PIN is also low-entropy, so a fast general-purpose hash is not ideal for storing PINs in a real system. | Replace SHA-1 with a safer password/PIN verification design. In the supplied cleaned demo, SHA-256 is used with constant-time comparison; for production, use a password-hashing function such as Argon2, scrypt, or PBKDF2 with a unique salt. |
| Hardcoded gateway secret and wallet PIN | Security — Medium | 6–7 | Secrets embedded directly in source code can be exposed through repository access, screenshots, or source distributions. | Read secrets from environment variables and avoid committing real credentials. The cleaned version uses `GATEWAY_SECRET` and `WALLET_PIN` environment variables. |
| Insecure temporary-file creation | Security — Medium | 60 | The original version used `tempfile.mktemp()`, which generates a filename without securely creating the file and can introduce a race condition. | Use `tempfile.NamedTemporaryFile()` to create the temporary file securely. The cleaned version uses this API. |
| Non-cryptographic random number generator for OTP | Security — Low | 64 | The original version used `random.randint()` to generate a one-time password. The `random` module is not designed for security-sensitive values. | Use `secrets.randbelow()` to generate an unpredictable OTP. |
| Missing module and function docstrings | Code quality — Low | Multiple | Pylint reported missing documentation strings, making the module and functions harder to understand and maintain. | Add a module docstring and concise docstrings to functions. |
| Naming conventions and whitespace violations | Style — Low | Multiple | Pylint and Flake8 reported names that did not follow Python naming conventions and formatting violations such as missing spaces. | Use `snake_case` for functions and variables, use uppercase names for constants, and format code consistently. |
| Mutable default argument | Code quality — Medium | 17 | The original function used a list as a default argument. Mutable defaults can retain changes between function calls and cause unexpected shared state. | Use `None` as the default and create a new list inside the function when no list is supplied. |

## Verification notes

- The supplied BEFORE reports document the findings in the original code.
- The supplied AFTER reports show a Pylint score of 10.00/10, no Bandit issues identified, and no Flake8 output.
- Run the tools again on the exact final `digital_wallet.py` before submission so the reports are generated from the same code version.
