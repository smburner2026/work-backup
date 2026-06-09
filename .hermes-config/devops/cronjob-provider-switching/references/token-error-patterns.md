# Common Token‑Related Error Messages in Hermes

- "RuntimeError: No access token found for Nous Portal login. Run hermes model to re-authenticate."
- "xAI token refresh failed. Response: {\"error\":\"invalid_grant\",\"error_description\":\"Refresh token has been revoked\"}"
- "credential_pool_refresh_failure" (seen in auth.json under xai-oauth)
- "provider: nous" jobs failing with "Unauthorized" or "401" from inference-api.nousresearch.com
- "provider: xai-oauth" jobs failing with "403 Forbidden" or "invalid_grant" during token refresh

These messages indicate that the job’s provider requires a valid OAuth token that is missing, expired, or revoked.