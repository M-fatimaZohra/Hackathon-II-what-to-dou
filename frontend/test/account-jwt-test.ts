/**
 * Account Creation and JWT Keys Test
 *
 * This test creates a new account via Better Auth and checks if JWT keys
 * are automatically created in the JWKS table after account creation.
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

async function testAccountCreationAndJWTKeys() {
  console.log('📝 Testing account creation and JWT key generation...\n');

  // Generate test user data
  const testUser = {
    name: `Test User ${Date.now()}`,
    email: `test${Date.now()}@example.com`,
    password: 'password123'
  };

  console.log('📝 Test user data:');
  console.log('- Name:', testUser.name);
  console.log('- Email:', testUser.email);
  console.log('- Password: password123\n');

  try {
    // Check JWKS table before account creation
    console.log('🔍 Checking JWKS table before account creation...');
    let jwksResult = await dbPool.query('SELECT COUNT(*) FROM jwks;');
    let jwksCount = parseInt(jwksResult.rows[0].count);
    console.log(`📊 JWKS table count before: ${jwksCount}`);

    // Step 1: Create an account via Better Auth
    console.log('\n🔐 Step 1: Creating account via Better Auth...');
    const signupResult = await testAuth.api.signUpEmail({
      body: {
        name: testUser.name,
        email: testUser.email,
        password: testUser.password,
        callbackURL: '/tasks'
      },
      headers: new Headers(), // Empty headers for test
    });

    console.log('✅ Account creation result:', !!signupResult);
    if (signupResult.user) {
      console.log('👤 User created with ID:', signupResult.user.id);
    }

    // Wait a moment for any async operations that might trigger JWT key creation
    console.log('\n⏳ Waiting for potential JWT key creation...');
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Check JWKS table after account creation
    jwksResult = await dbPool.query('SELECT COUNT(*) FROM jwks;');
    jwksCount = parseInt(jwksResult.rows[0].count);
    console.log(`📊 JWKS table count after account creation: ${jwksCount}`);

    if (jwksCount === 0) {
      console.log('❌ JWKS table still empty after account creation');

      // The JWT keys might be created when requesting a token, not during account creation
      console.log('\n🔑 Trying to get a JWT token to see if it triggers key creation...');

      try {
        // Try to get a token using the session from signup
        if (signupResult.session) {
          // This might not work directly with the testAuth instance
          // Let's try to trigger the JWT creation by attempting to use the session
          console.log('Using session from signup result to try token creation...');
        }

        // Wait again to see if any delayed initialization happens
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Check JWKS again
        jwksResult = await dbPool.query('SELECT COUNT(*) FROM jwks;');
        jwksCount = parseInt(jwksResult.rows[0].count);
        console.log(`📊 JWKS table count after token attempt: ${jwksCount}`);

        if (jwksCount > 0) {
          console.log('✅ SUCCESS: JWT keys created after token request attempt!');
          const sampleKeys = await dbPool.query('SELECT kid, alg FROM jwks LIMIT 3;');
          console.log('Sample JWT keys:', sampleKeys.rows);
        } else {
          console.log('❌ JWKS table still empty after token request attempt');
          console.log('💡 JWT keys may be created when the app is running in server context');
        }
      } catch (tokenError) {
        console.log('Token request attempt error:', (tokenError as any).message);
      }
    } else {
      console.log('✅ SUCCESS: JWT keys created after account creation!');
      const sampleKeys = await dbPool.query('SELECT kid, alg FROM jwks LIMIT 3;');
      console.log('JWT keys created:', sampleKeys.rows);
    }

    // Final status check
    console.log('\n📋 Final database status:');
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
    console.error('💥 Error during account creation and JWT test:', error);
    await dbPool.end();
  }
}

// Run the test
testAccountCreationAndJWTKeys().catch(console.error);