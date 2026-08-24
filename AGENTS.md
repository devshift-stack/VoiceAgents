# AGENTS.md — LiveKit

Trigger: User sagt „projekt LiveKit“ → dieses Verzeichnis ist das einzige Arbeitsobjekt.

## Project root
`/Users/activi/Code/Projects/LiveKit`

Session-Start: `cd` hierher. Neueste `handoff_*/SESSION_RESUME.md` falls vorhanden. Dann live prüfen.

## Source of truth
| Was | Regel |
|-----|--------|
| APIs, Imports, Flags | MCP `livekit-docs` oder `lk docs` — nie Gedächtnis, nie lokale Doku-Dumps |
| Architektur / Tests | Skill `livekit-agents` |
| Simulations / Szenarien | Skill `livekit-simulations` |
| CLI | `lk` 2.18.2; `lk docs` = gleicher Inhalt wie Docs-MCP |

Kein `llms.txt` / `llms-full.txt` im Repo.

## Hard rules
1. Live-Verify first
2. Docs: overview/get-page vor search; search vor code-search
3. Jede Agent-Implementierung braucht Tests
4. Keine Prod-Writes / Cloud-Deploy ohne Freigabe
5. Deutsch, direkt, knapp, Tabellen
6. Verify-before-claim

## Skills
- `livekit-agents` — nur hier: `skills/livekit-agents/SKILL.md`
- `livekit-simulations` — nur hier: `skills/livekit-simulations/SKILL.md`
- `hermes-mcp-http` — nur wenn Docs-MCP kaputt ist

## Approval
| Aktion | Ohne Freigabe? |
|--------|----------------|
| Lesen, Docs, lokaler Entwurf, Tests | Ja |
| `lk cloud auth`, Deploy, Secrets | Nein |
