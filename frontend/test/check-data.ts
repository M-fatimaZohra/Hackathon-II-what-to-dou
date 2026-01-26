/*
/**
 * Check Better Auth Data
 *
 * Check the actual data in Better Auth tables


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

async function checkData() {
  console.log('🔍 Checking Better Auth Data...\n');

  try {
    // Check account table
    try {
      const accountQuery = 'SELECT COUNT(*) as count FROM account;';
      const accountResult = await dbPool.query(accountQuery);
      console.log(`📊 Account table has ${accountResult.rows[0].count} records`);

      if (accountResult.rows[0].count > 0) {
        const accountDetails = await dbPool.query('SELECT id, email, name, created_at FROM account LIMIT 5;');
        console.log('Account details (first 5):');
        accountDetails.rows.forEach(row => {
          console.log(`  - ID: ${row.id}, Email: ${row.email}, Name: ${row.name}, Created: ${row.created_at}`);
        });
      }
    } catch (accountError) {
      console.log(`⚠️ Error querying account table:`, accountError.message);
    }

    // Check session table
    try {
      const sessionQuery = 'SELECT COUNT(*) as count FROM session;';
      const sessionResult = await dbPool.query(sessionQuery);
      console.log(`📊 Session table has ${sessionResult.rows[0].count} records`);

      if (sessionResult.rows[0].count > 0) {
        const sessionDetails = await dbPool.query('SELECT id, user_id, expires_at, created_at FROM session LIMIT 5;');
        console.log('Session details (first 5):');
        sessionDetails.rows.forEach(row => {
          console.log(`  - ID: ${row.id}, User_ID: ${row.user_id}, Expires: ${row.expires_at}, Created: ${row.created_at}`);
        });
      }
    } catch (sessionError) {
      console.log(`⚠️ Error querying session table:`, sessionError.message);
    }

    // Check user table
    try {
      const userQuery = 'SELECT COUNT(*) as count FROM user;';
      const userResult = await dbPool.query(userQuery);
      console.log(`📊 User table has ${userResult.rows[0].count} records`);

      if (userResult.rows[0].count > 0) {
        const userDetails = await dbPool.query('SELECT id, email, name, created_at FROM user LIMIT 5;');
        console.log('User details (first 5):');
        userDetails.rows.forEach(row => {
          console.log(`  - ID: ${row.id}, Email: ${row.email}, Name: ${row.name}, Created: ${row.created_at}`);
        });
      }
    } catch (userError) {
      console.log(`⚠️ Error querying user table:`, userError.message);
    }

    // Check jwks table
    try {
      const jwksQuery = 'SELECT COUNT(*) as count FROM jwks;';
      const jwksResult = await dbPool.query(jwksQuery);
      console.log(`📊 JWKS table has ${jwksResult.rows[0].count} records`);

      if (jwksResult.rows[0].count > 0) {
        const jwksDetails = await dbPool.query('SELECT created_at, expires_at FROM jwks LIMIT 5;');
        console.log('JWKS details (first 5):');
        jwksDetails.rows.forEach(row => {
          console.log(`  - Created: ${row.created_at}, Expires: ${row.expires_at}`);
        });
      } else {
        console.log('❌ JWKS table is EMPTY - this is the likely cause of JWT generation failure!');
      }
    } catch (jwksError) {
      console.log(`⚠️ Error querying jwks table:`, jwksError.message);
    }

    await dbPool.end();
    console.log('\n🔒 Database connection closed');

  } catch (error) {
    console.error('💥 Error checking data:', error);
    await dbPool.end();
  }
}

// Run the check
checkData().catch(console.error);
*/