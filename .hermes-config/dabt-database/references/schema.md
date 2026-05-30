# DABT Database Schema

```sql
-- Source files (banks)
CREATE TABLE source_files (
    id INTEGER PRIMARY KEY,
    bank_name TEXT NOT NULL,
    filename TEXT,
    format_type TEXT,       -- "chapter-based", "topic-based", "comprehensive", "real-exam"
    year TEXT,
    description TEXT
);

-- Questions
CREATE TABLE questions (
    id TEXT PRIMARY KEY,              -- DABT-0001 to DABT-XXXX
    question_text TEXT NOT NULL,
    correct_answer_letter TEXT,
    correct_answer_text TEXT,
    explanation TEXT,
    source_file_id INTEGER,
    question_number_in_source INTEGER,
    bloom_level TEXT,
    FOREIGN KEY (source_file_id) REFERENCES source_files(id)
);

-- Answer options (1:M)
CREATE TABLE answer_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    option_letter TEXT NOT NULL,
    option_text TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Topic tags (M:M)
CREATE TABLE question_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    topic TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Domain classification
CREATE TABLE question_domains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    domain TEXT NOT NULL,         -- "Domain I" through "Domain IV"
    sub_domain TEXT,
    task TEXT,
    confidence TEXT,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Matching test pairs
CREATE TABLE match_pairs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    term TEXT NOT NULL,
    match_answer TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

CREATE INDEX idx_q_domain ON question_domains(domain);
CREATE INDEX idx_q_topic ON question_topics(topic);
CREATE INDEX idx_q_source ON questions(source_file_id);
```
