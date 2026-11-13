# NEXO 0.3

Private Sites application. Uses platform-provided identity headers and per-user client-encrypted R2 objects. No simulated tool output is used for operational results.

## Functional modules

- DNS (Google Public DNS), RDAP (rdap.org routing to registries), IPv4 routing/ASN (RIPEstat).
- Local Web Crypto SHA-256 (25 MB limit), file properties, URL structure inspection and cryptographic password generator. File contents are never uploaded.
- Cases, evidence with provenance, manually documented coordinates, timelines, per-user server persistence, optimistic concurrency, export and import.
- Institutional interface: OpenStreetMap, cases, sources, evidence and timeline. No terminal/pentest controls. Selecting a profile does not verify institutional identity or grant additional privileges.
- Optional OpenAI Responses integration. Disabled until a server secret is configured. No custom model training has been performed. Case context is sent only with explicit selection per question.
- Global visual globe remains labeled as synthetic and is isolated from investigative locations.

## Deployment

Run `node scripts/build.mjs`, `node --test tests/api.test.mjs tests/vault.test.mjs tests/worker.test.mjs`, `node tests/ui.test.cjs` and `node tests/vault-ui.test.cjs`. Deploy exact committed source with `.openai/hosting.json` and `dist/server/index.js`. Static assets are embedded at build time. `BUCKET` is the Sites R2 binding.

## Runtime secrets

`LINUX_RUNNER_URL` and `LINUX_RUNNER_TOKEN` (optional, dedicated HTTPS execution service; see runner/README.md). `OPENAI_API_KEY` (optional; server-only) and `OPENAI_MODEL` (optional, defaults to gpt-4.1-mini). Never put credentials in source, browser code or chat. Configure through Sites environment tools. The platform handles `/signin-with-chatgpt` and `/signout-with-chatgpt`.

## Scope and limitations

Current infrastructure is a Cloudflare Worker: no Linux, arbitrary TCP, packet capture or durable processes. An optional fixed-argument Nmap runner adapter is included under runner/ but is not deployed. TShark, Sherlock and additional pentest tools are not integrated. They require a separate persistent isolated Linux execution service with authenticated jobs, server-enforced target scopes, resource limits, tool licenses and audited lifecycle. No arbitrary shell or unscoped execution endpoint is exposed.

The role picker only adapts navigation. All cases belong to the authenticated visitor; no inter-user or institutional sharing is implemented. API mutations enforce same-origin requests. Storage paths derive only from trusted platform identity. Concurrent edits use object etags and return conflicts; data can be exported before reloading. The limited audit history is not immutable forensic chain-of-custody evidence.

NEXO is not a malware scanner, password vault, person locator or forensic certification system. RDAP and routing data may be incomplete and do not establish identity. No real threat telemetry is configured. External providers receive query values. OpenStreetMap receives map tile requests. Software licensing for Leaflet is included in web/vendor/leaflet-LICENSE.txt.

Browser visual QA may require the managed cua_repl.js capability; do not replace the managed preview infrastructure to bypass its absence.

## Security and migration

See SECURITY.md for the exact encryption boundary, no-recovery design, legacy migration, export/AI/map disclosures and remaining trust assumptions. Entry is /login; /app requires platform identity, then profile selection and vault unlock. Existing records are not encrypted until the owner creates a passphrase and completes the migration save. New case writes require encrypted envelopes.
