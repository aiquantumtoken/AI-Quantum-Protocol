import puppeteer from 'puppeteer-core';
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

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

async function verifyAndGetHandle() {
  const env = loadEnv();
  const authToken = env.X_AUTH_TOKEN;
  const ct0 = env.X_CT0;

  console.log("Launching Headless Chrome via puppeteer-core...");
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: "new",
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--window-size=1280,800'
    ]
  });

  try {
    const page = await browser.newPage();
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36");

    // Set cookies for x.com
    await page.setCookie(
      {
        name: 'auth_token',
        value: authToken,
        domain: '.x.com',
        path: '/',
        secure: true,
        httpOnly: true
      },
      {
        name: 'ct0',
        value: ct0,
        domain: '.x.com',
        path: '/',
        secure: true
      }
    );

    console.log("Navigating to https://x.com/home...");
    await page.goto("https://x.com/home", { waitUntil: 'networkidle2', timeout: 30000 });

    const currentUrl = page.url();
    console.log("Current URL:", currentUrl);

    // Check if redirected to login or in home
    if (currentUrl.includes("/login") || currentUrl.includes("/i/flow/login")) {
      console.log("Failed: Session expired or redirected to login.");
      return null;
    }

    console.log("Login verified! Page title:", await page.title());
    return true;
  } catch (err) {
    console.error("Error during verification:", err.message);
    return null;
  } finally {
    await browser.close();
  }
}

verifyAndGetHandle();
