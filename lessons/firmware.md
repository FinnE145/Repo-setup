# Firmware lessons

Read by the phases in repos with the `firmware` module, the parts that touch the work at hand — never every turn. Distilled from desk-bridge's dashboard (an ESP32-S3 RGB display with LVGL 9, a Pico 2 input module on I2C, a Windows laptop host), 2026-10-13 to 10-16. Board-specific facts belong in the repo's `docs/firmware/board-notes.md`, not here.

## Display and LVGL
- **A page change paints top to bottom when LVGL renders tile by tile straight onto the panel.** Rendering the whole change into one full-size PSRAM buffer (direct render mode) and copying the changed rows to the panel's framebuffer in one go makes it appear complete, at the price of a tap being answered about 30 ms later. Use one buffer, not two: with two, LVGL also copies every change into the spare. Write back only the rows copied, not the whole framebuffer. Keep it behind a flag so the two can be compared by eye.
- **With no LVGL theme every object starts bare**, so one helper that strips styles, scrolling and clicking, and a few for labels, icons and round buttons, keep the screens short. A label that must end in "..." needs a fixed height as well as a width, or it wraps instead.
- **A pressed child object does not pass the press to its parent**, so decoration inside a tappable object is made non-clickable.
- **Only set what changed.** `lv_label_set_text` and style setters invalidate even when the value is the same; wrapping them to compare first keeps redraws to what actually changed.
- **A highlight made by changing an object's fill is painted over by any refresh that sets the same fill**: the compare-first helpers write the base colour back. Re-apply the highlight after every refresh, or draw it on an object nothing else touches. (A border-based ring has the opposite flaw: LVGL borders take layout space and shift the content a couple of pixels, which wrecks small icons. An outline would not shift anything.)
- **A frame for a lit fill must sit under the content.** A bare overlay made after the content hides it when lit; make it the first child so the fill is drawn first.
- **Rounded text and icon assets without installing anything:** a font can come from the LVGL repo's own TTF drawn by Tiny TTF at any size from one embedded array, and alpha-only icon bitmaps can be made from SVG with a small numpy rasterizer (flatten curves and arcs, even-odd or nonzero fill, supersample). One weight only, so "bold" has to be faked by drawing text twice a pixel apart or by colour.
- **A touch panel library's rotation constants may not mean what they say**: check all four corners with a throwaway screen before building on it (one library's "normal" mirrored both axes).

## USB and the host
- **A host's sleep is not visible on USB by default.** A laptop with Modern Standby kept the USB bus running through standby on AC, and suspended it only after about 46 s on battery. Measure on the real host, on battery and on the charger, for minutes rather than seconds. A tiny helper on the host listening for display off/on was instant on every path.
- **Watch the bus, not only the stack's flags.** Logging the USB frame counter directly (it advances every 1 ms while the host runs the bus) separated "the host kept the bus up" from "the stack didn't report it".
- **A USB device being unplugged or plugged in looks like a sleeping host for a moment.** Pulled out, the device lived a few milliseconds more and saw its bus go quiet (longer on a slow pull: the data pins break before the power pins); plugged in, it was unmounted until the host set it up, about 2 s. Read the host's sleep from USB only after it has held for a few seconds, and give a faster signal (a host helper) its own path.
- **A Windows serial handle kept open can go dead silently** when the device re-enumerates (reflashed, replugged): writes still succeed and nothing arrives. Reopen it periodically. Opening it on demand instead was too slow at Modern Standby entry: Windows froze the process before the line went out.
- **An app holding the device's port stops the upload** from resetting it into the bootloader ("No drive to deploy"). Stop it first, or use the bootloader button.
- **The board's serial port moves** between USB ports: list the boards before every upload. Opening the port may reset the board.

## Wiring and power
- **Pin labels on the underside mirror the columns.** "Left" and "right" flip between the person reading the labels and the person counting from the top. Give wiring by label or by a printed corner mark; a photo of the wiring finds the mistake at once.
- **A reset on a button press is a wiring clue**: the switch is on a reset or enable pin (RUN, on a Pico). Check the uptime after each test: a small one means the device restarted.
- **Dual power needs its own diode.** Powering a dev board from a rail and its USB at once usually needs a Schottky diode on the rail's side: the board's built-in diode protects only its own USB port. Check the board's datasheet before calling it safe (a session got this wrong).
- **On a shared bus, send cumulative counters, not events.** A dropped or corrupt read then loses nothing: the next good one carries the difference. And test that the new device unpowered doesn't hold the bus down.

## State the device writes on the server
- **A QoS 1 resend can put an older write back as the retained value.** The ESP-IDF MQTT client sent each write twice; when a newer write went out in between, the broker kept the older one, and changes were lost until a reboot. Two things fixed it: the device writes its current value again whenever a live copy of its own topic differs from its last write, and changes made together go out as one write.
