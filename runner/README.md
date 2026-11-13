# Linux execution adapter (not deployed)

This adapter implements a fixed Nmap TCP connect/service discovery job, not an interactive shell and not an unrestricted tool suite. It has not been tested in a running container or against a real target. Unit tests cover scope enforcement and result parsing.

## Operator prerequisites

Use a dedicated Linux host with Docker, a trusted TLS reverse proxy and a defined network boundary. Do not run on the web application host, with privileged containers, Docker socket access, or on a workstation containing sensitive data. Network reachability still needs to be limited by the host/firewall to the authorized lab scope. This fixed adapter is not a multi-tenant arbitrary-code sandbox.

Set NEXO_RUNNER_TOKEN to a random token of at least 32 characters using your secret manager. Set NEXO_ALLOWED_CIDRS to the exact networks you own or are authorized to assess. It defaults to empty, so no targets are allowed. Hostname input also requires an exact entry in NEXO_ALLOWED_HOSTS and every resolved IPv4 must be inside the allowed networks. DNS is resolved once and the approved address is pinned to the job.

From this directory run `docker compose up -d --build` after preparing the environment. Only localhost:8080 is published. Place it behind TLS on a dedicated hostname and restrict ingress to the application where supported. Configure the Site's LINUX_RUNNER_URL to that HTTPS origin and LINUX_RUNNER_TOKEN to the same secret. Never submit secrets through chat or browser fields.

The NEXO Worker forwards the authenticated visitor as a hashed identity. The runner validates authorization and ownership on every result request. Two jobs maximum; fixed Nmap arguments; 75-second wall timeout; no shell, scripts, flags, CIDR targets or arbitrary command arguments. Jobs are held in memory for up to one hour and lost on restart. Save completed results to an investigation case to retain them.

## Extending tool coverage

Add a separate reviewed adapter per tool with input schemas, explicit licenses, execution isolation, output normalization, limits and tests. Packet capture needs an explicitly authorized capture source and different privileges; do not grant raw network privileges to this service. Browser-based web assessment, malware analysis and forensic disk handling need dedicated execution environments. This adapter intentionally does not claim those capabilities.
