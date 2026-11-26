# Academic Writing Debate (v0.1)

Codex Desktop orchestrates real Gemini Carbon through Antigravity CLI and Claude Opus through your existing Claude Code login. The original codex-claude-debate repository remains unchanged. No extra API key is configured by this skill; actual subscription access and quotas depend on your accounts.

## Windows setup

1. Install Antigravity CLI using the official installer if `agy --version` fails. Open a new PowerShell, run `agy`, sign in with your eligible Google account, and run `agy models`. See https://antigravity.google/docs/getting-started?tab=cli and https://antigravity.google/docs/cli/headless/.
2. Test `agy -p "Reply with exactly GEMINI_OK" --model gemini-4-carbon-high --output-format json`. Confirm success; `claude auth status` checks your existing Claude login. Do not paste tokens into chat. Do not configure API-key billing unless you explicitly intend it.
3. Extract this package and run `install.cmd`. It copies a separate skill to `%USERPROFILE%\.agents\skills\academic-writing-debate` and a text-only custom Antigravity agent to `%USERPROFILE%\.gemini\config\agents\academic-writing-reviewer\agent.md`. Existing differing files are not overwritten. Restart Codex if necessary.
4. In PowerShell run:
   ```powershell
   py -3 "$HOME\.agents\skills\academic-writing-debate\scripts\bridge.py" check --provider gemini
   py -3 "$HOME\.agents\skills\academic-writing-debate\scripts\bridge.py" check --provider claude
   ```
   If executable discovery fails, set `AGY_BIN` or `CLAUDE_BIN` to its absolute path. If the custom agent is not recognized, check `agy agents` and the installed CLI version. Do not disable security permissions to work around errors.
5. Open your paper workspace in Codex and invoke `$academic-writing-debate`. Explicitly authorize sharing the selected unpublished excerpts with both providers only if permitted by your research collaborators and applicable data policy. Add `.academic-review/` to the project's local `.git/info/exclude` or `.gitignore` before creating transcripts.

Default requested models: `gemini-4-carbon-high` and `opus`. Override with `AW_GEMINI_MODEL` and `AW_CLAUDE_MODEL` if necessary after verifying actual model availability. No silent fallback. The orchestrator is Codex, not an autonomous Python pipeline: Python performs genuine external calls and checks; Codex makes substantive decisions and coordinates the stages.

## Privacy and limits

The bridge sends only supplied prompts and uses a fresh temporary working directory. The Antigravity custom agent specifies no tools; Claude CLI disables builtin tools and disallows MCP tools. These are application controls, not an independently verified OS sandbox. Local configuration, CLI versions and provider data policies may affect behavior. Inspect settings and use a controlled environment before sending confidential work. Raw logs contain manuscript content. SHA-256 checks versions, not mathematical validity. The LaTeX audit is a limited regex check, not a parser or proof checker. No original manuscript changes or Git publishing occur automatically. Do not claim provider authentication or remote access has been tested without running the local check.

## Offline tests

`py -3 -m unittest discover -s tests -v` from the extracted directory. Tests use mock CLI results; real calls require your authenticated Windows host. No API keys are stored in the package.

## Known limitations (v0.1)

- A live Gemini Carbon smoke test has succeeded on Windows. The live Claude smoke test encountered a provider usage limit (HTTP 429); end-to-end three-model review has not yet been verified. Account access may vary.
- `check` uses a temporary directory that is removed when the command finishes. To retain troubleshooting output, run `ask` with a harmless, explicitly authorized test prompt and a fresh output path. Check Claude usage limits before retrying.
- If `install.cmd` closes without a visible result, run `py -3 install.py` from the extracted repository directory in PowerShell to display installation errors.

## License

[MIT License](LICENSE), Copyright (c) 2026 Knarf-Z.
