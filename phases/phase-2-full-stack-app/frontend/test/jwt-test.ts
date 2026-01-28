/*
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

async function testJWTGeneration() {
  console.log('🔍 Testing JWT Generation with Better Auth...\n');

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
    // Step 1: Sign up the test user
    console.log('🔐 Step 1: Signing up test user...');
    const signupResult = await testAuth.api.signUpEmail({
      body: {
        name: testUser.name,
        email: testUser.email,
        password: testUser.password,
        callbackURL: '/tasks'
      },
      headers: new Headers(), // Empty headers for test
    });

    console.log('✅ Signup successful:', !!signupResult);

    if (!signupResult.user) {
      console.error('❌ Signup failed - no user returned');
      return;
    }

    console.log('👤 User created with ID:', signupResult.user.id);

    // Step 2: Create a mock request to simulate getting a session
    console.log('\n👤 Step 2: Getting session...');
    const sessionResult = await testAuth.api.getSession({
      headers: new Headers(), // Empty headers for test
    });

    console.log('✅ Session result:', !!sessionResult);
    if (sessionResult && sessionResult.user) {
      console.log('👤 Session user ID:', sessionResult.user.id);
    } else {
      console.log('👤 No session user found (this may be expected in test context)');
    }

    // Step 3: Try to generate JWT token
    console.log('\n🔑 Step 3: Attempting to generate JWT token...');
    const tokenResult = await testAuth.api.getToken({
      headers: new Headers(), // Empty headers for test
    });

    console.log('✅ Token result:', !!tokenResult);
    if (tokenResult && tokenResult.token) {
      console.log('✅ JWT TOKEN GENERATED SUCCESSFULLY!');
      console.log('Token (first 50 chars):', tokenResult.token.substring(0, 50) + '...');

      // Decode and display token info
      const tokenParts = tokenResult.token.split('.');
      if (tokenParts.length === 3) {
        const payload = JSON.parse(atob(tokenParts[1]));
        console.log('Token payload:', {
          userId: payload.sub || payload.id || payload.userId,
          exp: new Date(payload.exp * 1000).toISOString(),
          iat: new Date(payload.iat * 1000).toISOString()
        });
      }
    } else {
      console.log('❌ JWT TOKEN GENERATION FAILED');
      console.log('Token result:', tokenResult);

      // Check if it's due to missing session
      console.log('\n🔍 Diagnosing JWT generation failure...');

      // Check if JWKS table has keys
      try {
        const jwksResult = await dbPool.query('SELECT COUNT(*) FROM jwks;');
        const jwksCount = parseInt(jwksResult.rows[0].count);
        console.log(`📊 JWKS table record count: ${jwksCount}`);

        if (jwksCount === 0) {
          console.log('⚠️ JWKS table is empty - JWT signing keys are missing!');
          console.log('   This explains why JWT tokens cannot be generated.');
        } else {
          console.log('✅ JWKS table has signing keys');

          // Get a sample key to inspect
          const sampleKeys = await dbPool.query('SELECT kid, alg FROM jwks LIMIT 1;');
          if (sampleKeys.rows.length > 0) {
            console.log('Sample JWKS key:', sampleKeys.rows[0]);
          }
        }
      } catch (jwksError) {
        console.log('⚠️ Could not query JWKS table:', (jwksError as any).message);
      }
    }

    // Step 4: Check database tables for debugging
    console.log('\n📋 Database table status:');
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
    console.error('💥 Error during JWT test:', error);
    await dbPool.end();
  }
}

// Run the test
testJWTGeneration().catch(console.error);
*/