import { Scraper } from 'agent-twitter-client';
import fs from 'fs';

function loadEnv() {
  const env = {};
  if (fs.existsSync('.env')) {
    const lines = fs.readFileSync('.env', 'utf-8').split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
        const [k, ...v] = trimmed.split('=');
        env[k.trim()] = v.join('=').trim().replace(/^["']|["']$/g, '');
      }
    }
  }
  return env;
}

async function run() {
  const env = loadEnv();
  const authToken = env.X_AUTH_TOKEN;
  const ct0 = env.X_CT0;

  const scraper = new Scraper();

  // Set cookies for twitter.com
  await scraper.setCookies([
    `auth_token=${authToken}; Domain=.twitter.com; Path=/; Secure; HttpOnly`,
    `ct0=${ct0}; Domain=.twitter.com; Path=/; Secure`
  ]);

  const loggedIn = await scraper.isLoggedIn();
  console.log("Logged In Status:", loggedIn);

  if (loggedIn) {
    console.log("Authentication SUCCESSFUL!");
  }
}

run().catch(console.error);
