# Cloud Storage Options

## Requirements

- **Capacity:** 10-50GB for raw files (PDFs, documents, images)
- **Sharing:** Need to share with family members who are gathering materials
- **Access:** From VPS, WSL, and possibly phone
- **Backup:** Reliable, redundant storage
- **Cost:** Reasonable (free tier preferred initially)

## Options Comparison

### 1. Google Drive
**Free tier:** 15GB
**Paid plans:** $2/month (100GB), $3/month (200GB), $10/month (2TB)

**Pros:**
- Generous free tier (15GB)
- Excellent sharing features (easy to share folders with family)
- Good integration with other tools
- Accessible from any device
- Searchable (OCR for PDFs and images)

**Cons:**
- Privacy concerns (Google has access to files)
- Limited offline access without setup
- 15GB shared across Gmail, Drive, and Photos

**Best for:** Sharing with family, general-purpose storage, easy access

### 2. Dropbox
**Free tier:** 2GB
**Paid plans:** $12/month (2TB), $20/month (3TB)

**Pros:**
- Excellent syncing and sharing
- Good version history
- Reliable and fast
- Good offline access

**Cons:**
- Very limited free tier (2GB)
- Expensive paid plans
- Privacy concerns (similar to Google)

**Best for:**FileSyncing across devices, reliable backup

### 3. MEGA
**Free tier:** 20GB
**Paid plans:** €5/month (400GB), €10/month (2TB)

**Pros:**
- Generous free tier (20GB)
- End-to-end encryption (privacy)
- Good sharing features
- No file size limits on paid plans

**Cons:**
- Less well-known (potential trust issues)
- Slower than Google/Dropbox in some regions
- Limited integration with other tools

**Best for:** Privacy-conscious users, large free storage

### 4. pCloud
**Free tier:** 10GB
**Paid plans:** Lifetime plans available (e.g., $175 for 500GB lifetime)

**Pros:**
- Lifetime plans (no monthly fees)
- End-to-end encryption (optional)
- Good sharing features
- Media player built-in

**Cons:**
- Less well-known
- Lifetime plans require upfront payment
- Limited free tier (10GB)

**Best for:** Long-term storage, privacy-conscious users

### 5. Backblaze B2 (Object Storage)
**Free tier:** 10GB
**Paid plans:** $0.005/GB/month (e.g., 50GB = $0.25/month)

**Pros:**
- Very cheap for large amounts of data
- No egress fees
- Good API for developers
- Reliable and secure

**Cons:**
- Not user-friendly (requires technical setup)
- No sharing features (need to set up sharing yourself)
- No mobile app

**Best for:** Technical users, large amounts of data, backup

### 6. Wasabi (Object Storage)
**Free tier:** None (but very cheap)
**Paid plans:** $0.0059/GB/month (e.g., 50GB = $0.30/month)

**Pros:**
- Very cheap
- No egress fees
- Good API for developers
- Reliable and secure

**Cons:**
- Not user-friendly (requires technical setup)
- No sharing features
- No mobile app

**Best for:** Technical users, large amounts of data, backup

### 7. Cloudflare R2 (Object Storage)
**Free tier:** 10GB
**Paid plans:** $0.015/GB/month stored, $0.00 egress

**Pros:**
- Free egress (no download fees)
- Good API for developers
- Integrated with Cloudflare CDN
- Reliable and secure

**Cons:**
- Not user-friendly (requires technical setup)
- No sharing features
- No mobile app

**Best for:** Technical users, large downloads, CDN integration

---

## Recommendation

### Primary: Google Drive (15GB free)
- Use for sharing with family
- Use for general-purpose storage
- Use for documents that need to be easily accessible

### Secondary: MEGA (20GB free) or pCloud (10GB free)
- Use for privacy-sensitive materials
- Use for backup of critical files

### Tertiary: Backblaze B2 or Wasabi (cheap object storage)
- Use for large amounts of data (if needed)
- Use for long-term archive

---

## Workflow

1. **Family gathering materials** → Share a Google Drive folder with family
   - Family uploads documents, photos, etc. to the shared folder
   - You organize and move to project structure

2. **Raw files storage** → Google Drive or MEGA
   - Store PDFs, documents, images
   - Organize by period and pillar

3. **Backup** → Backblaze B2 or Wasabi (if needed)
   - Backup critical files
   - Long-term archive

4. **G-Brain integration** → G-Brain file upload
   - Upload key documents to G-Brain
   - Get URLs for reference in notes

---

## Cost Estimate

| Service | Free Tier | Paid Plan (if needed) |
|---------|-----------|----------------------|
| Google Drive | 15GB | $2/month (100GB) |
| MEGA | 20GB | €5/month (400GB) |
| pCloud | 10GB | $175 lifetime (500GB) |
| Backblaze B2 | 10GB | $0.25/month (50GB) |
| **Total** | **45GB free** | **$2-7/month** |

**Recommendation:** Start with Google Drive (15GB free). If you need more storage or privacy, add MEGA (20GB free). Total: 35GB free, enough for initial phase.
