/**
 * JWT Initialization Test
 *
 * This test attempts to trigger JWT plugin initialization to create signing keys.
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

async function testJWTInitialization() {
  console.log('🔧 Testing JWT Plugin Initialization...\n');

  try {
    // Check JWKS table before any operations
    console.log('🔍 Checking JWKS table before operations...');
    try {
      const jwksResult = await dbPool.query('SELECT COUNT(*) FROM jwks;');
      const jwksCount = parseInt(jwksResult.rows[0].count);
      console.log(`📊 JWKS table record count before: ${jwksCount}`);

      if (jwksCount === 0) {
        console.log('⚠️ JWKS table is empty - this may be expected initially');

        // The JWKS keys are typically created when JWT functionality is first used
        // Let's try to make a request that would trigger JWT creation
        console.log('\n📝 Attempting to trigger JWT creation via Better Auth API...');

        // Try to get a session token (this might trigger JWT creation if configured properly)
        try {
          const sessionResult = await testAuth.api.getSession({
            headers: new Headers(),
          });

          console.log('Session result:', !!sessionResult);

          // Wait a moment for any async operations
          await new Promise(resolve => setTimeout(resolve, 1000));

          // Check JWKS again
          const jwksResultAfter = await dbPool.query('SELECT COUNT(*) FROM jwks;');
          const jwksCountAfter = parseInt(jwksResultAfter.rows[0].count);
          console.log(`📊 JWKS table record count after session attempt: ${jwksCountAfter}`);

        } catch (sessionError) {
          console.log('Session attempt result:', (sessionError as any).message || sessionError);
        }
      } else {
        console.log('✅ JWKS table already has keys:', jwksCount);
      }
    } catch (jwksError) {
      console.log('⚠️ Could not query JWKS table:', (jwksError as any).message);
    }

    // Check if there are existing users we can use for JWT testing
    console.log('\n🔍 Checking for existing users to test JWT generation...');

    try {
      const usersResult = await dbPool.query('SELECT id, name, email FROM user LIMIT 1;');
      if (usersResult.rows.length > 0) {
        console.log('👤 Found existing user:', usersResult.rows[0]);

        // Try to create a proper session context to generate JWT
        console.log('\n🔑 Attempting JWT generation with existing user...');

        // This is tricky - we need the proper session context
        // The JWT is typically generated when a user is authenticated and needs a token
      } else {
        console.log('ℹ️ No existing users found - will create a test user');

        // Create a test user to trigger the full flow
        const testUser = {
          name: `JWT Test ${Date.now()}`,
          email: `jwttest${Date.now()}@example.com`,
          password: 'password123'
        };

        console.log('Creating test user:', testUser.email);

        try {
          const signupResult = await testAuth.api.signUpEmail({
            body: {
              name: testUser.name,
              email: testUser.email,
              password: testUser.password,
              callbackURL: '/tasks'
            },
            headers: new Headers(),
          });

          console.log('✅ User created:', !!signupResult.user);

          // Now try to get a JWT token
          // This requires a proper session context, which is typically set up by the auth flow

        } catch (error) {
          console.log('User creation error:', (error as any).message);
        }
      }
    } catch (usersError) {
      console.log('Error querying users:', (usersError as any).message);
    }

    // Final check of JWKS table
    console.log('\n📋 Final JWKS table status:');
    try {
      const finalJwksResult = await dbPool.query('SELECT COUNT(*) FROM jwks;');
      const finalJwksCount = parseInt(finalJwksResult.rows[0].count);
      console.log(`📊 Final JWKS count: ${finalJwksCount}`);

      if (finalJwksCount > 0) {
        console.log('✅ SUCCESS: JWT signing keys exist!');
        const sampleKeys = await dbPool.query('SELECT kid, alg FROM jwks LIMIT 2;');
        console.log('Sample keys:', sampleKeys.rows);
      } else {
        console.log('❌ JWKS table still empty - JWT keys not created');
        console.log('💡 This may indicate that JWT keys are created on first actual token request');
        console.log('   with proper session context, not during initial setup');
      }
    } catch (error) {
      console.log('Error checking final JWKS:', (error as any).message);
    }

    // Close the database connection
    await dbPool.end();
    console.log('\n🔒 Database connection closed');

  } catch (error) {
    console.error('💥 Error during JWT initialization test:', error);
    await dbPool.end();
  }
}

// Run the test
testJWTInitialization().catch(console.error);