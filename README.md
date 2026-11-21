# curly-succotash — Builders Mech Royale

An original Python bot for the [Builders Buildathon: Mech Royale](https://www.joinbuilders.org/buildathon/tracks/builders), using the official mechfight/1 JSON-lines protocol. Objective: maximize placement points (16 minus finishing place), not kills.

## How it plays

- **Survival:** tries to avoid 2v1 encounters, breaks line of sight when injured, preserves energy for emergency escapes, evades incoming rounds and predicted mortar impacts, and sidesteps visible charged lasers.
- **Map awareness:** reads the official terrain and building footprints from \`/arena/v2\`, inflates collision obstacles, and runs bounded A* planning across multiple decisions. Direct paths use inexpensive ray checks. Includes limited wall-stuck recovery.
- **Circle management:** moves toward future safe zones before the shrink is dangerous, looks for reachable cover and favorable holding points, and tracks the center in the last circles.
- **Selective combat:** faces attackers to avoid rear damage, leads gun rounds with a projectile-intercept calculation, charges/releases lasers with torso alignment, fires lightning at close range, and uses ballistic mortar pitch where viable. Gun triggers anticipate the next 0.1-second action window.
- **Economy:** prefers early laser loot, picks up unclaimed cubes, opportunistically captures supplies, and applies defensive upgrades first. Avoids prolonged drone farming while injured.
- **Modes:** infers whether enemies are independently dying; it plays cautiously when a free-for-all is detected, but accepts worthwhile duels against individual practice hunters.
- **Robustness:** standard-library-only runtime, controlled pathfinding workload, and the official wrapper's fallback if a decision raises.

## Files

| File | Role |
| --- | --- |
| \`bot.py\` | Policy, enemy/loot memory, combat and movement |
| \`arena.py\` | Terrain loading, obstacle grid, incremental pathfinding |
| \`mechfight.py\` | Official Python kit protocol wrapper, preserved verbatim |
| \`Dockerfile\` | linux/amd64 submission runtime (UID 65534, Python 3.13.9) |
| \`.github/workflows/check.yml\` | Download kit and run protocol + Docker conformance checks |

## Build and validate

Download the [official starter kit](https://www.joinbuilders.org/buildathon/tracks/builders/files/mechfight-kit.tar.gz) and extract it separately. Let \`KIT\` be the path to its \`mechfight-kit\` folder.

\`\`\`bash
python3 -m py_compile bot.py arena.py mechfight.py
python3 "$KIT/check/check.py" --map-dir "$KIT/arena" -- python3 -u bot.py

docker build --platform linux/amd64 -t curly-mech .
python3 "$KIT/check/check.py" --map-dir /arena -- \
  docker run --rm -i --network none --cpus 1 --memory 512m \
  --read-only --tmpfs /tmp:rw,size=64m --user 65534:65534 \
  -v "$KIT/arena:/arena:ro" curly-mech
\`\`\`

**Important:** \`check/check.py\` replays 300 fixed observations and checks protocol correctness and runtime latency. It **does not calculate a placement score**; only the organizer's practice submission runs 48 private games. An official practice score has not been independently established by this README. Local third-party simulators do not reproduce the private house-bot squad exactly.

For an official practice run, submit this public repository URL on the Builders site. The selected commit must be kept fetchable, public and buildable through results publication. Submit only tested commits. The event cutoff is November 23, 2026, at 00:00 Singapore time.

This repository is licensed MIT. The kit's unchanged protocol wrapper remains attributed to the organizer.
