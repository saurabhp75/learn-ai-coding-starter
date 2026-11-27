import { Plugin } from "@opencode/plugin"
import { appendFile, mkdir } from "node:fs/promises"
import { dirname, resolve } from "node:path"

const loggedTools = new Set(["edit", "write", "patch"])

export default Plugin.define({
  id: "edit-log",
  async setup(ctx) {
    const logPath = resolve(ctx.location.project.canonical, "logs/plugin-tools.log")

    await ctx.tool.hook("execute.after", async (event) => {
      if (event.status !== "completed") return
      if (!loggedTools.has(event.tool)) return

      await mkdir(dirname(logPath), { recursive: true })
      await appendFile(logPath, JSON.stringify({ tool: event.tool, status: "completed" }) + "\n")
    })
  },
})
