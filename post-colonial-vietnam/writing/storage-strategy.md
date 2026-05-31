# Storage and Organization Strategy

## Current Constraints

- **VPS:** 38GB total, 11GB available (70% used)
- **G-Brain:** 1.4GB (structured notes, embeddings, search)
- **Work directory:** 620MB
- **Obsidian vault:** 36KB (basically empty)

## Recommendation: Hybrid System

### Tier 1: G-Brain (Primary Knowledge Base)

**Use for:**
- Structured notes and analysis
- Period portraits (one page per period)
- Biographical sketches (one page per person)
- Class analysis notes
- Covert apparatus findings
- High-level synthesis and cross-referencing

**Why:**
- Semantic search across all notes
- Links between pages (wiki-style)
- Embeddings for conceptual connections
- Already installed and configured
- Can store key files via file upload

**G-Brain can handle:**
- Text-based notes (unlimited in practice)
- Key documents via file upload (with URL generation)
- Structured analysis across periods and pillars

### Tier 2: Obsidian (Detailed Source Notes)

**Use for:**
- Annotated bibliographies (one note per source)
- Detailed reading notes
- Working drafts
- Quick captures and references

**Why:**
- Markdown-based (lightweight, portable)
- Bidirectional linking (see connections)
- Graph view (visualize relationships)
- Already has a vault at `/root/obsidian-vault/`

**Obsidian cannot handle well:**
- Large binary files (PDFs, images) — store elsewhere
- High-volume storage — better for notes than raw files

### Tier 3: Cloud Storage (Raw Files)

**Use for:**
- PDFs and government documents
- Images and photographs
- Large files that don't fit in G-Brain or Obsidian
- Backup of all research material

**Options:**
1. **Local storage + backup** — Store on VPS/WSL, back up to cloud
2. **Cloud-first** — Store directly in cloud (Google Drive, Dropbox, etc.)
3. **G-Brain file upload** — Store key documents in G-Brain, get URLs

**Recommendation:** Local storage + cloud backup
- Store raw files on VPS or WSL
- Back up to cloud service (Google Drive, Dropbox, etc.)
- Use G-Brain file upload for key documents referenced in notes

### Tier 4: LLM Wiki (Optional Enhancement)

**What it could be:**
- A wiki that uses LLMs for search and synthesis
- A knowledge base that connects disparate pieces of information
- A system that generates summaries and insights

**G-Brain already does this:**
- Semantic search across pages
- Synthesis via `think` tool
- Cross-referencing between periods and pillars

**Recommendation:** Use G-Brain as your LLM wiki. It already has the capabilities you need.

---

## Workflow

### 1. Gather Sources
- Download PDFs, documents, images
- Store in cloud storage (or local + backup)
- Log in source tracking file

### 2. Read and Annotate
- Read sources, take notes
- Store detailed notes in Obsidian (optional)
- Store key insights in G-Brain

### 3. Analyze with Five Lenses
- Burckhardt: Cultural themes
- Biography: Individual lives
- Nietzsche: Vital forces
- Marxist: Class structures
- Covert: Hidden apparatus
- Store analysis in G-Brain (one page per period/person)

### 4. Synthesize
- Create period portraits in G-Brain
- Cross-reference between periods
- Identify patterns and connections

### 5. Write
- Draft in G-Brain or Obsidian
- Refine and finalize
- Export as needed

---

## Storage Allocation

| Tier | Purpose | Estimated Size |
|------|---------|----------------|
| G-Brain | Notes, analysis, synthesis | 5-10GB |
| Obsidian | Detailed source notes (optional) | 1-2GB |
| Cloud | Raw files, PDFs, images | 10-50GB |
| **Total** | | **16-62GB** |

**VPS constraint:** 11GB available. Raw files should go to cloud storage.
**WSL constraint:** 32GB RAM, likely more storage. Could store raw files locally.

---

## Recommendation Summary

1. **G-Brain** for primary knowledge base (notes, analysis, synthesis)
2. **Obsidian** for detailed source notes (optional)
3. **Cloud storage** for raw files and backup
4. **G-Brain file upload** for key documents referenced in notes

This gives you:
- Semantic search across all notes (G-Brain)
- Structured analysis by period and pillar (G-Brain)
- Detailed source notes if needed (Obsidian)
- Unlimited storage for raw files (cloud)
- Backup of all material (cloud)

The system scales with your project. Start with G-Brain + cloud, add Obsidian if needed.
