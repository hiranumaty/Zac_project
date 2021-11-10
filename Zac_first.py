from playwright.async_api import async_playwright
from glob import glob
import time 
import asyncio
import codecs
import os
import datetime
def FileCheck(path):
    #自作のエクセプションを投げるようにしたい
    today = datetime.date.today()
    if os.path.exists(path):
        modify_datestamp = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        modify_date = modify_datestamp.date()
        if modify_date == today:
            if not glob("\.crdownload$"):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
def ChangeFileEncode(Filepath):
    """
    エンコーディングの変更
    Shift_JISからUTF-8(BOM)へ
    """
    fin = codecs.open(Filepath,"r",encoding="shift_jis")
    temp = "temp.csv"
    fout = codecs.open(temp,"w",encoding="utf_8_sig")
    for row in fin:
        fout.write(row)
    fin.close()
    fout.close()
    os.remove(Filepath)
    os.rename(temp,Filepath)
    
async def ZAC_login(page,USERNAME,PASSWORD):
    await page.goto("https://noar.zac.ai/noar_test/User/user_logon.asp")
    await page.fill('#username',USERNAME)
    await page.fill('#password',PASSWORD)
    await page.click('.cv-button')
    await page.wait_for_selector('.notice_gadget-c')
    await page.click('.menu-trigger')

async def GETCASTING(page):
    """
    キャスティング一覧の出力
    """
    window = page.main_frame
    await window.click('a[href="/noar_test/b/output"]')
    await window.click(":nth-match(a:has-text('キャスティング一覧'),2)")
    classic_window = await (await window.query_selector("#classic_window")).content_frame()
    async with page.expect_download() as download_info:
        await classic_window.click("input.btn_red[name='CSV']", force=True)
    download = await download_info.value
    path = download.suggested_filename
    await download.save_as(path)
    ChangeFileEncode(path)
    FileCheck(path)
    #ここでファイルが存在するかのチェックを行う

async def GetExpectedCost(page):
    """
    予定原価の出力
    """
    window = page.main_frame
    #class global-menu がクラスis-openedを保持しているか
    await window.click('a[href="/noar_test/b/output"]')
    await window.click(":nth-match(a:has-text('予定原価CSV出力'),2)")
    classic_window = await (await window.query_selector("#classic_window")).content_frame()
    #モードと日付は後で指定が入りそう
    await classic_window.select_option("select[name='date_type']",value="4")
    await classic_window.fill("input.numeric:nth-child(2)","2021")
    await classic_window.fill("input.numeric:nth-child(4)","11")
    await classic_window.fill("input.numeric:nth-child(5)","1")
    await classic_window.fill("input.numeric:nth-child(7)","2021")
    await classic_window.fill("input.numeric:nth-child(9)","11")
    await classic_window.fill("input.numeric:nth-child(10)","30")
    
    await classic_window.check("input[name='id_progress_status_list'][value='1']")
    await classic_window.check("input[name='id_progress_status_list'][value='2']")
    async with page.expect_download() as download_info:
        await classic_window.click("input.btn_red[name='Submit']", force=True)
    download = await download_info.value
    path = download.suggested_filename
    await download.save_as(path)
    ChangeFileEncode(path)
    FileCheck(path)
    #ここでファイルが存在するかのチェックを行う
async def GetMatterCSV(page):
    window = page.main_frame
    await window.click('a[href="/noar_test/b/output"]')
    await window.click(":nth-match(a:has-text('案件CSV出力'),2)")
    classic_window = await (await window.query_selector("#classic_window")).content_frame()
    await classic_window.select_option("select[name='id_type_date']",value="19")
    await classic_window.fill("input.numeric:nth-child(2)","2021")
    await classic_window.fill("input.numeric:nth-child(4)","11")
    await classic_window.check("input[name='id_progress_status_list'][value='1']")
    await classic_window.check("input[name='id_progress_status_list'][value='2']")
    async with page.expect_download() as download_info:
        await classic_window.click("input.btn_red[name='output']", force=True)
    download = await download_info.value
    path = download.suggested_filename
    await download.save_as(path)
    ChangeFileEncode(path)
    FileCheck(path)
    
async def main():
    USERNAME = "hisadakn"
    PASSWORD = "e-m1mark3"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        await ZAC_login(page,USERNAME,PASSWORD)
        await GETCASTING(page)
        await GetExpectedCost(page)
        await GetMatterCSV(page)
        await browser.close()

asyncio.run(main())