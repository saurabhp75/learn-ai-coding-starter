---
description: Serve the SlopLang playground on a port (default 8080) after checking the port is free
---

Start the SlopLang playground.

Port: $ARGUMENTS (use 8080 if that is empty)

## Current listeners

!`lsof -nP -iTCP -sTCP:LISTEN`

## Steps

1. Decide the port: the port above if provided, otherwise `8080`.
2. Use the listener output above to check whether that port is already taken. If it is, do not start a second server: identify the process with `lsof -nP -iTCP:<port> -sTCP:LISTEN`, check whether it is already a Sloperator playground by fetching `http://localhost:<port>/` (the playground serves its page at `/`), and report what you found. If it is a different process, stop and ask before killing anything.
3. If the port is free, start the server in the background from the project root, without blocking the session:

```bash
uv run playground/server.py <port>
```

   Run it with the background shell tool so the command returns immediately.
4. Confirm it came up: check the background output for the "SlopLang playground running at http://localhost:<port>" line, or fetch `http://localhost:<port>/`.
5. Report the URL and how to stop the server.

Keep the port as a plain number from the user; never put it inside a shell-injection block.
