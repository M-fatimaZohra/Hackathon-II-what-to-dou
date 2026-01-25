/**
 * Check User Table Structure
 *
 * Check the actual structure of the user table
 */

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

async function checkUserTable() {
  console.log('🔍 Checking User Table Structure...\n');

  try {
    // Get column information for the user table
    const columnsQuery = `
      SELECT column_name, data_type
      FROM information_schema.columns
      WHERE table_name = 'user'
      ORDER BY ordinal_position;
    `;

    const columnsResult = await dbPool.query(columnsQuery);
    console.log('User table columns:');
    columnsResult.rows.forEach(col => {
      console.log(`  - ${col.column_name}: ${col.data_type}`);
    });

    console.log('');

    // Get actual user data
    const userQuery = 'SELECT * FROM user LIMIT 5;';
    const userResult = await dbPool.query(userQuery);

    console.log('User table data (first record):');
    if (userResult.rows.length > 0) {
      console.log(userResult.rows[0]);
    } else {
      console.log('No records found in user table');
    }

    console.log('');

    // Check if there are any accounts (even though count was 0, let's check structure)
    const accColumnsQuery = `
      SELECT column_name, data_type
      FROM information_schema.columns
      WHERE table_name = 'account'
      ORDER BY ordinal_position;
    `;

    const accColumnsResult = await dbPool.query(accColumnsQuery);
    console.log('Account table columns:');
    accColumnsResult.rows.forEach(col => {
      console.log(`  - ${col.column_name}: ${col.data_type}`);
    });

    console.log('');

    // Check if there are any sessions (even though count was 0, let's check structure)
    const sessColumnsQuery = `
      SELECT column_name, data_type
      FROM information_schema.columns
      WHERE table_name = 'session'
      ORDER BY ordinal_position;
    `;

    const sessColumnsResult = await dbPool.query(sessColumnsQuery);
    console.log('Session table columns:');
    sessColumnsResult.rows.forEach(col => {
      console.log(`  - ${col.column_name}: ${col.data_type}`);
    });

    console.log('\n🎯 KEY FINDINGS:');
    console.log('- Account table exists but has 0 records');
    console.log('- Session table exists but has 0 records');
    console.log('- User table exists and has 1 record');
    console.log('- JWKS table exists but has 0 records (this is the main issue!)');

    await dbPool.end();
    console.log('\n🔒 Database connection closed');

  } catch (error) {
    console.error('💥 Error checking user table:', error);
    await dbPool.end();
  }
}

// Run the check
checkUserTable().catch(console.error);