from playwright.async_api import async_playwright
import asyncio
from Reading_Data import get_screen_names
import pandas as pd
import time
from Get_Cookies import get_cookies


auth_token, twid, ct0 = get_cookies()

screen_names = get_screen_names()

dic = {}
async def scraper(screen_name):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless = True ,devtools=False)
        context = await browser.new_context()
        cookies = [
        {'name': 'ct0', 'value': ct0, 'domain': '.twitter.com', 'path': '/'} ,
        {'name': 'twid', 'value': twid, 'domain': '.twitter.com', 'path': '/'} ,
        {'name': 'auth_token', 'value': auth_token, 'domain': '.twitter.com', 'path': '/'}]
        await context.add_cookies(cookies)
        page = await context.new_page()
        url = "https://twitter.com/"+screen_name
        try:
            await page.goto(url, timeout = 60000)
            await page.wait_for_selector('div[data-testid="UserDescription"]', timeout=10000)
            div_content = await page.inner_text('div[data-testid="UserDescription"]')
            # print(f"Content of the div: {div_content}")
            dic[screen_name] = div_content

        except:
            print(f"{url} not found")
        finally:
            await page.close()  # Close the browser.
            await browser.close()

async def main(usernames):
    await asyncio.gather(*(scraper(screen_name) for screen_name in usernames))

step = 20

for sp in range(0, len(screen_names), step):
    asyncio.run(main(screen_names[sp:sp+step]))

    df = pd.DataFrame.from_dict(dic, orient = 'index')
    df.to_excel(f"Data/bios{sp//step + 1}.xlsx")
    print(f"Got the {sp//step + 1} batch of users")
    time.sleep(1)
    dic.clear()

