-- Nexora University – UniSphere AI Database Schema

-- 1. Profiles Table
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL DEFAULT 'admin',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Documents Table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    file_url TEXT,
    file_name TEXT,
    uploaded_by UUID REFERENCES profiles(id) ON DELETE SET NULL,
    status TEXT DEFAULT 'uploaded' CHECK (status IN ('uploaded', 'processing', 'indexed', 'failed', 'draft', 'published', 'archived')),
    chunk_count INT DEFAULT 0,
    processed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Chat History Table
CREATE TABLE IF NOT EXISTS chat_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT NOT NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    source_document TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Analytics Table
CREATE TABLE IF NOT EXISTS analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type TEXT NOT NULL,
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    page_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Notices Table
CREATE TABLE IF NOT EXISTS notices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT,
    category TEXT CHECK (category IN ('Academic', 'Examination', 'Events', 'Administration')),
    attachment_url TEXT,
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    published_at TIMESTAMPTZ,
    created_by UUID REFERENCES profiles(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Events Table
CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    venue TEXT,
    organizer TEXT,
    brochure_url TEXT,
    status TEXT DEFAULT 'upcoming' CHECK (status IN ('upcoming', 'active', 'completed', 'archived')),
    created_by UUID REFERENCES profiles(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. University Settings Table
CREATE TABLE IF NOT EXISTS university_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL DEFAULT 'Nexora University',
    tagline TEXT,
    description TEXT,
    vision TEXT,
    mission TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    logo_url TEXT,
    banner_url TEXT,
    social_links JSONB DEFAULT '{}',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_documents_category ON documents(category);
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);
CREATE INDEX IF NOT EXISTS idx_notices_status ON notices(status);
CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
CREATE INDEX IF NOT EXISTS idx_chat_history_session ON chat_history(session_id);
CREATE INDEX IF NOT EXISTS idx_analytics_type ON analytics(event_type);

-- Row Level Security (RLS)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE notices ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics ENABLE ROW LEVEL SECURITY;
ALTER TABLE university_settings ENABLE ROW LEVEL SECURITY;

-- Public Read Policies
DROP POLICY IF EXISTS "Public can read published documents" ON documents;
CREATE POLICY "Public can read published documents" ON documents FOR SELECT USING (status IN ('published', 'indexed'));

DROP POLICY IF EXISTS "Public can read published notices" ON notices;
CREATE POLICY "Public can read published notices" ON notices FOR SELECT USING (status = 'published');

DROP POLICY IF EXISTS "Public can read active events" ON events;
CREATE POLICY "Public can read active events" ON events FOR SELECT USING (status IN ('upcoming', 'active'));

DROP POLICY IF EXISTS "Public can read university settings" ON university_settings;
CREATE POLICY "Public can read university settings" ON university_settings FOR SELECT USING (true);
