---
name: cronjob-provider-switching
description: Workflow for migrating token‑dependent Hermes cron jobs to token‑free providers (e.g., OpenRouter) to avoid "No access token found" errors.
category: devops
---

# Cronjob Provider Switching Skill

## Purpose
Provides a reliable workflow for identifying and migrating Hermes cron jobs that depend on external token‑based providers (e.g., Nous/xAI OAuth) to token‑free alternatives such as OpenRouter, preventing “No access token found” failures.

## When to Use
- A cron job fails with an error indicating missing access token for a provider (Nous, xAI‑oauth, etc.).
- You want to eliminate manual `hermes model` re‑authentication for scheduled jobs.
- You are auditing cron jobs for token dependencies and wish to switch them to a stable, free provider.

## Steps
1. **List cron jobs**  
   `cronjob action=list`  
   Identify jobs where `provider` is `nous` or `xai-oauth` and `last_status` is `error` with a token‑related message.

2. **Confirm the failing provider**  
   Inspect the job’s `provider` and `model` fields. Typical failing combos:  
   - `provider: nous`, `model: grok-4.3`  
   - `provider: xai-oauth`, `model: grok-4.3` (internal tooling)

3. **Choose a token‑free replacement**  
   - Preferred: OpenRouter with a free model (e.g., `owl-alpha`, `llama-4-maverick:free`).  
   - Ensure the model supports the required capabilities (reasoning, tool use) for the job’s prompt.

4. **Update the job**  
   ```bash
   cronjob action=update job_id=<JOB_ID> \
       model="openrouter/<MODEL>:free" \
       provider="openrouter"
   ```
   Keep `schedule`, `profile`, `deliver`, `enabled_toolsets`, `workdir`, and other fields unchanged unless you intend to modify them.

5. **Verify the change**  
   Run `cronjob action=list` again and confirm the new `provider` and `model` appear.

6. **Test immediately (optional)**  
   ```bash
   cronjob action=run job_id=<JOB_ID>
   ```
   Check that `last_status` becomes `ok` and that the job completes its intended work.

7. **Monitor**  
   After the next scheduled run, verify `last_status` stays `ok`. If it reverts to `error`, re‑examine the prompt for provider‑specific assumptions and adjust accordingly.

## Pitfalls & How to Avoid Them
- **Assuming the model is interchangeable** – Some prompts may rely on provider‑specific behaviors (e.g., function calling, JSON mode). After switching, run a quick test and inspect the output; if quality degrades, consider a different model or retain the original provider with a refreshed token.
- **Forgetting to update related auxiliary jobs** – Token‑related failures can appear in multiple cron jobs (truth audit, maintenance, infrastructure hygiene). Always run the list and update all `nous`/`xai-oauth` jobs in one batch.
- **Overlooking the `default` profile** – Jobs under the `default` profile may inherit the global `xai-oauth` setting; check `default/config.yaml` if you see persistent token errors.
- **Neglecting to clear cached tokens** – After switching, old tokens remain in `~/.hermes/auth.json`. They are harmless but can be cleared if desired; they do not affect OpenRouter jobs.
- **Assuming OpenRouter is always free** – Verify the model’s pricing on OpenRouter; some models are paid. Use the `:free` suffix or check the OpenRouter catalog.

## References
- `references/openrouter-free-models.md` – list of free models currently available on OpenRouter.
- `references/token-error-patterns.md` – common error messages indicating missing Nous/xAI tokens.

## Related Skills
- `cronjob-management` – general cron job creation, listing, and removal.
- `hermes-agent` – configuring Hermes provider settings.
- `devops/artifact-pyramids` – for jobs that generate artifact reports after provider switch.

## Change Log
- 2026-06-09: Initial creation based on session fixing Nous‑token failures for DABT and infrastructure cron jobs.
