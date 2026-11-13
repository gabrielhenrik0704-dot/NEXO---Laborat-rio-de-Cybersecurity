# NEXO security model — 0.3

## Authentication and roles

The private Site access policy is preserved. Platform authentication is mandatory for case APIs; the gateway supplies the trusted visitor identity. `/login` is the app entry, `/app` requires identity, and the visitor chooses a role before unlocking the vault. Roles personalize navigation; none grants institutional verification or additional privileges. PF is explicitly self-declared. Only platform-granted access controls who can visit the private Site.

No homemade password database, OAuth exchange, cookie or recovery service has been introduced. Platform sign-in/out routes are navigated at the top level. The vault passphrase is a separate secret from the account login.

## Client-side encrypted vault

Each user has an independent R2 object, keyed by platform identity. The browser encrypts the entire case workspace before uploading using Web Crypto AES-256-GCM, a fresh random 96-bit IV per encryption, a 128-bit authentication tag and account-bound additional authenticated data. Keys derive from the passphrase using PBKDF2-HMAC-SHA-256 with 600,000 iterations and a random 128-bit salt. The key is non-extractable, kept only in memory, and not written to localStorage, sessionStorage, source or the server. The passphrase is not transmitted. Non-sensitive profile and selected case-ID preferences remain local.

`/api/workspace` rejects the old plaintext write format. The server validates the encrypted envelope shape, fixed cryptographic parameters, body size and account context. ETags prevent ordinary concurrent overwrites. Storage sees ciphertext size, identity and save timestamps. Cryptography does not hide that metadata or prevent a malicious storage operator from replaying an old ciphertext.

Locking clears application references to keys and decrypted case content, resets sensitive UI/results, and stops maps/animations. Keys can only be recreated with the passphrase. Auto-lock is scheduled after ten minutes without interaction; it is postponed while writes or unsaved changes are pending to avoid losing work. Pagehide also clears decrypted application state and restored BFCache pages reload locked. JavaScript cannot guarantee physical zeroization of every browser memory copy or clipboard.

**No passphrase recovery exists. Losing the phrase means losing access to encrypted cases.** A strong randomly generated multi-word phrase is recommended; a predictable 16-character phrase is still weak.

## Scope and explicit disclosures

- This is a personal client-encrypted storage vault, not end-to-end encrypted messaging between users.
- Ordinary OSINT queries and their results are processed by the application backend and public providers. They are not end-to-end encrypted. Saved copies become part of the encrypted vault.
- AI questions and explicitly shared case context are visible to the application backend and AI provider. Case context is opt-in with an additional confirmation. OpenAI Responses requests set `store:false`; this does not promise zero provider retention in all account configurations. The UI states the boundary.
- OpenStreetMap is loaded only after an explicit user action. IP and requested tile regions are disclosed to the map provider and can reveal an approximate viewport.
- Default JSON backups are encrypted. Import decrypts locally using the backup's phrase. Plaintext report export requires confirmation and is clearly labeled; the downloaded report is no longer protected by the vault.
- Existing plaintext case records are read for migration after login and encrypted on the next save after the user creates a phrase. Migration does not retroactively protect older exports, logs, snapshots or copies. Historical deletion is not claimed.

## Web controls

All Worker responses include no-store cache policy, HSTS, MIME sniffing prevention, no-referrer, restrictive permissions and CSP. Executable inline scripts/handlers are disallowed (`script-src 'self'; script-src-attr 'none'`). Leaflet-required inline styling remains allowed. Frame ancestry is limited to the same origin and explicit ChatGPT/Codex origins. Dependencies are served locally. There are no third-party fonts or analytics. APIs enforce visitor identity, origin on writes, JSON content type, streaming body limits and per-user storage isolation. Public queries use fixed upstream service origins. Output is escaped, and map popup user content uses text nodes.

## Remaining trust and work

The server still delivers the JavaScript; a compromised hosting account, malicious app update, browser extension, compromised endpoint or XSS with script execution could access unlocked data or the passphrase. Browser code must be trusted. An independent security audit and browser-based QA are not completed. No claim of absolute security, certified forensic chain of custody or full compliance is made. The application-level consultation limiter is per Worker isolate and is not a distributed WAF or DDoS defense. Provider settings, service credentials, backups and Linux runner isolation require ongoing operational review.

Linux test tooling and optional AI are still dependent on separately configured infrastructure and credentials. E2EE does not secure a compromised Linux runner or its job output before import into a vault.

## Declarative extensions and introductory courses (0.4)

Imported integration manifests are data, not code. Strict schemas reject unknown fields, arbitrary commands/scripts/endpoints, unavailable adapters and incompatible input types. User-installed manifests live inside the encrypted workspace. Author fields are declared metadata, not verified signatures. The backend continues enforcing authentication, fixed public sources and server-side Linux scope. Manifest installation does not install binaries or grant permissions. A new adapter requires reviewed source changes and deployment.

Course progress is stored inside the encrypted workspace per profile. Completion only hides the introductory guide; it does not grant privileges, certify training or validate institutional identity. The user can reopen the guide. Backups include integration definitions and course progress; imports validate definitions before merging.
