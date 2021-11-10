import time 
import asyncio
import codecs
import os
import datetime
from Module import ConnectPlaywright
from playwright.async_api import async_playwright
from glob import glob

async def main():
    USERNAME = "hisadakn"
    PASSWORD = "e-m1mark3"
    async with ConnectPlaywright.ConnectZac() as C:
        await C.Login(USERNAME,PASSWORD)
        await C.GETCASTING()
        await C.GetExpectedCost()
        await C.GetMatterCSV()
        
asyncio.run(main())