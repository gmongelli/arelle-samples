CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    name TEXT
)

CREATE TABLE presentation_linkbases (
    id SERIAL PRIMARY KEY,
    id_document INTEGER REFERENCES documents(id),
    linkrole TEXT,
    label_en TEXT,
    layout JSONB
)

CREATE TABLE facts (
    id SERIAL PRIMARY KEY,
    id_document INTEGER REFERENCES documents(id),
    value TEXT,
    decimals INTEGER,
    concept TEXT,
    entity TEXT,
    period_values VARCHAR(128),
    unit VARCHAR(255),
    language VARCHAR(16),
    id_note TEXT,
    dimensions JSONB,
    links JSONB
)