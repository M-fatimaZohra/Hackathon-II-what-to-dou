/*
/**
 * Check Better Auth Tables
 *
 * Directly query the database to see what tables exist
 

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

async function checkTables() {
  console.log('🔍 Checking Better Auth Tables...\n');

  try {
    // Query to get all tables in the public schema
    const query = `
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public'
      ORDER BY table_name;
    `;

    const result = await dbPool.query(query);

    console.log('All tables in database:');
    result.rows.forEach(row => {
      console.log('- ' + row.table_name);
    });

    console.log('\n--- Checking for Better Auth specific tables ---');

    const baTables = ['accounts', 'sessions', 'users', 'verification', 'jwks'];
    for (const table of baTables) {
      const exists = result.rows.some(row => row.table_name === table);
      console.log(`${exists ? '✅' : '❌'} ${table} table: ${exists ? 'EXISTS' : 'MISSING'}`);
    }

    // If accounts table exists, check if there are any records
    if (result.rows.some(row => row.table_name === 'accounts')) {
      try {
        const countQuery = 'SELECT COUNT(*) as count FROM accounts;';
        const countResult = await dbPool.query(countQuery);
        console.log(`\n📊 Accounts table has ${countResult.rows[0].count} records`);
      } catch (countError) {
        console.log(`\n⚠️ Error counting accounts:`, countError.message);
      }
    }

    // If sessions table exists, check if there are any records
    if (result.rows.some(row => row.table_name === 'sessions')) {
      try {
        const countQuery = 'SELECT COUNT(*) as count FROM sessions;';
        const countResult = await dbPool.query(countQuery);
        console.log(`📊 Sessions table has ${countResult.rows[0].count} records`);
      } catch (countError) {
        console.log(`⚠️ Error counting sessions:`, countError.message);
      }
    }

    await dbPool.end();
    console.log('\n🔒 Database connection closed');

  } catch (error) {
    console.error('💥 Error checking tables:', error);
    await dbPool.end();
  }
}

// Run the check
checkTables().catch(console.error);
*/