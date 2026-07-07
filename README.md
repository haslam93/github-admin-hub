# 🛠️ GitHub Enterprise Admin Hub

**An interactive guide to GitHub Enterprise administration** — enterprise & org setup, enterprise teams, cost centers, budgets, **AI credit pooling**, Copilot seat management, AI policies, and the full billing/Copilot REST API surface.

🔗 **Live app:** GitHub Pages → `https://haslam93.github.io/github-admin-hub/` · Azure Static Web Apps mirror (see [Deployments](#deployments))

> All content is verified against [GitHub Docs](https://docs.github.com/en/enterprise-cloud@latest) and the [GitHub Changelog](https://github.blog/changelog/) as of **July 2026**, and is **auto-refreshed weekly** by a scheduled workflow ([details below](#-weekly-auto-update-workflow)).

---

## ✨ What's inside the app

| Tab | What you'll learn |
|---|---|
| **Overview** | The whole landscape in one diagram — hierarchy + the three pillars: attribution (cost centers), control (budgets), caps (AI credit pools) |
| **Enterprise & Orgs** | EMU vs classic, enterprise/org roles, adding orgs, policy inheritance (enforce / delegate / disable) |
| **Enterprise Teams** | GA (June 2026) cross-org teams: Copilot licensing, org membership, cost attribution, ruleset bypass, SCIM sync, limits |
| **Cost Centers & Budgets** | Who manages them, the 4 resource types, attribution priority (user → enterprise team → org), budget types/scopes, hard stops, 75/90/100% alerts |
| **AI Credits** | Premium requests → AI credits (1 credit = $0.01), included amounts (1,900 Business / 3,900 Enterprise), enterprise-wide pooling, and the **July 2, 2026 AI credit pool caps for cost centers** |
| **Copilot Seats** | The two licensing paths (enterprise-direct Business vs org enablement), deduplication, mixed plans, metrics API |
| **Policies** | AI Controls tab, per-policy modes, multi-org conflict resolution, Agent Control Plane |
| **Scenario Lab 🧪** | Interactive simulator: assign licenses to cost centers, toggle pool caps (block vs roll-to-paid), set budgets, drag usage sliders, watch alerts fire and the bill compute — with 3 ready-made presets |
| **API Explorer** | 40+ endpoints (cost centers, budgets, usage, Copilot seats enterprise/org, metrics, enterprise teams) with auth, payloads and copyable `curl` |
| **Changelog** | Live view of `data/changelog.json`, refreshed weekly |

## 🚀 Quick start

It's a **zero-build static app** — a single `index.html`.

```bash
git clone https://github.com/haslam93/github-admin-hub.git
cd github-admin-hub
# open index.html, or serve it:
python -m http.server 8080   # → http://localhost:8080
```

Light/dark theme follows your OS, or force it with `?clawpilotTheme=dark`.

## 🧠 Key concepts in 60 seconds

```text
Enterprise account
├── Organizations ──── repos, org teams, members
├── Enterprise teams ─ cross-org groups (IdP-synced on EMU)
├── Unaffiliated users (can still hold Copilot Business!)
└── Billing platform
    ├── Cost centers ..... WHO spent it   (users, orgs, repos, ent. teams)
    ├── Budgets .......... HOW MUCH may they spend (metered $, hard stop optional)
    └── AI credit pools .. HOW MUCH of the shared included credits may a
                           cost center draw (auto-sized by its own licenses)
```

- **Included AI credits pool enterprise-wide** — Business seats bring 1,900 credits/user/mo, Enterprise seats 3,900. One team *can* drain everyone's credits… unless you cap it.
- **AI credit pools (July 2, 2026):** set `ai_credit_pool_enabled: true` on a cost center and its draw is capped at what its own licenses fund. On cap: **block** or **roll into paid usage** ($0.01/credit) where **budgets** take over.
- **Budgets alert at 75 / 90 / 100%** and only stop usage if you enable the hard stop. User-level budgets are *always* hard stops.
- **An enterprise budget is not a bill cap**: max bill = license fees + budget.

## 📂 Repository layout

```text
├── index.html                        # the entire app (self-contained, no build)
├── data/changelog.json               # auto-updated changelog feed data
├── scripts/update_changelog.py       # RSS watcher (stdlib-only Python)
├── staticwebapp.config.json          # Azure SWA config
└── .github/workflows/
    ├── changelog-watch.yml           # weekly cron → updates data + README
    ├── deploy-pages.yml              # GitHub Pages deploy on push
    └── azure-swa.yml                 # Azure Static Web Apps deploy on push
```

## 🔄 Weekly auto-update workflow

Every **Monday 06:00 UTC** (`changelog-watch.yml`):

1. Fetches the GitHub Changelog RSS feeds (main + `copilot` + `enterprise` labels)
2. Keyword-filters for admin/billing topics (cost centers, budgets, AI credits, seats, enterprise teams, policies…)
3. Merges new entries into [`data/changelog.json`](data/changelog.json)
4. Rewrites the [Latest changelog](#-latest-relevant-changelog-entries) section below
5. Commits — which triggers redeploy of **both** GitHub Pages and Azure SWA

Run it on demand from the **Actions** tab (`workflow_dispatch`).

## 📰 Latest relevant changelog entries

<!-- CHANGELOG:START -->

_Last checked: 2026-07-07T10:16:50+00:00 (auto-updated weekly)_

- **2026-07-02** — [Improved accuracy and coverage in Copilot usage metrics reports](https://github.blog/changelog/2026-07-02-improved-accuracy-and-coverage-in-copilot-usage-metrics-reports) `Improvement` `account management` `copilot`
- **2026-07-02** — [Copilot agent session streaming is now in public preview](https://github.blog/changelog/2026-07-02-copilot-agent-session-streaming-is-now-in-public-preview) `Improvement` `copilot` `enterprise management tools`
- **2026-07-02** — [Cost centers now support AI credit pools](https://github.blog/changelog/2026-07-02-cost-centers-now-support-included-usage-caps) `Release` `account management` `copilot`
- **2026-07-01** — [Enterprises can default to auto model selection](https://github.blog/changelog/2026-07-01-enterprises-can-default-to-auto-model-selection) `Improvement` `client apps` `copilot`
- **2026-07-01** — [Enterprise managed-settings.json is generally available](https://github.blog/changelog/2026-07-01-enterprise-managed-settings-json-is-generally-available) `Release` `client apps` `copilot`
<!-- CHANGELOG:END -->

## ☁️ Deployments

| Target | Trigger | Workflow |
|---|---|---|
| **GitHub Pages** | push to `main` | `deploy-pages.yml` |
| **Azure Static Web Apps** | push to `main` | `azure-swa.yml` (needs `AZURE_STATIC_WEB_APPS_API_TOKEN` secret) |

## 📚 Primary sources

- [Cost centers (concepts)](https://docs.github.com/en/enterprise-cloud@latest/billing/concepts/cost-centers) · [cost center allocation](https://docs.github.com/en/enterprise-cloud@latest/billing/reference/cost-center-allocation)
- [Changelog: Cost centers now support AI credit pools (2026-07-02)](https://github.blog/changelog/2026-07-02-cost-centers-now-support-included-usage-caps/)
- [Budgets & alerts](https://docs.github.com/en/enterprise-cloud@latest/billing/concepts/budgets-and-alerts) · [budgets for usage-based billing](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/billing/budgets-for-usage-based-billing)
- [REST: cost centers](https://docs.github.com/en/enterprise-cloud@latest/rest/billing/cost-centers) · [budgets](https://docs.github.com/en/enterprise-cloud@latest/rest/billing/budgets) · [usage](https://docs.github.com/en/enterprise-cloud@latest/rest/billing/usage) · [Copilot user management](https://docs.github.com/en/enterprise-cloud@latest/rest/copilot/copilot-user-management) · [enterprise teams](https://docs.github.com/en/rest/enterprise-teams/enterprise-teams)
- [Enterprise Teams GA (2026-06-04)](https://github.blog/changelog/2026-06-04-enterprise-teams-is-now-generally-available/) · [Copilot Business in enterprise GA (2025-10-28)](https://github.blog/changelog/2025-10-28-managing-copilot-business-in-enterprise-is-now-generally-available/) · [AI Controls GA (2026-02-26)](https://github.blog/changelog/2026-02-26-enterprise-ai-controls-agent-control-plane-now-generally-available/)

---

*Educational reference — not affiliated with GitHub, Inc. Verify pricing and behavior against official docs before making purchasing decisions.*
