import time 
import asyncio
import codecs
import os
import datetime
import traceback
from Module import ConnectPlaywright
from playwright.async_api import async_playwright
from glob import glob

async def main():
    USERNAME = "hisadakn"
    PASSWORD = "e-m1mark3"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        Connection = ConnectPlaywright.ConnectZac(browser)
        try:
            await Connection.Login(USERNAME,PASSWORD)
            await Connection.GETCASTING()
            await Connection.GetExpectedCost()
            await Connection.GetMatterCSV()
        except ConnectPlaywright.MakeFileException as e:
            error_msg = traceback.format_exception_only(type(e), e)
            print(error_msg)
            print("エラーが発生したため動作を終了しました")
        finally:
            await Connection.logout()
asyncio.run(main())