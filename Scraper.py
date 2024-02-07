from playwright.async_api import async_playwright
import asyncio
from Reading_Data import get_data
import pandas as pd
from Get_Cookies import get_cookies, get_second_cookies
import time

auth_token, twid, ct0 = get_cookies()
auth_token_2, twid_2, ct0_2 = get_second_cookies()

screen_names, index = get_data()

temp_dict = {}


async def scraper(screen_name, context):

    page = await context.new_page()
    url = "https://twitter.com/" + screen_name

    try:
        await page.goto(url, timeout=60000)
        await page.wait_for_selector(
            'div[data-testid="UserDescription"]', timeout=10000
        )

        div_content = await page.inner_text('div[data-testid="UserDescription"]')
        temp_dict[screen_name] = div_content

    except:
        print(f"{url} is probably dead")

    finally:
        await page.close()


async def main(usernames, is_firefox, is_first_account):

    async with async_playwright() as p:
        if is_firefox:
            browser = await p.firefox.launch(headless=True, devtools=False)
        else:
            browser = await p.chromium.launch(headless=True, devtools=False)
        context = await browser.new_context()

        if is_first_account:
            cookies = [
                {"name": "ct0", "value": ct0, "domain": ".twitter.com", "path": "/"},
                {"name": "twid", "value": twid, "domain": ".twitter.com", "path": "/"},
                {
                    "name": "auth_token",
                    "value": auth_token,
                    "domain": ".twitter.com",
                    "path": "/",
                },
            ]

        else:
            cookies = [
                {"name": "ct0", "value": ct0_2, "domain": ".twitter.com", "path": "/"},
                {
                    "name": "twid",
                    "value": twid_2,
                    "domain": ".twitter.com",
                    "path": "/",
                },
                {
                    "name": "auth_token",
                    "value": auth_token_2,
                    "domain": ".twitter.com",
                    "path": "/",
                },
            ]

        await context.add_cookies(cookies)

        await asyncio.gather(
            *(scraper(screen_name, context) for screen_name in usernames)
        )

        await browser.close()


step = 20


for sp in range(0, len(screen_names), step):
    if sp % 6 == 4:
        time.sleep(100)
    asyncio.run(main(screen_names[sp : sp + step], (sp % 6) < 3, (sp % 2) == 1))
    if temp_dict:
        df = pd.DataFrame.from_dict(temp_dict, orient="index")
        df.columns = ["bio"]
        df.to_excel(f"Data/bios{(index + sp)//step + 1}.xlsx")
    print(
        f"Got the #{(index + sp)//step + 1} batch of users, with the total of {len(temp_dict.keys())} rows."
    )
    temp_dict.clear()
