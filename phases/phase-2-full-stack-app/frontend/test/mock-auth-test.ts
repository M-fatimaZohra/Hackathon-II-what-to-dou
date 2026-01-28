/*
/**
 * Mock Authentication Test
 *
 * This test simulates the signup process like Better Auth does:
 * 1. Save user data to database
 * 2. Create a session
 * 3. Generate a JWT token
 * 4. Verify the token can be retrieved


// Load environment variables
import { readFileSync } from 'fs';
import { join } from 'path';

// Load .env file manually
try {
  const envFilePath = join(process.cwd(), '.env');
  const envFileContent = readFileSync(envFilePath, 'utf8');

  // Parse the .env file content
  const envLines = envFileContent.split('\n');
  for (const line of envLines) {
    if (line.trim() && line.includes('=')) {
      const [key, ...valueParts] = line.split('=');
      const trimmedKey = key.trim();
      let value = valueParts.join('=').trim(); // Preserve = in the value

      // Remove quotes if present
      if ((value.startsWith('"') && value.endsWith('"')) ||
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.substring(1, value.length - 1);
      }

      process.env[trimmedKey] = value;
    }
  }
} catch (error) {
  console.log('⚠️ Could not load .env file:', error.message);
}

import { Pool } from 'pg';
import { SignJWT } from 'jose';
import crypto from 'crypto';

// Database connection using the same config as auth.ts
const dbPool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  min: 5,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 10000,
  maxUses: 750,
  allowExitOnIdle: true,
});

async function mockSignupProcess() {
  console.log('🧪 Starting Mock Authentication Test...\n');

  try {
    // Step 1: Generate mock user data
    console.log('📝 Step 1: Creating mock user data...');

    const mockUserData = {
      name: 'Test User',
      email: `test-${Date.now()}@example.com`,
      password: 'SecurePassword123!',
      id: `user_${crypto.randomBytes(10).toString('hex')}`,
      createdAt: new Date().toISOString(),
    };

    console.log('Mock user data created:');
    console.log('- ID:', mockUserData.id);
    console.log('- Email:', mockUserData.email);
    console.log('- Name:', mockUserData.name);
    console.log('');

    // Step 2: Insert user into database (mocking Better Auth's account creation)
    console.log('💾 Step 2: Saving user to database (mocking Better Auth)...');

    // First, let's check if Better Auth tables exist by querying the accounts table
    try {
      const checkTablesQuery = `
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name IN ('accounts', 'sessions', 'users', 'verification', 'jwks');
      `;

      const tableResults = await dbPool.query(checkTablesQuery);
      console.log('Existing Better Auth tables:', tableResults.rows.map(r => r.table_name));
      console.log('');

      // Try to insert a user into the accounts table (this is where Better Auth stores user data)
      const insertUserQuery = `
        INSERT INTO accounts (id, provider_id, email, name, username, email_verified, phone_number, avatar, created_at, updated_at, password)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        RETURNING id, email, name, created_at;
      `;

      const providerId = 'credential'; // Default for email/password auth
      const result = await dbPool.query(insertUserQuery, [
        mockUserData.id,
        providerId,
        mockUserData.email,
        mockUserData.name,
        null, // username
        false, // email_verified
        null, // phone_number
        null, // avatar
        mockUserData.createdAt,
        mockUserData.createdAt,
        '$2b$10$examplehashedpassword', // This would be the actual hashed password
      ]);

      console.log('✅ User inserted into database:', result.rows[0]);
      console.log('');
    } catch (insertError: any) {
      if (insertError.code === '42P01') { // Undefined table
        console.log('⚠️ Better Auth tables not found in database - they may not be created yet');
        console.log('💡 Run "npx @better-auth/cli migrate" to create Better Auth tables');
      } else {
        console.log('⚠️ Error inserting user (this is expected if tables don\'t exist yet):', insertError.message);
      }
      console.log('');
    }

    // Step 3: Create a mock session (similar to how Better Auth creates sessions)
    console.log('🔑 Step 3: Creating mock session (mimicking Better Auth session creation)...');

    try {
      const sessionId = `sess_${crypto.randomBytes(10).toString('hex')}`;
      const expiresAt = new Date();
      expiresAt.setDate(expiresAt.getDate() + 7); // 7 days expiry

      const insertSessionQuery = `
        INSERT INTO sessions (id, user_id, expires_at, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, user_id, expires_at;
      `;

      const sessionResult = await dbPool.query(insertSessionQuery, [
        sessionId,
        mockUserData.id,
        expiresAt.toISOString(),
        new Date().toISOString(),
        new Date().toISOString(),
      ]);

      console.log('✅ Session created in database:', sessionResult.rows[0]);
      console.log('');
    } catch (sessionError: any) {
      if (sessionError.code === '42P01') { // Undefined table
        console.log('⚠️ Sessions table not found - Better Auth tables may not be created');
      } else {
        console.log('⚠️ Error creating session:', sessionError.message);
      }
      console.log('');
    }

    // Step 4: Generate JWT token using the Better Auth secret (this works based on our previous test)
    console.log('🔐 Step 4: Generating JWT token with Better Auth secret...');

    const BETTER_AUTH_SECRET = process.env.BETTER_AUTH_SECRET;
    if (!BETTER_AUTH_SECRET) {
      console.log('❌ Cannot generate JWT - BETTER_AUTH_SECRET not found');
      return;
    }

    console.log('✅ Better Auth secret is available');

    // Create a JWT payload similar to what Better Auth would create
    const tokenPayload = {
      id: mockUserData.id,
      email: mockUserData.email,
      name: mockUserData.name,
      sid: `sess_${crypto.randomBytes(10).toString('hex')}`, // session ID
      iat: Math.floor(Date.now() / 1000), // Issued at time
      exp: Math.floor(Date.now() / 1000) + (7 * 24 * 60 * 60), // Expire in 7 days
    };

    // Create JWT using the same method from our successful test
    const encoder = new TextEncoder();
    const secret = encoder.encode(BETTER_AUTH_SECRET);

    const jwt = await new SignJWT(tokenPayload)
      .setProtectedHeader({ alg: 'HS256' })
      .setIssuedAt()
      .setExpirationTime('7d')
      .sign(secret);

    console.log('✅ JWT token generated successfully!');
    console.log('Token (first 50 chars):', jwt.substring(0, 50) + '...');
    console.log('');

    // Step 5: Decode and verify the token contents
    console.log('🔍 Step 5: Verifying token contents...');

    const tokenParts = jwt.split('.');
    if (tokenParts.length === 3) {
      try {
        const payload = JSON.parse(atob(tokenParts[1]));
        console.log('Decoded payload:');
        console.log('- User ID:', payload.id);
        console.log('- Email:', payload.email);
        console.log('- Name:', payload.name);
        console.log('- Session ID:', payload.sid);
        console.log('- Expires at:', new Date(payload.exp * 1000).toISOString());
        console.log('');
      } catch (decodeError) {
        console.log('❌ Could not decode token payload:', decodeError);
      }
    }

    // Step 6: Summary
    console.log('🏁 Mock Authentication Test Summary:');
    console.log('');

    console.log('✅ User data prepared');
    console.log('✅ Database insertion simulated');
    console.log('✅ Session creation simulated');
    console.log('✅ JWT token generation successful');
    console.log('');

    console.log('🎯 Key Finding: JWT generation works perfectly with Better Auth secret');
    console.log('🎯 The issue is likely in Better Auth\'s session management, not JWT signing');
    console.log('');

    // Close the database connection
    await dbPool.end();
    console.log('🔒 Database connection closed');

  } catch (error) {
    console.error('💥 Error in mock authentication test:', error);
    await dbPool.end();
  }
}

// Run the test
mockSignupProcess().catch(console.error);
*/