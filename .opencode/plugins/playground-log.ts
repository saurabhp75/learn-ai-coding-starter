import { Plugin } from "@opencode/plugin"
import { appendFile, mkdir } from "node:fs/promises"
import { dirname, resolve } from "node:path"

export default Plugin.define({
  id: "playground-log",
  async setup(ctx) {
    const logPath = resolve(ctx.location.project.canonical, "logs/plugin-playground.log")

    await ctx.shell.hook("create.before", async (event) => {
      if (!event.command.includes("playground/server.py")) return

      await mkdir(dirname(logPath), { recursive: true })
      await appendFile(logPath, "playground shell request\n")
    })
  },
})
