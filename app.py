from aiohttp import web
import aiohttp
import asyncio
from bs4 import BeautifulSoup as bs
import json
from db import db_session
from models import Rate
import sqlalchemy
from datetime import datetime

app = web.Application()

async def nbu(session):
    async with session.get('https://bank.gov.ua/ua/markets/exchangerates', ssl=False) as response:

        html = await response.text()
        beauty_version = bs(html, 'html.parser')
        result = beauty_version.find("table", attrs={'id' : 'exchangeRates'})
        table_body = result.find('tbody')
        rows = table_body.find_all("tr")
        for row in rows:
            cols = row.find_all('td')
            if cols[1].text in ["USD", "EUR"]:
                try:
                    rate = Rate(bank="NBU", currency=f"{cols[1].text}", rate=f"{float(cols[4].text.replace(',', '.'))}")
                    db_session.add(rate)
                    db_session.commit()
                except sqlalchemy.exc.IntegrityError:
                    db_session.rollback()
                    print("Data already exist")


async def aval(session):

    async with session.get('https://raiffeisen.ua/currency', ssl=False) as response:

        html = await response.text()
        beauty_version = bs(html, 'html.parser')
        result = beauty_version.find("section", attrs={'id' : 'exchange-rate-app', 'class': 'exchange-rate-app'}).find("index-component")
        EUR_res = float(json.loads(result.attrs[":currencies"])["main"][0]["rates"]["bank"]["rate_sell"])
        USD_res = float(json.loads(result.attrs[":currencies"])["main"][1]["rates"]["bank"]["rate_sell"])

        try:
            rate_usd = Rate(bank="Aval", currency="USD", rate=USD_res)
            rate_eur = Rate(bank="Aval", currency="EUR", rate=EUR_res)
            db_session.add(rate_usd)
            db_session.add(rate_eur)
            db_session.commit()

        except sqlalchemy.exc.IntegrityError:
            db_session.rollback()
            print("Data already exist")


async def privat(session):
    async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5', ssl=False) as response:

        html = await response.json()
        
        try:
            rate_usd = Rate(bank="Privat", currency="USD", rate=html[0]["sale"])
            rate_eur = Rate(bank="Privat", currency="EUR", rate=html[1]["sale"])
            db_session.add(rate_usd)
            db_session.add(rate_eur)
            db_session.commit()
        except sqlalchemy.exc.IntegrityError:
            db_session.rollback()
            print("Data already exist")
    

async def main():

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(nbu(session), aval(session), privat(session))
        

async def rate(request):

    result = db_session.query(Rate).filter(Rate.created==datetime.now().date()).all()
    
    print("\n".join([str(a) for a in result]))

    return web.Response(text="\n".join([str(a) for a in result]))
    
if __name__=="__main__":    

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

    app.add_routes([web.get('/', rate)])
    web.run_app(app)