/**
 * JWT Flow Test
 *
 * This test follows the complete flow to trigger JWT creation:
 * 1. Create a user
 * 2. Authenticate the user (creating a session)
 * 3. Request a JWT token (which should trigger JWKS key creation)
 */

import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { Pool } from "pg";

// Load environment variables
import { readFileSync } from 'fs';
import { join } from 'path';

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

// Create a database pool (same as in auth.ts for consistency)
const dbPool = new Pool({
  connectionString: process.env.DATABASE_URL || '',
  max: 20,
  min: 5,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 10000,
  maxUses: 750,
  allowExitOnIdle: true,
});

// Create a fresh Better Auth instance with JWT plugin for testing
const testAuth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || 'test-secret-change-in-production',
  database: dbPool,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  session: {
    expiresIn: 604800, // 7 days in seconds
    cookie: {
      secure: false, // Set to false for localhost development
      sameSite: "lax",
      path: "/",
    },
  },
  baseURL: "http://localhost:3000", // Explicitly set the base URL
  trustedOrigins: ["http://localhost:3000"], // Allow localhost for development
  plugins: [
    jwt()
  ],
});

async function testJWTFlow() {
  console.log('🔄 Testing Complete JWT Flow...\n');

  // Generate test user data
  const testUser = {
    name: `JWT Flow Test ${Date.now()}`,
    email: `jwtflow${Date.now()}@example.com`,
    password: 'password123'
  };

  console.log('📝 Test user data:');
  console.log('- Name:', testUser.name);
  console.log('- Email:', testUser.email);
  console.log('- Password: password123\n');

  try {
    console.log('🔍 Initial JWKS table check...');
    let jwksResult = await dbPool.query('SELECT COUNT(*) FROM jwks;');
    let jwksCount = parseInt(jwksResult.rows[0].count);
    console.log(`📊 JWKS table count before signup: ${jwksCount}`);

    // Step 1: Sign up the user
    console.log('\n🔐 Step 1: Signing up user...');
    const signupResponse = await fetch('http://localhost:3000/api/auth/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: testUser.name,
        email: testUser.email,
        password: testUser.password
      }),
    });

    const signupData = await signupResponse.json();
    console.log('✅ Signup response:', signupResponse.status, signupData.success);

    // Wait a bit for database operations to complete
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Check JWKS after signup
    jwksResult = await dbPool.query('SELECT COUNT(*) FROM jwks;');
    jwksCount = parseInt(jwksResult.rows[0].count);
    console.log(`📊 JWKS table count after signup: ${jwksCount}`);

    if (jwksCount === 0) {
      console.log('ℹ️ JWKS still empty after signup, trying to get JWT token...');

      // Step 2: Try to get JWT token (this should trigger JWT creation if session is valid)
      console.log('\n🔑 Step 2: Requesting JWT token...');
      const tokenResponse = await fetch('http://localhost:3000/api/auth/token', {
        method: 'GET',
        credentials: 'include',
      });

      const tokenData = await tokenResponse.json();
      console.log('✅ Token response:', tokenResponse.status);
      console.log('Token data:', tokenData);

      // Check JWKS after token request
      await new Promise(resolve => setTimeout(resolve, 1000)); // Wait for async ops
      jwksResult = await dbPool.query('SELECT COUNT(*) FROM jwks;');
      jwksCount = parseInt(jwksResult.rows[0].count);
      console.log(`📊 JWKS table count after token request: ${jwksCount}`);

      if (jwksCount > 0) {
        console.log('✅ SUCCESS: JWKS keys created after token request!');
        const sampleKeys = await dbPool.query('SELECT kid, alg FROM jwks LIMIT 3;');
        console.log('JWT Keys:', sampleKeys.rows);
      } else {
        console.log('❌ JWKS still empty - JWT keys not created');

        // Check if it's because there's no valid session
        console.log('\n👤 Checking session status...');
        const sessionResponse = await fetch('http://localhost:3000/api/auth/session', {
          method: 'GET',
          credentials: 'include',
        });

        const sessionData = await sessionResponse.json();
        console.log('Session response:', sessionResponse.status);
        console.log('Session data:', sessionData);
      }
    } else {
      console.log('✅ JWKS keys already exist after signup!');
    }

    // Final status check
    console.log('\n📋 Final Status:');
    const tables = ['account', 'session', 'user', 'jwks', 'verification'];
    for (const table of tables) {
      try {
        const result = await dbPool.query(`SELECT COUNT(*) FROM ${table};`);
        const count = parseInt(result.rows[0].count);
        console.log(`   ${table.toUpperCase()}: ${count} records`);
      } catch (error) {
        console.log(`   ${table.toUpperCase()}: ERROR - ${(error as any).message}`);
      }
    }

    // Close the database connection
    await dbPool.end();
    console.log('\n🔒 Database connection closed');

  } catch (error) {
    console.error('💥 Error during JWT flow test:', error);
    await dbPool.end();
  }
}

// Run the test
testJWTFlow().catch(console.error);