# Module: laptop

**Applies when** the repo is worked on from Finn's Windows laptop (the G14) in the Claude desktop app: code edited, built or run there. Distilled from desk-bridge's firmware sessions.

## What setup asks
Nothing beyond confirming it applies; the traps below are the machine's, not the repo's.

## What it adds
- **CLAUDE.md**, a section at the `flow:modules` marker:
  "## Laptop (Windows)
  - **The Claude desktop app is MSIX-packaged**: writes to AppData or HKCU from your shell tools are silently redirected and nothing else sees them. Never install a toolchain or library under AppData. Persistent settings (`setx`, registry) go to me as commands for the app's Terminal panel or a normal terminal, which aren't redirected.
  - **Smart App Control blocks executables compiled on this machine** (event log IDs 3033/3077; no per-folder exclusions), though not reputable downloaded toolchains, and scripts on a trusted interpreter run. Check before the first test whether what the repo builds can run here; if not, run it on fe-pro over SSH. Don't suggest turning the policy off, but **tell me every time it blocks something**, even when a workaround exists: what it blocked and what it cost. I'm deciding whether to turn it off, and that tally is what decides it.
  - **Write edit scripts to a file with the file tool and run that**: through the shell tool's heredocs, a `\0` came out as a real NUL and made git treat a source file as binary."
