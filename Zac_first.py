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
    await page.click('a[href="/noar_test/b/output"]')
    await page.click(":nth-match(a:has-text('キャスティング一覧'),2)")
    print(page.url)
    #ここでCSVボタンを押下してダウンロードを実行する
    classic_window = await (await page.query_selector("#classic_window")).content_frame()
    #CSSセレクタ JSセレクタ　full_Xpathすべてなぜか動かない
    async with page.expect_download() as download_info:
        await classic_window.click("input.btn_red[name='CSV']", force=True)
    download = await download_info.value
    path = download.suggested_filename
    await download.save_as(path)

async def main():
    USERNAME = "hisadakn"
    PASSWORD = "e-m1mark3"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        await ZAC_login(page,USERNAME,PASSWORD)
        await GETCASTING(page)
        await browser.close()

asyncio.run(main())