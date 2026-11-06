CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id TEXT UNIQUE,
    target TEXT NOT NULL,
    scope TEXT,
    purpose TEXT,
    authorized INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    report_path TEXT,
    status TEXT DEFAULT 'draft'
);

CREATE TABLE IF NOT EXISTS hosts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id TEXT,
    host TEXT,
    state TEXT,
    vendor TEXT,
    os TEXT
);

CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id TEXT,
    host TEXT,
    port INTEGER,
    protocol TEXT,
    service TEXT,
    version TEXT
);

CREATE TABLE IF NOT EXISTS findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id TEXT,
    title TEXT,
    severity TEXT,
    evidence TEXT,
    source TEXT,
    confidence TEXT
);
