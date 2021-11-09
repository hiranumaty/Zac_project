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
    """
    キャスティング一覧の出力
    """
    await page.click('.menu-trigger')
    await page.click('a[href="/noar_test/b/output"]')
    await page.click(":nth-match(a:has-text('キャスティング一覧'),2)")
    classic_window = await (await page.query_selector("#classic_window")).content_frame()
    async with page.expect_download() as download_info:
        await classic_window.click("input.btn_red[name='CSV']", force=True)
    download = await download_info.value
    path = download.suggested_filename
    await download.save_as(path)
    #ここでファイルが存在するかのチェックを行う
    
async def GetExpectedCost(page):
    """
    予定原価の出力
    """
    await page.click('.menu-trigger')
    await page.click('a[href="/noar_test/b/output"]')
    await page.click(":nth-match(a:has-text('予定原価CSV出力'),2)")
    classic_window = await (await page.query_selector("#classic_window")).content_frame()
    await classic_window.select_option("select[name='date_type']",value="4")
    await classic_window.fill("input.numeric:nth-child(2)","2021")
    await classic_window.fill("input.numeric:nth-child(4)","11")
    await classic_window.fill("input.numeric:nth-child(5)","1")
    await classic_window.fill("input.numeric:nth-child(7)","2021")
    await classic_window.fill("input.numeric:nth-child(9)","12")
    await classic_window.fill("input.numeric:nth-child(10)","30")
    await classic_window.check("input[name='id_progress_status_list'][value='1']")
    await classic_window.check("input[name='id_progress_status_list'][value='2']")
    async with page.expect_download() as download_info:
        await classic_window.click("input.btn_red[name='CSV']", force=True)
    download = await download_info.value
    path = download.suggested_filename
    await download.save_as(path)
    #ここでファイルが存在するかのチェックを行う
    
async def main():
    USERNAME = "hisadakn"
    PASSWORD = "e-m1mark3"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        await ZAC_login(page,USERNAME,PASSWORD)
        #await GETCASTING(page)
        await GetExpectedCost(page)
        await browser.close()

asyncio.run(main())