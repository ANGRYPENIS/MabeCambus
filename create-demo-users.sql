-- =====================================================
-- CamBus - Demo Users Creation Script
-- Execute this script IN the configured database
-- to create additional demo/test accounts
-- =====================================================

-- IMPORTANT: Change these hashes in production!
-- These demo accounts use 'demo_password' for all
-- Password hashes were generated with bcrypt (rounds: 12)
-- To generate your own: use any bcrypt online tool or Python bcrypt library

-- ===========================
-- Demo User (OPERADOR role)
-- ===========================
-- Username: demo
-- Password: demo_password
-- Role: OPERADOR (Read-only access to dashboard)
-- ===========================
INSERT INTO usuarios (
    nombre_completo, 
    email, 
    username, 
    password_hash, 
    rol, 
    activo, 
    departamento,
    telefono
)
VALUES (
    'Demo User',
    'demo@cambus.local',
    'demo',
    '$2b$12$YY7GWLRVHMPXkc9iOvN/NeHEbKKW6SH1lWHPEqPjKsHwSHVqXFU3G',
    'OPERADOR',
    true,
    'DEMOSTRACION',
    '0000-0000'
)
ON CONFLICT (username) DO UPDATE SET 
    activo = true,
    ultimo_acceso = NULL;

-- ===========================
-- Supervisor Demo (SUPERVISOR role)
-- ===========================
-- Username: supervisor_demo
-- Password: demo_password
-- Role: SUPERVISOR (Dashboard + Reports access)
-- ===========================
INSERT INTO usuarios (
    nombre_completo,
    email,
    username,
    password_hash,
    rol,
    activo,
    departamento,
    telefono
)
VALUES (
    'Demo Supervisor',
    'supervisor_demo@cambus.local',
    'supervisor_demo',
    '$2b$12$YY7GWLRVHMPXkc9iOvN/NeHEbKKW6SH1lWHPEqPjKsHwSHVqXFU3G',
    'SUPERVISOR',
    true,
    'DEMOSTRACION',
    '0000-0001'
)
ON CONFLICT (username) DO UPDATE SET
    activo = true,
    ultimo_acceso = NULL;

-- ===========================
-- Admin Demo (ADMIN role)
-- ===========================
-- Username: admin_demo
-- Password: demo_password
-- Role: ADMIN (Full system access)
-- ===========================
INSERT INTO usuarios (
    nombre_completo,
    email,
    username,
    password_hash,
    rol,
    activo,
    departamento,
    telefono
)
VALUES (
    'Demo Admin',
    'admin_demo@cambus.local',
    'admin_demo',
    '$2b$12$YY7GWLRVHMPXkc9iOvN/NeHEbKKW6SH1lWHPEqPjKsHwSHVqXFU3G',
    'ADMIN',
    true,
    'DEMOSTRACION',
    '0000-0002'
)
ON CONFLICT (username) DO UPDATE SET
    activo = true,
    ultimo_acceso = NULL;

-- =====================================================
-- Verification
-- =====================================================
-- Run this query to verify users were created:

-- SELECT id_usuario, nombre_completo, username, rol, activo, departamento 
-- FROM usuarios 
-- WHERE username LIKE '%demo%' 
-- ORDER BY rol;

-- =====================================================
-- IMPORTANT SECURITY NOTES
-- =====================================================
-- 1. ALL demo accounts use the same password: "demo_password"
-- 2. CHANGE these passwords IMMEDIATELY before production
-- 3. Delete demo accounts when not needed
-- 4. Never use these credentials in production
-- 5. Hash format: bcrypt with 12 rounds (alg: $2b$12$...)
-- =====================================================
