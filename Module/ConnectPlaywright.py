from playwright.async_api import async_playwright
from glob import glob
import time 
import asyncio
import codecs
import os
import datetime
import re

class MakeFileException(Exception):
    pass

class DatingException(Exception):
    pass

def FileCheck(path):
    """
    ファイルが存在するか
    一時ファイル(*.crdownload)が存在しないか
    """
    today = datetime.date.today()
    if os.path.exists(path):
        modify_datestamp = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        modify_date = modify_datestamp.date()
        if modify_date == today:
            if not glob("\.crdownload$"):
                return True
            else:
                raise MakeFileException("一時ファイルが残っています")
        else:
            raise MakeFileException("ファイルの更新に失敗しました")
    else:
        raise MakeFileException("ファイルの作成に失敗しました")

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

 

class ConnectZac(object):
    def __init__(self,browser,first_date,last_date):
        self.page =None
        self.browser = browser
        self.first_date = first_date
        self.last_date = last_date
        pattern = r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])'
        if not (re.match(pattern,str(self.first_date)) and re.match(pattern,str(self.first_date))):
            raise DatingException("日付の書式が間違っています正しくはYYYY-MM-DDです")
        
        
    async def Login(self,USERNAME,PASSWORD):
        context = await self.browser.new_context(accept_downloads=True)
        self.page = await context.new_page()
        await self.page.goto("https://noar.zac.ai/noar_test/User/user_logon.asp")
        await self.page.fill('#username',USERNAME)
        await self.page.fill('#password',PASSWORD)
        await self.page.click('.cv-button')
        await self.page.wait_for_selector('.notice_gadget-c')
        await self.page.click('.menu-trigger')

    async def GetCastingIchiranCSV(self):
        window = self.page.main_frame
        await window.click('a[href="/noar_test/b/output"]')
        await window.click(":nth-match(a:has-text('キャスティング一覧'),2)")
        classic_window = await (await window.query_selector("#classic_window")).content_frame()
        await classic_window.fill("input[name='y_date_start']",str(self.first_date.year))
        await classic_window.fill("input[name='m_date_start']",str(self.first_date.month))
        await classic_window.fill("input[name='y_date_end']",str(self.last_date.year))
        await classic_window.fill("input[name='m_date_end']",str(self.last_date.month))
        async with self.page.expect_download() as download_info:
            await classic_window.click("input.btn_red[name='CSV']", force=True)
        download = await download_info.value
        path = download.suggested_filename
        await download.save_as(path)
        ChangeFileEncode(path)
        FileCheck(path)
    
    async def GetYoteiGenka(self):
        window = self.page.main_frame
        await window.click('a[href="/noar_test/b/output"]')
        await window.click(":nth-match(a:has-text('予定原価CSV出力'),2)")
        classic_window = await (await window.query_selector("#classic_window")).content_frame()
        await classic_window.select_option("select[name='date_type']",value="4")
        await classic_window.fill("input[name='y_date_start']",str(self.first_date.year))
        await classic_window.fill("input[name='m_date_start']",str(self.first_date.month))
        await classic_window.fill("input[name='d_date_start']",str(self.first_date.day))
        await classic_window.fill("input[name='y_date_end']",str(self.last_date.year))
        await classic_window.fill("input[name='m_date_end']",str(self.last_date.month))
        await classic_window.fill("input[name='d_date_end']",str(self.last_date.day))
        await classic_window.check("input[name='id_progress_status_list'][value='1']")
        await classic_window.check("input[name='id_progress_status_list'][value='2']")
        async with self.page.expect_download() as download_info:
            await classic_window.click("input.btn_red[name='Submit']", force=True)
        download = await download_info.value
        path = download.suggested_filename
        await download.save_as(path)
        ChangeFileEncode(path)
        FileCheck(path)
        
    async def GetAnkenCSV(self):
        window = self.page.main_frame
        await window.click('a[href="/noar_test/b/output"]')
        await window.click(":nth-match(a:has-text('案件CSV出力'),2)")
        classic_window = await (await window.query_selector("#classic_window")).content_frame()
        await classic_window.select_option("select[name='id_type_date']",value="19")
        await classic_window.fill("input[name='y_start']",str(self.first_date.year))
        await classic_window.fill("input[name='m_start']",str(self.first_date.month))
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