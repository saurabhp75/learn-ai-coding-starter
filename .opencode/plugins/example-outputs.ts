import { Plugin } from "@opencode/plugin"
import { spawn } from "node:child_process"
import { readdir } from "node:fs/promises"
import { basename, resolve } from "node:path"

const inputSchema = {
  type: "object",
  properties: {},
  additionalProperties: false,
} as const

const outputSchema = {
  type: "object",
  properties: {
    examples: {
      type: "array",
      items: {
        type: "object",
        properties: {
          name: { type: "string" },
          exitCode: { type: "integer" },
          firstLine: { type: "string" },
        },
        required: ["name", "exitCode", "firstLine"],
        additionalProperties: false,
      },
    },
  },
  required: ["examples"],
  additionalProperties: false,
} as const

type ExampleOutput = {
  name: string
  exitCode: number
  firstLine: string
}

function runExample(projectRoot: string, filePath: string, signal?: AbortSignal): Promise<ExampleOutput> {
  return new Promise((resolvePromise) => {
    let stdout = ""
    let settled = false

    const done = (exitCode: number) => {
      if (settled) return
      settled = true
      resolvePromise({
        name: basename(filePath),
        exitCode,
        firstLine: stdout.split(/\r?\n/, 1)[0] ?? "",
      })
    }

    const child = spawn("uv", ["run", "--no-active", "sloperator.py", filePath], {
      cwd: projectRoot,
      signal,
      stdio: ["ignore", "pipe", "ignore"],
    })

    child.stdout?.on("data", (chunk) => {
      stdout += chunk.toString()
    })
    child.on("error", () => done(1))
    child.on("close", (code) => done(code ?? 1))
  })
}

export default Plugin.define({
  id: "example-outputs",
  async setup(ctx) {
    const projectRoot = ctx.location.project.canonical

    await ctx.tool.transform((editor) => {
      editor.add({
        name: "example_outputs",
        description:
          "Run every examples/*.slop file and return each filename, exit code, and first stdout line.",
        input: inputSchema,
        output: outputSchema,
        options: { codemode: false },
        execute: async (_input, context) => {
          const examplesDir = resolve(projectRoot, "examples")
          const entries = await readdir(examplesDir, { withFileTypes: true })
          const files = entries
            .filter((entry) => entry.isFile() && entry.name.endsWith(".slop"))
            .map((entry) => entry.name)
            .sort()

          const examples = await Promise.all(
            files.map((name) => runExample(projectRoot, resolve(examplesDir, name), context.signal)),
          )

          return {
            content: JSON.stringify({ examples }, null, 2),
            output: { examples },
          }
        },
      })
    })
  },
})
