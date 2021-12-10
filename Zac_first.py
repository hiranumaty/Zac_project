import time 
import asyncio
import datetime
import traceback
import calendar
from Module import ConnectPlaywright
from playwright.async_api import async_playwright

async def main():
    #ここは外部ファイルにするべきか
    USERNAME = "hisadakn"
    PASSWORD = "e-m1mark3"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        today = datetime.date.today()
        t_year = today.year
        t_month = today.month
        last_date_ofMonth = calendar.monthrange(t_year,t_month)[1]
        
        first_date = today - datetime.timedelta(days=today.day - 1)
        last_date = datetime.date(t_year,t_month,last_date_ofMonth)
        try:
            Connection = ConnectPlaywright.ConnectZac(browser,first_date,last_date)
            await Connection.Login(USERNAME,PASSWORD)
            #現在日時を取得してそれを以下の3つに引数として与える
            await Connection.GetCastingIchiranCSV()
            await Connection.GetYoteiGenka()
            await Connection.GetAnkenCSV()
        except (ConnectPlaywright.DatingException,ConnectPlaywright.MakeFileException) as e:
            error_msg = traceback.format_exception_only(type(e), e)
            print(error_msg)
            print("エラーが発生したため動作を終了しました")
        else:
            await Connection.logout()
asyncio.run(main())