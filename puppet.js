const puppeteer = require('puppeteer');
import fs from 'fs';
const fs = require('fs').promises;

// Replace 'get_screen_names' with the actual way you get screen names in JavaScript
const parse = require('csv-parse/sync'); // You need to install the 'csv-parse' package

// Function to mimic the pandas functionality in the provided Python code
async function getScreenNames(filePath) {
  // Read the CSV file
  const fileContent = fs.readFileSync(filePath, { encoding: 'utf8' });
  
  // Parse the CSV content
  const records = parse(fileContent, {
    columns: true,
    skip_empty_lines: true
  });

  // Filter and sort the records
  const filteredAndSorted = records
    .filter(record => Number(record.score) > 2) // Filter records with score > 2
    .sort((a, b) => Number(b.score) - Number(a.score)); // Sort by score in descending order

  // Extract screen names
  const screenNames = filteredAndSorted.map(record => record.screen_name);

  return screenNames;
}

// Example usage
const filePath = "C:\\Users\\malir\\OneDrive\\Old laptop\\Find\\scores.csv";
const screenNames = getScreenNames(filePath);

let dic = {};

async function scraper(screenName) {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  const url = `https://twitter.com/${screenName}`;

  // Define your cookies here
  const cookies = [
    {'name': 'guest_id_ads', 'value': 'v1%3A170526598080178325', 'domain': '.twitter.com', 'path': '/'} ,
    {'name': 'guest_id', 'value': 'v1%3A170526598080178325', 'domain': '.twitter.com', 'path': '/'} ,
    {'name': 'ct0', 'value': '3222aa945567780050c74642ba496105077cd428912e864bd3d5246b6886cba3bd0b23e219213dc883b3817632fd34dd43d1a313806426e3c07cd00cf1db7851d0bb710d0df163a73601647d71001698', 'domain': '.twitter.com', 'path': '/'} ,
    {'name': 'twid', 'value': 'u%3D1575975937274806273', 'domain': '.twitter.com', 'path': '/'} ,
    {'name': 'auth_token', 'value': '059cdc89dbb9f2862c9ddabec2c7c337d2e0e135', 'domain': '.twitter.com', 'path': '/'}];

  try {
    // Set cookies before navigating to the URL
    await page.setCookie(...cookies);
    await page.goto(url, { timeout: 60000 });
    await page.waitForSelector('div[data-testid="UserDescription"]', { timeout: 10000 });
    const divContent = await page.$eval('div[data-testid="UserDescription"]', div => div.textContent);
    dic[screenName] = divContent;
  } catch (error) {
    console.log(`${url} not found`);
  } finally {
    await page.close();
    await browser.close();
  }
}

async function main(usernames) {
  await Promise.all(usernames.map(scraper));
}

const step = 20;

(async () => {
  for (let sp = 0; sp < screenNames.length; sp += step) {
    await main(screenNames.slice(sp, sp + step));
    await fs.writeFile(`Data/bios${sp / step}.json`, JSON.stringify(dic));
    console.log(`Got the ${sp / step + 1} batch of users`);
    await new Promise(resolve => setTimeout(resolve, 340)); // Sleep for 0.34 seconds
    dic = {}; // Clear the dictionary
  }
})();
