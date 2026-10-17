# Module: firmware

**Applies when** the repo carries firmware for a microcontroller board (Arduino, ESP-IDF, Pico SDK, …), usually beside the server it talks to. Distilled from desk-bridge's dashboard (an ESP32-S3 display with LVGL, and a Pico 2 input module), roadmap steps E and E2, 2026-10-13 to 10-16. Usually comes with `two-checkouts` (the board is plugged into a different machine from the server code) and, on Finn's laptop, `laptop`. The phase-notes point at `lessons/firmware.md` for the hardware and library detail.

## What setup asks
- The board(s), and where the schematic is (a vendor PDF, a link). Pins come from it.
- Which machine the board is plugged into, and whether the rest of the repo is worked on there (if not, add `two-checkouts`).
- The toolchain with exact versions (CLI, core, board identifier, libraries) and where it's installed.
- What the firmware talks to (a broker, an HTTP API, a host helper over serial) and how it authenticates.
- Whether flash writes disturb anything on this board. If nobody knows, it's a Plan question to measure: it decides whether the device keeps any state of its own.

## What it adds
- **Where the code lives:** the firmware goes in its own folder (`firmware/`) **in the same repo as the server it talks to**, not a separate repo. The contract, the ACL, the CA and shared lists (icon names, say) then live in one place, and nothing is copied across to drift.
- **`firmware/CLAUDE.md`**, for sessions on the machine the board is plugged into:
  "# firmware/ — {{BOARD}} ({{MACHINE}} sessions)

  {{What it is, its spec, where it's built and flashed. Sessions on this machine work in this folder.}}

  The root `CLAUDE.md` applies here too, except {{the sections that hold only on the other machine}}. The board's reference (pins from the schematic, timings, measured results) is `docs/firmware/board-notes.md`; read the section you need, not the whole file.

  ## Rules
  - **Serial output is a log**, and it ends up in your transcript: the root `CLAUDE.md`'s content rules for logs apply to it, and nothing from `secrets.h` is ever printed.
  - **`secrets.h` is never committed or printed** (`firmware/**/secrets.h` is gitignored); `secrets.h.example` holds placeholders. Without a `secrets.h` the network code compiles to nothing and the UI runs on sample data.
  - **Pins come from the schematic** (board notes), never from a vendor example alone.
  - **Untested hardware gets a tiny test sketch first**, and I look at it before real code relies on it. If it fails, stop and ask.
  - **Every decision lives in plain C++** with no Arduino, display-library or vendor SDK headers, so it compiles natively and is tested with the host's compiler. The hardware-facing code stays thin.
  - **Every value I may want to tune** goes in `config.h` with a name and a comment, not scattered as literals.
  {{- **Nothing is written to flash** (no NVS, `Preferences`, filesystem or OTA): <the measured reason>. What the board must remember lives on the server, read back after a reboot. — only when measured so}}

  ## Toolchain
  {{exact versions, install paths, board identifier}}

  ## Commands
  {{find the port (it can move between USB ports: list boards before every upload), build and flash, serial, native tests, mutation — each slow one with its measured time}}"
- **Root `CLAUDE.md`:**
  - Tech Stack: a firmware bullet (board, toolchain and library versions, or a pointer to `firmware/CLAUDE.md` for the exact ones).
  - Codebase Map: a `firmware/` bullet with its invariants (what it never writes, what it alone publishes), pointing at `firmware/CLAUDE.md`.
  - Keep It Simple, after the security bullet:
    "- **Holding a device gives no more power than standing at it.** Physical access beats everything, so a credential stored on the device is not a weakness to engineer around: one account per device, least privilege, and a lost one is cut off by changing its password.
    - **Whatever a device sends is untrusted input**: the server validates it strictly (size first, then known fields, bounded values), and config changes only on the server, never over the wire."
- **`docs/firmware/board-notes.md`**, a stub: title plus "Reference for {{BOARD}}: the pin map from the schematic, the toolchain, display timing, measured results. Measured or documented facts only, each dated."
- **`.gitignore`:** `firmware/**/secrets.h`.
