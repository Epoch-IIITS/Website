# Learn Python executor: VPS deployment

The executor runs Python code and supplied tests in restricted Docker containers. Next.js owns authentication, MongoDB writes, submissions, and progress. The executor has no database credentials. Next.js calls only `POST /execute` with a server-held bearer token; the executor has no `/health` route.

Choose **one** of the three HTTPS connection cases below after completing the shared service setup. `LEARN_EXECUTOR_URL` must be an `https://` **origin** (with a port if needed); Next.js appends `/execute` itself and rejects HTTP. Keep `LEARN_EXECUTOR_TOKEN` server-only and use the same value on both sides. The executor service always stays on `127.0.0.1:8765` unless you explicitly change `LEARN_EXECUTOR_PORT`.

## Shared setup: runner and host service

Use a dedicated Linux VPS or VM with Docker Engine, Python 3, and OpenSSL. The service is sized for **2 vCPU, 4 GB RAM and a 40 GB SSD** (about 100 students): two jobs run at once, each limited to one CPU and 1 GB, and two preloaded containers wait for the next jobs. Add a 2 GB host swap file as a safety margin for the host; containers themselves cannot swap:

```sh
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile
sudo mkswap /swapfile && sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```
 These commands assume Ubuntu and the standard Docker socket. Docker access is effectively root access, so restrict administrator access to this machine. Keep Docker's default seccomp profile enabled. Follow [Docker's Ubuntu installation guide](https://docs.docker.com/engine/install/ubuntu/) and confirm `sudo docker info` succeeds.

Deploy this repository to the VPS, including `executor/service.py`, `executor/runner.py`, `executor/Dockerfile`, and `executor/tests.generated.json`. A fresh Git checkout will see them only after they are committed and pushed. From the repository root on the VPS:

```sh
sudo docker build -t epoch-learn-runner:latest executor/
sudo install -d -m 700 /opt/epoch-learn-executor
sudo install -m 600 executor/service.py /opt/epoch-learn-executor/service.py
sudo install -m 600 executor/tests.generated.json /opt/epoch-learn-executor/tests.generated.json
```

The image (about 1.9 GB on disk) contains Python 3.13 and every library the packs use, pinned in `executor/requirements.txt`: NumPy, pandas, SciPy, scikit-learn, OpenCV (headless), PyTorch (CPU build, installed from `https://download.pytorch.org/whl/cpu`), FastAPI, httpx, LangChain Core, LangGraph and Gymnasium. Keep the previous image tagged for rollback; two versions use under 4 GB of the SSD.

Keep `tests.generated.json` on the server. Do not put it in `public/`, serve it as a static file, or send it to the browser. The host service reads the test file from its own directory and passes tests to a restricted runner container.

Generate an executor token with `openssl rand -hex 32`. Put the generated value in `/etc/epoch-learn-executor.env` and restrict that file to root:

```sh
sudoedit /etc/epoch-learn-executor.env
sudo chmod 600 /etc/epoch-learn-executor.env
```

```dotenv
LEARN_EXECUTOR_TOKEN=<generated-64-character-token>
```

Create `/etc/systemd/system/epoch-learn-executor.service` with `sudoedit`:

```ini
[Unit]
Description=Epoch Learn Python executor
Requires=docker.service
After=network-online.target docker.service
Wants=network-online.target

[Service]
Type=simple
User=root
EnvironmentFile=/etc/epoch-learn-executor.env
WorkingDirectory=/opt/epoch-learn-executor
ExecStart=/usr/bin/python3 /opt/epoch-learn-executor/service.py
Restart=on-failure
RestartSec=3
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

This example runs the service as root to reach the root-owned Docker socket; use the dedicated VPS for that reason. Start it and enable it after reboot:

```sh
sudo systemctl daemon-reload
sudo systemctl enable --now epoch-learn-executor
sudo systemctl status epoch-learn-executor --no-pager
```

Do not publish port **8765** or the Docker socket. The service listens only on loopback; the selected HTTPS frontend below connects to it locally.

## Case 1: the VPS provider gives an HTTPS URL

Use the provider's managed HTTPS proxy if it can forward requests to the executor's local HTTP service. Configure its upstream as `127.0.0.1:8765`, keep the full request path and `Authorization` header, and allow `POST` bodies up to the executor's 20 KB request limit. The provider URL alone is insufficient unless it actually routes to this service. If its proxy cannot reach the local service, use Case 2 or a public ingress arrangement instead.

Example server environment for the **Next.js** deployment:

```dotenv
LEARN_EXECUTOR_URL=https://your-provider-executor.example
LEARN_EXECUTOR_TOKEN=<same-executor-token>
```

Architecture: `Next.js server → provider HTTPS proxy → HTTP 127.0.0.1:8765 → Docker runner`. You do not need DuckDNS or Caddy for this case.

## Case 2: private IP, no provider HTTPS URL

A private-only IP cannot be reached from the public internet through a DuckDNS record. Use a public HTTPS tunnel or a separate public gateway. One option is [Tailscale Funnel](https://tailscale.com/docs/features/tailscale-funnel), which provides a public `*.ts.net` HTTPS URL and forwards to this VPS's loopback service without an inbound public port or Caddy.

1. [Install Tailscale on Linux](https://tailscale.com/docs/install/linux), then enable its service and connect the VPS to your tailnet:

   ```sh
   sudo systemctl enable --now tailscaled
   sudo tailscale up
   ```

2. In the Tailscale admin console, enable MagicDNS, HTTPS certificates, and Funnel for the tailnet. Complete the approval flow that the CLI opens on first use.
3. On the VPS, run:

   ```sh
   sudo tailscale funnel --bg --https=443 8765
   sudo tailscale funnel status
   ```

4. Copy the **actual** `https://<machine>.<tailnet>.ts.net` URL printed by Funnel into the Next.js server environment:

   ```dotenv
   LEARN_EXECUTOR_URL=https://your-machine.your-tailnet.ts.net
   LEARN_EXECUTOR_TOKEN=<same-executor-token>
   ```

Architecture: `Next.js server → Funnel public HTTPS URL → encrypted tunnel → HTTP 127.0.0.1:8765 → Docker runner`. The `--bg` setting makes Funnel resume after Tailscale and VPS restarts. Funnel is currently a beta feature with bandwidth limits; for heavier production traffic, use a public gateway that can reach the private VPS instead. See the [Funnel CLI reference](https://tailscale.com/docs/reference/tailscale-cli/funnel) for current commands and limits.

## Case 3: public or shared IP, but ports 80/443 are unavailable

Use this when the provider routes **one other public TCP port** (for example, `5500`) to your VPS, but public ports 80 and 443 belong to another service or are unavailable. DuckDNS supplies the hostname; a custom Caddy build uses a DuckDNS **DNS challenge** to obtain a trusted certificate without needing inbound 80/443. The external port is still required for actual API traffic. If no inbound port is routed to this VPS, use Case 2.

1. Create a name such as `epoch-learn.duckdns.org` at [DuckDNS](https://www.duckdns.org/) and set its A record to the **shared public IP**. If the public IP can change, use [DuckDNS's update API](https://www.duckdns.org/spec.jsp). Keep its account token separate from `LEARN_EXECUTOR_TOKEN`. Check that `dig +short A epoch-learn.duckdns.org` resolves to the public IP; remove a stale `AAAA` record if IPv6 is not routed to this VPS.
2. Ask the provider to route public **TCP 5500** to this VPS and allow it through the VPS firewall (`sudo ufw allow 5500/tcp` if UFW is active). Keep **8765** private. Replace `5500` below with the port actually assigned to your VPS.
3. Install the [standard Caddy package](https://caddyserver.com/docs/install), then install Go and `xcaddy` per [Caddy's custom-build guide](https://caddyserver.com/docs/build). Build and install a binary with the [DuckDNS DNS provider](https://github.com/caddy-dns/duckdns):

   ```sh
   xcaddy build --with github.com/caddy-dns/duckdns --output ./caddy-duckdns
   sudo install -m 755 ./caddy-duckdns /usr/local/bin/caddy-duckdns
   /usr/local/bin/caddy-duckdns list-modules | grep -Fx dns.providers.duckdns
   ```

4. Save the **DuckDNS account token** in `/etc/caddy/duckdns.env`, then limit its permissions:

   ```sh
   sudoedit /etc/caddy/duckdns.env
   sudo chmod 600 /etc/caddy/duckdns.env
   ```

   ```dotenv
   DUCKDNS_API_TOKEN=<DuckDNS-account-token>
   ```

5. Use `sudo systemctl edit caddy` to create a drop-in. Put the following lines **between the editor's two comment markers**, where systemd says edits will be kept. This loads the token and makes both start and reload use the custom Caddy binary:

   ```ini
   [Service]
   EnvironmentFile=/etc/caddy/duckdns.env
   ExecStart=
   ExecStart=/usr/local/bin/caddy-duckdns run --config /etc/caddy/Caddyfile
   ExecReload=
   ExecReload=/usr/local/bin/caddy-duckdns reload --config /etc/caddy/Caddyfile --force
   ```

   Do not add Caddy's `--environ` flag here: it can print the DuckDNS token into service logs.

6. Replace the package's default `/etc/caddy/Caddyfile` site with this configuration. If you merge it into an existing Caddyfile, keep only one global options block and remove or adjust other sites that bind the unavailable ports 80/443. Disabling automatic redirects does not disable explicit `:80` sites.

   ```caddyfile
   {
       auto_https disable_redirects
   }

   epoch-learn.duckdns.org:5500 {
       tls {
           dns duckdns {env.DUCKDNS_API_TOKEN}
       }

       reverse_proxy 127.0.0.1:8765
   }
   ```

7. Enable Caddy at boot and restart it with the new binary and config:

   ```sh
   sudo systemctl daemon-reload
   sudo systemctl enable --now caddy
   sudo systemctl restart caddy
   sudo systemctl status caddy --no-pager
   ```

Set the Next.js server environment to the **HTTPS origin including the public port**:

```dotenv
LEARN_EXECUTOR_URL=https://epoch-learn.duckdns.org:5500
LEARN_EXECUTOR_TOKEN=<same-executor-token>
```

Architecture: `Next.js server → HTTPS :5500 (Caddy) → HTTP 127.0.0.1:8765 → Docker runner`. Caddy's DNS challenge needs outbound access to DuckDNS and the certificate authority, while the Next.js server needs to reach public port `5500`. Browsers do not call the executor directly. See [Caddy's DNS challenge explanation](https://caddyserver.com/docs/automatic-https) and the [DuckDNS Caddy module](https://github.com/caddy-dns/duckdns).

## Verify any case

Restart or redeploy Next.js after adding `LEARN_EXECUTOR_URL` and `LEARN_EXECUTOR_TOKEN`. Both are **server-only**: never use a `NEXT_PUBLIC_` prefix or put the tokens in a URL. Next.js already owns auth and MongoDB; do not give those credentials to the executor.

From a machine **outside** the VPS, send an unauthenticated POST to the selected public URL's `/execute` path. The expected HTTP status is **401**: TLS, routing, and the executor are reachable, and the token gate is working. For Case 3:

```sh
curl -sS -o /dev/null -w '%{http_code}\n' -X POST https://epoch-learn.duckdns.org:5500/execute
```

The equivalent checks use `https://your-provider-executor.example/execute` for Case 1 and the Funnel URL plus `/execute` for Case 2. Do not use `curl -k` or bypass certificate verification. This service has no `/health` endpoint; a GET to `/execute` is not the test.

Next, sign in as a test member, open `/learn/problems/factorial-validated`, and **Submit** code. A graded response saves the submission under that user's account; a passing solution contributes to `/learn/progress`. Compatible **Run** actions use local Pyodide practice, while incompatible Run actions use the executor. If trusted execution is unavailable, Next.js shows “Python execution is currently unavailable.” and saves no submission.

For errors, inspect `sudo journalctl -u epoch-learn-executor -n 100 --no-pager`. For Case 3 also inspect `sudo journalctl -u caddy -n 100 --no-pager`; for Case 2 inspect `sudo tailscale funnel status`. Confirm the public hostname and port are reachable from the **Next.js server**, not only from the VPS itself.

## Limits, updates, and tests

The host service accepts authenticated `POST /execute` requests only and caps requests at 20 KB and code at 16 KB.

* **Warm pool.** At start the service launches two containers. Each imports the libraries, runs a tiny warm-up, prints `READY` and waits for one job on stdin. A request takes a waiting container, sends the code and tests, reads the result, and the container exits and is removed. A container is never reused, so one submission cannot see another's code, files or processes. A replacement starts only while fewer than two containers are busy (running a job or importing), so refilling never competes with running tests. If containers fail to start, the service backs off for up to 30 s between attempts.
* **Queue.** At most two jobs run at once. Up to 30 more requests wait in a queue, Submit ahead of Run; a request that cannot start within about 30 s, or arrives when the queue is full, gets `503 {"error": "Busy"}`. Next.js waits up to 58 s for a response and shows “Python execution is currently unavailable.”
* **Per job.** No network, a read-only root, a 32 MB temporary filesystem, no Linux capabilities, no new privileges, 1 GB memory with swap disabled, one CPU, 64 PIDs, one thread for NumPy/PyTorch, file and output limits, a 30 s wall clock from when the job is sent, and 10 s of CPU for the learner's code and tests. The runner sets the CPU limit after the imports (current usage plus 10 s), so import time is not charged to the learner. Timed-out containers are removed.
* **Per-user limits.** Each request carries `client`, an HMAC of the signed-in user's id (Next.js never sends the id itself, and requests without it are rejected with 400). A client may make 10 Runs and 5 Submits per minute and have one request in flight; beyond that the service returns `429` with `Retry-After`, before any container is used. Set `LEARN_EXECUTOR_RUNS_PER_MINUTE` and `LEARN_EXECUTOR_SUBMITS_PER_MINUTE` in `/etc/epoch-learn-executor.env` to change the limits. Limits live in memory and reset when the service restarts. Deploy this `service.py` together with the matching Next.js release, because older releases do not send `client`.
* **Responses.** Run results expose only visible-test names and pass flags. Submit returns counts plus the **names** of failed tests (checked against `testNames` in `tests.generated.json`), never their code or output; the workspace shows each name with the pack's advice. The runner also reports time and peak memory, which the service strips.

**Smaller test machines.** The slots, pool and per-job memory can be set in `/etc/epoch-learn-executor.env`. For a 1 vCPU / 2 GB / 20 GB test VPS use one slot, one warm container and 768 MB per job (the largest pack peaks at about 510 MB), and add the 2 GB swap file:

```dotenv
LEARN_EXECUTOR_SLOTS=1
LEARN_EXECUTOR_POOL=1
LEARN_EXECUTOR_MEMORY=768m
```

With one slot, requests are graded one at a time (roughly 40 jobs per minute; each job also pays for starting its replacement container), and the 30-request queue absorbs bursts. Expect up to 2–3× slower tests than the numbers below on a small VPS core.

Memory budget on a 4 GB VPS: about 0.7 GB for the OS, Docker, the service and the HTTPS proxy; about 0.3 GB for each waiting container; at most 1 GB for each running job.

To measure the image on the executor host, run from the repository root (it needs the generated files in `lib/learn/` and Docker access):

```sh
sudo LEARN_EXECUTOR_IMAGE=epoch-learn-runner:latest python3 -B -m executor.measure
```

Measured on an Apple-silicon Mac with Docker Desktop (2026-10-25, all 291 packs): a container imports the libraries in about 1.3–2 s and then idles at about 300 MB; every solution passed in Run and Submit mode and every starter failed; 873 jobs ran at 79 per minute with two slots; the median end-to-end request took 1.5 s and the slowest 2.7 s; the slowest test run used 1.0 s of CPU (`lm-tiny-gpt`, against the 10 s budget) and peak runner memory was 511 MB (against the 1 GB limit). Under sustained load each job pays for its replacement container's start, so throughput is bounded by container starts rather than tests. Repeat the measurement on the VPS, whose cores are slower.

It prints one progress line per pack (position, ok or the failed check, test time, CPU, memory, failures so far and an estimate of the time left), so pipe it through `tee` to keep a log. It grades every pack through the same pool, queue and limits — the reference solution in Run and Submit mode and the starter in Submit mode — and writes per-pack time and peak memory to `executor/measurements.json`. Every solution should pass and every starter should fail. Do not run it against a busy production service: it uses its own pool of containers alongside the service's.

Problem data is generated by `python3 scripts/generate-learn-demo.py`. When packs change, copy the regenerated `executor/tests.generated.json` to `/opt/epoch-learn-executor/tests.generated.json` and restart `epoch-learn-executor`. Rebuild the Docker image if `runner.py` or `requirements.txt` change (the image pins the versions the packs are validated against; `aimlgym/build/requirements-executor.txt` must match `requirements.txt`); copy an updated `service.py` to `/opt/epoch-learn-executor/service.py` when the host handler changes. Restart the executor after either change. For Case 3, rebuild the custom Caddy binary when updating Caddy or its DuckDNS plugin; the systemd override continues to point at `/usr/local/bin/caddy-duckdns`.

Run `python3 -B -m unittest executor.test_service` from the repository root for service authentication, response sanitization, warm-pool, queue-priority and queue-limit checks. Run `node --test scripts/learn.test.cjs` for Next.js submission and progress checks and the supplied factorial problem.
