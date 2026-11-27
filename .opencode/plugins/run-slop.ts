import { Plugin } from "@opencode/plugin"
import { spawn } from "node:child_process"
import { resolve } from "node:path"

const inputSchema = {
  type: "object",
  properties: {
    path: {
      type: "string",
      description: "Path to the .slop file to run, relative to the project root or absolute.",
    },
  },
  required: ["path"],
  additionalProperties: false,
} as const

const outputSchema = {
  type: "object",
  properties: {
    stdout: { type: "string" },
    stderr: { type: "string" },
    exitCode: { type: "integer" },
  },
  required: ["stdout", "stderr", "exitCode"],
  additionalProperties: false,
} as const

type RunResult = {
  stdout: string
  stderr: string
  exitCode: number
}

function runSloperator(projectRoot: string, filePath: string, signal?: AbortSignal): Promise<RunResult> {
  return new Promise((resolvePromise) => {
    let stdout = ""
    let stderr = ""
    let settled = false

    const done = (exitCode: number) => {
      if (settled) return
      settled = true
      resolvePromise({ stdout, stderr, exitCode })
    }

    const child = spawn("uv", ["run", "--no-active", "sloperator.py", filePath], {
      cwd: projectRoot,
      signal,
      stdio: ["ignore", "pipe", "pipe"],
    })

    child.stdout?.on("data", (chunk) => {
      stdout += chunk.toString()
    })
    child.stderr?.on("data", (chunk) => {
      stderr += chunk.toString()
    })
    child.on("error", (error) => {
      stderr += `${error.message}\n`
      done(1)
    })
    child.on("close", (code) => {
      done(code ?? 1)
    })
  })
}

export default Plugin.define({
  id: "run-slop",
  async setup(ctx) {
    const projectRoot = ctx.location.project.canonical

    await ctx.tool.transform((editor) => {
      editor.add({
        name: "run_slop",
        description: "Run a SlopLang (.slop) file with Sloperator and return stdout, stderr, and the exit code.",
        input: inputSchema,
        output: outputSchema,
        options: { codemode: false, permission: "run_slop" },
        execute: async (input, context) => {
          const filePath = resolve(projectRoot, (input as { path: string }).path)
          const result = await runSloperator(projectRoot, filePath, context.signal)
          return {
            content: JSON.stringify(result, null, 2),
            output: result,
          }
        },
      })
    })

    await ctx.tool.transform((editor) => {
      editor.update("run_slop", (tool) => {
        tool.description +=
          " Use this tool to run individual .slop examples when checking language behavior. Use the test suite for regression testing."
      })
    })
  },
})
