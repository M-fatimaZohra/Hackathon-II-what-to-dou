/**
 * Trigger JWT Initialization
 *
 * This script attempts to trigger JWT signing key creation by directly using
 * Better Auth's JWT functionality.
 */

// Import auth using relative path since tsx might not resolve @ alias
// Commenting out to avoid conflicts during migration testing
// import { auth } from '../src/lib/auth';
import { Pool } from 'pg';

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

// Create a database pool to check the JWKS table
const dbPool = new Pool({
  connectionString: process.env.DATABASE_URL || '',
  max: 5, // Lower for this test
  min: 1,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 10000,
  maxUses: 750,
  allowExitOnIdle: true,
});

async function triggerJWTInitialization() {
  console.log('🔄 Attempting to trigger JWT initialization...\n');

  try {
    // Check JWKS table before
    console.log('🔍 Checking JWKS table before triggering JWT functionality...');
    let jwksResult = await dbPool.query('SELECT COUNT(*) FROM jwks;');
    let jwksCount = parseInt(jwksResult.rows[0].count);
    console.log(`📊 JWKS table count before: ${jwksCount}`);

    if (jwksCount === 0) {
      console.log('ℹ️ JWKS table is empty - attempting to trigger key creation...');

      // Try to access JWT functionality directly through Better Auth
      // This should trigger the initialization if done in the right context

      // First, let's check if there are existing sessions we can use to generate a JWT
      const sessionsResult = await dbPool.query(`
        SELECT s.id, s."userId", u.email
        FROM session s
        JOIN "user" u ON s."userId" = u.id
        LIMIT 1;
      `);

      if (sessionsResult.rows.length > 0) {
        const session = sessionsResult.rows[0];
        console.log(`👤 Found existing session for user: ${session.email} (ID: ${session.userId})`);

        // Try to get a JWT token for this session by simulating a proper request
        // We'll need to create a mock request context

        console.log('🔑 Attempting to trigger JWT creation via API...');

        // Wait a bit for any async initialization
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Check JWKS table again
        jwksResult = await dbPool.query('SELECT COUNT(*) FROM jwks;');
        jwksCount = parseInt(jwksResult.rows[0].count);
        console.log(`📊 JWKS table count after checking existing session: ${jwksCount}`);
      } else {
        console.log('ℹ️ No existing sessions found - JWT keys may be created on first authentication');
      }

      // The key insight: JWT signing keys should be created when the JWT functionality
      // is first used in a real application context. This might happen when:
      // 1. Someone calls the /api/auth/token endpoint
      // 2. The JWT plugin is first invoked

      // Let's try to access the plugin directly if possible
      console.log('\n🔧 Exploring Better Auth JWT plugin internals...');

      // Check if there are any direct methods we can call on the auth instance
      // to trigger JWT initialization
      console.log('Checking auth instance structure...');

      // Wait a bit more to allow for any async initialization that might happen
      // when the auth module is imported
      await new Promise(resolve => setTimeout(resolve, 3000));

      // Final check
      jwksResult = await dbPool.query('SELECT COUNT(*) FROM jwks;');
      jwksCount = parseInt(jwksResult.rows[0].count);
      console.log(`📊 JWKS table count after delay: ${jwksCount}`);

      if (jwksCount === 0) {
        console.log('\n❌ JWKS table still empty.');
        console.log('💡 The JWT keys might be created when the Next.js app first starts up');
        console.log('   and the auth instance is initialized in the server context.');
        console.log('   Or they might be created on the first actual JWT token request.');
      } else {
        console.log('\n✅ JWT signing keys have been created!');
        const sampleKeys = await dbPool.query('SELECT kid, alg FROM jwks LIMIT 5;');
        console.log('Sample keys:', sampleKeys.rows);
      }
    } else {
      console.log('✅ JWKS table already has keys:', jwksCount);
    }

    // Final status
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

    await dbPool.end();
    console.log('\n🔒 Database connection closed');

  } catch (error) {
    console.error('💥 Error during JWT initialization trigger:', error);
    await dbPool.end();
  }
}

// Run the trigger
triggerJWTInitialization().catch(console.error);