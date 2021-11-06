from playwright.async_api import async_playwright
import time 
import asyncio
async def ZAC_login(page,USERNAME,PASSWORD):
    await page.goto("https://noar.zac.ai/noar_test/User/user_logon.asp")
    await page.fill('#username',USERNAME)
    await page.fill('#password',PASSWORD)
    await page.click('.cv-button')
    await page.wait_for_selector('.notice_gadget-c')

async def GETCASTING(page):
    await page.click('.menu-trigger')
    await page.wait_for_selector('a[href="/noar_test/b/output"]')
    await page.click('a[href="/noar_test/b/output"]')
    await page.wait_for_selector(":nth-match(a:has-text('キャスティング一覧'),2)")
    await page.click(":nth-match(a:has-text('キャスティング一覧'),2)")
    print(page.url)
    #ここでCSVボタンを押下してダウンロードを実行する
    await page.wait_for_selector('//html/body/form[2]/table/tbody/tr/td/table.bor_a/tbody/tr[4]/td[5]/input.btn_red')
    #await page.wait_for_selector('xpath=//html/body/form[2]/table/tbody/tr/td/table[3]/tbody/tr[4]/td[5]/input[2]')
    #await page.click('xpath=//html/body/form[2]/table/tbody/tr/td/table[3]/tbody/tr[4]/td[5]/input[2]')

async def main():
    USERNAME = "hisadakn"
    PASSWORD = "e-m1mark3"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await ZAC_login(page,USERNAME,PASSWORD)
        await GETCASTING(page)
        await browser.close()

asyncio.run(main())