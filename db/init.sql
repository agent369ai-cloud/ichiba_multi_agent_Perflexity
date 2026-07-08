CREATE TABLE IF NOT EXISTS merchant_listings (
    row_id SERIAL PRIMARY KEY,
    merchant_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    listing_status TEXT NOT NULL,
    category TEXT,
    locale TEXT NOT NULL DEFAULT 'en',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS campaign_records (
    row_id SERIAL PRIMARY KEY,
    merchant_id TEXT NOT NULL,
    campaign_id TEXT NOT NULL,
    campaign_status TEXT NOT NULL,
    rejection_reason TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS conversation_turns (
    turn_id SERIAL PRIMARY KEY,
    session_id TEXT NOT NULL,
    merchant_id TEXT NOT NULL,
    route TEXT,
    query TEXT NOT NULL,
    final_answer TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_conversation_turns_session ON conversation_turns (session_id, created_at DESC);

INSERT INTO merchant_listings (merchant_id, product_id, listing_status, category, locale) VALUES
    ('M123', 'P-9001', 'pending_moderation', NULL, 'jp'),
    ('M456', 'P-9002', 'active', 'home-goods', 'en'),
    ('M789', 'P-9003', 'active', 'electronics', 'en'),
    ('M999', 'P-9004', 'suspended', 'apparel', 'en');

INSERT INTO campaign_records (merchant_id, campaign_id, campaign_status, rejection_reason) VALUES
    ('M456', 'C-501', 'rejected', 'discount exceeds category maximum'),
    ('M123', 'C-502', 'approved', NULL);
