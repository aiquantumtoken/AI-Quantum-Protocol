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

async function postTweet(text) {
  const env = loadEnv();
  const authToken = env.X_AUTH_TOKEN;
  const ct0 = env.X_CT0;

  if (!text) {
    console.error("No tweet text provided.");
    process.exit(1);
  }

  console.log("Starting headless post sequence for:", text);

  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: "new",
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--window-size=1280,900'
    ]
  });

  try {
    const page = await browser.newPage();
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36");

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

    console.log("Navigating to https://x.com/compose/post...");
    await page.goto("https://x.com/compose/post", { waitUntil: 'networkidle2', timeout: 30000 });

    // Wait for the tweet textbox
    const editorSelector = '[data-testid="tweetTextarea_0"]';
    await page.waitForSelector(editorSelector, { timeout: 15000 });
    console.log("Found tweet composer textbox.");

    await page.click(editorSelector);
    // Type with a realistic human cadence
    await page.type(editorSelector, text, { delay: 25 });
    console.log("Tweet text entered.");

    // Find and click the Post button
    const postButtonSelector = '[data-testid="tweetButton"]';
    await page.waitForSelector(postButtonSelector, { timeout: 5000 });
    await page.click(postButtonSelector);
    console.log("Clicked Post button.");

    // Wait for submission to complete
    await new Promise(r => setTimeout(r, 4000));
    console.log("Tweet successfully submitted!");
    return true;
  } catch (err) {
    console.error("Error posting tweet:", err.message);
    return false;
  } finally {
    await browser.close();
  }
}

const tweetContent = process.argv.slice(2).join(" ");
if (tweetContent) {
  postTweet(tweetContent);
} else {
  console.log("Usage: node scripts/post_tweet.mjs \"Your tweet here\"");
}
