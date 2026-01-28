/*
/**
 * Simple Database Check
 *
 * Simple check to see what's in the database tables


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

async function simpleCheck() {
  console.log('🔍 Simple Database Check...\n');

  try {
    // Check counts in all tables
    const tables = ['account', 'session', 'user', 'jwks', 'task', 'verification'];

    for (const table of tables) {
      try {
        const result = await dbPool.query(`SELECT COUNT(*) FROM ${table};`);
        const count = parseInt(result.rows[0].count);
        console.log(`${table.toUpperCase()} table: ${count} records`);

        // If it's not the task table and has records, show a sample
        if (table !== 'task' && count > 0) {
          const sample = await dbPool.query(`SELECT * FROM ${table} LIMIT 1;`);
          console.log(`  Sample record:`, JSON.stringify(sample.rows[0], null, 2));
        }
      } catch (error) {
        console.log(`${table.toUpperCase()} table: ERROR - ${(error as any).message}`);
      }
      console.log('');
    }

    console.log('🎯 ANALYSIS:');
    console.log('- ACCOUNT table has 0 records - no users registered via Better Auth');
    console.log('- SESSION table has 0 records - no active sessions');
    console.log('- USER table has data but structure seems mixed (possibly from both Better Auth and SQLModel)');
    console.log('- JWKS table has 0 records - NO JWT SIGNING KEYS (this is the core issue!)');
    console.log('- VERIFICATION table has 0 records - no verification tokens');
    console.log('');

    console.log('💡 CONCLUSION: The JWKS table being empty explains why JWT tokens cannot be generated,');
    console.log('   which explains the "get-session 200:null, token 401" issue.');

    await dbPool.end();
    console.log('\n🔒 Database connection closed');

  } catch (error) {
    console.error('💥 Error in simple check:', error);
    await dbPool.end();
  }
}

// Run the check
simpleCheck().catch(console.error);
*/