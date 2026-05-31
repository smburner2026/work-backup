# Cloud Storage — AI Agentic Friendly Options

## Ranking by Free Storage + AI Friendliness

| Rank | Service | Free Tier | AI Agentic Score | Notes |
|------|---------|-----------|------------------|-------|
| **1** | **Backblaze B2** | 10GB | ★★★★★ | S3-compatible API, excellent CLI (rclone, b2 CLI), programmatic control |
| **2** | **Cloudflare R2** | 10GB | ★★★★★ | S3-compatible API, excellent CLI (rclone), free egress |
| **3** | **Google Drive** | 15GB | ★★★☆☆ | Good API, CLI tools (rclone, gdrive), OAuth setup required |
| **4** | **MEGA** | 20GB | ★★☆☆☆ | API exists, CLI tools (megatools), less documented |
| **5** | **pCloud** | 10GB | ★★☆☆☆ | API exists, CLI tools (pcloudcc), less documented |
| **6** | **OneDrive** | 5GB | ★★★☆☆ | Good API, CLI tools (rclone), Microsoft ecosystem |
| **7** | **Dropbox** | 2GB | ★★★☆☆ | Good API, CLI tools, but very limited free tier |

## What "AI Agentic Friendly" Means

- **API access** — Can be programmatically controlled (upload, download, list, search)
- **CLI tools** — Can be used from terminal (rclone, native CLI)
- **S3-compatible** — Standard API that works with many tools
- **G-Brain integration** — Can upload files and get URLs
- **Scriptable** — Can be automated with Python, bash, etc.

## Recommendation: Two-Tier Strategy

### Tier 1: Google Drive (15GB free) — Primary
**Use for:**
- Sharing with family (easy sharing features)
- General-purpose storage
- Documents that need to be easily accessible

**Why:**
- Most user-friendly for family sharing
- 15GB free is generous
- Good API for AI integration (with OAuth setup)
- CLI tools: `rclone`, `gdrive`

**AI Integration:**
- Google Drive API (Python, Node.js, etc.)
- `rclone` for CLI automation
- G-Brain file upload (via API or manual upload)

### Tier 2: Backblaze B2 (10GB free) — Secondary
**Use for:**
- Raw files (PDFs, documents, images)
- Backup of critical files
- Long-term archive
- Programmatic access for AI agents

**Why:**
- S3-compatible API (industry standard)
- Excellent CLI tools (`rclone`, `b2`)
- Very cheap if you need more storage ($0.005/GB/month)
- No egress fees
- Most AI agentic friendly

**AI Integration:**
- S3-compatible API (Python boto3, AWS CLI, etc.)
- `rclone` for CLI automation
- G-Brain file upload (via S3 API or manual upload)
- Scriptable for automated workflows

## Total Free Storage: 25GB

| Service | Free Tier | Purpose |
|---------|-----------|---------|
| Google Drive | 15GB | Sharing, general storage |
| Backblaze B2 | 10GB | Raw files, backup, AI integration |
| **Total** | **25GB** | |

## Cost if You Need More

| Service | Paid Plan | Cost |
|---------|-----------|------|
| Google Drive | 100GB | $2/month |
| Backblaze B2 | 100GB | $0.50/month |
| **Total** | **200GB** | **$2.50/month** |

## Workflow

1. **Family gathering materials** → Google Drive shared folder
   - Family uploads to shared folder
   - You organize and move to project structure

2. **Raw files storage** → Backblaze B2
   - Store PDFs, documents, images
   - Programmatic access for AI agents
   - Backup of critical files

3. **G-Brain integration** → Both
   - Upload key documents to G-Brain
   - Get URLs for reference in notes
   - Use B2 for large files, Google Drive for sharing

4. **Automation** → Backblaze B2 (S3 API)
   - Scripts can upload/download/list files
   - AI agents can access files programmatically
   - Automated workflows possible

## Setup Steps

### Google Drive
1. Create Google account (if needed)
2. Enable Google Drive API
3. Install `rclone` or `gdrive` CLI
4. Configure shared folder for family

### Backblaze B2
1. Create Backblaze account
2. Create bucket for project
3. Install `rclone` or `b2` CLI
4. Configure for AI agent access

### G-Brain Integration
1. Use G-Brain file upload for key documents
2. Get URLs for reference in notes
3. Use B2 or Google Drive for large files
