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


class ConnectZac(object):
    async def __aenter__(self):
        pass
    def __init__(self,browser):
        self.page =None
        self.browser = browser
    async def Login(self,USERNAME,PASSWORD):
        context = await self.browser.new_context(accept_downloads=True)
        self.page = await context.new_page()
        await self.page.goto("https://noar.zac.ai/noar_test/User/user_logon.asp")
        await self.page.fill('#username',USERNAME)
        await self.page.fill('#password',PASSWORD)
        await self.page.click('.cv-button')
        await self.page.wait_for_selector('.notice_gadget-c')
        await self.page.click('.menu-trigger')

    async def GETCASTING(self):
        window = self.page.main_frame
        await window.click('a[href="/noar_test/b/output"]')
        await window.click(":nth-match(a:has-text('キャスティング一覧'),2)")
        classic_window = await (await window.query_selector("#classic_window")).content_frame()
        async with self.page.expect_download() as download_info:
            await classic_window.click("input.btn_red[name='CSV']", force=True)
        download = await download_info.value
        path = download.suggested_filename
        await download.save_as(path)
        ChangeFileEncode(path)
        FileCheck(path)
    
    async def GetExpectedCost(self):
        window = page.main_frame
        await window.click('a[href="/noar_test/b/output"]')
        await window.click(":nth-match(a:has-text('予定原価CSV出力'),2)")
        classic_window = await (await window.query_selector("#classic_window")).content_frame()
        await classic_window.select_option("select[name='date_type']",value="4")
        await classic_window.fill("input.numeric:nth-child(2)","2021")
        await classic_window.fill("input.numeric:nth-child(4)","11")
        await classic_window.fill("input.numeric:nth-child(5)","1")
        await classic_window.fill("input.numeric:nth-child(7)","2021")
        await classic_window.fill("input.numeric:nth-child(9)","11")
        await classic_window.fill("input.numeric:nth-child(10)","30")
        await classic_window.check("input[name='id_progress_status_list'][value='1']")
        await classic_window.check("input[name='id_progress_status_list'][value='2']")
        async with self.page.expect_download() as download_info:
            await classic_window.click("input.btn_red[name='Submit']", force=True)
        download = await download_info.value
        path = download.suggested_filename
        await download.save_as(path)
        ChangeFileEncode(path)
        FileCheck(path)
    
    
    async def GetMatterCSV(self):
        window = self.page.main_frame
        await window.click('a[href="/noar_test/b/output"]')
        await window.click(":nth-match(a:has-text('案件CSV出力'),2)")
        classic_window = await (await window.query_selector("#classic_window")).content_frame()
        await classic_window.select_option("select[name='id_type_date']",value="19")
        await classic_window.fill("input.numeric:nth-child(2)","2021")
        await classic_window.fill("input.numeric:nth-child(4)","11")
        await classic_window.check("input[name='id_progress_status_list'][value='1']")
        await classic_window.check("input[name='id_progress_status_list'][value='2']")
        async with self.page.expect_download() as download_info:
            await classic_window.click("input.btn_red[name='output']", force=True)
        download = await download_info.value
        path = download.suggested_filename
        await download.save_as(path)
        ChangeFileEncode(path)
        FileCheck(path)
    async def logout(self):
        await self.browser.close()
        
    async def __aexit__(self,exc_type,exc,tb):
        await self.logout()