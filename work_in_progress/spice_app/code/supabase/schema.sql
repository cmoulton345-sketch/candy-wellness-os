-- 🌶️ SPICE App Supabase Database Schema
-- Run this in your Supabase SQL Editor (https://app.supabase.com)

-- 1. Create UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Sessions Table
CREATE TABLE IF NOT EXISTS public.game_sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  room_code VARCHAR(6) UNIQUE NOT NULL,
  mode VARCHAR(20) NOT NULL DEFAULT 'pass_and_play',
  status VARCHAR(20) NOT NULL DEFAULT 'calibrating',
  partner_1_name VARCHAR(50) DEFAULT 'Partner 1',
  partner_2_name VARCHAR(50) DEFAULT 'Partner 2',
  partner_1_survey JSONB DEFAULT '{}'::jsonb,
  partner_2_survey JSONB DEFAULT '{}'::jsonb,
  allowed_categories JSONB DEFAULT '[]'::jsonb,
  current_deck JSONB DEFAULT '[]'::jsonb,
  current_card_index INT DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Enable Row Level Security (RLS) & Public Access Policies for Session Joining
ALTER TABLE public.game_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow anonymous read access" ON public.game_sessions
  FOR SELECT USING (true);

CREATE POLICY "Allow anonymous insert access" ON public.game_sessions
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow anonymous update access" ON public.game_sessions
  FOR UPDATE USING (true);

-- 4. Enable Supabase Realtime for Dual-Phone Sync
ALTER PUBLICATION supabase_realtime ADD TABLE public.game_sessions;
