from patchright.async_api import async_playwright
from playwright_stealth import Stealth
import asyncio
import pandas as pd
import numpy as np
import random
import re
#listing data
title=[]
description=[]
budget=[]
posted_date=[]
proposes_count=[]
client_name=[]
acceptance_rating=[]
status=[]
job_url=[]
skill_sets=[]
time_interval=[]
#sleeping variable
sleep_time = random.uniform(1, 2.4)
#auto-web scraping
async def mostaql_scrape(search=None,cancel=False):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36")
        stealth = Stealth()
        await stealth.apply_stealth_async(context)
        page = await context.new_page()
        await context.route("**/*.{png,jpg,jpeg,gif,webp,css,woff,woff2,mp4}", lambda route: route.abort())
        await page.goto('https://mostaql.com/',timeout=30000)
        await asyncio.sleep(sleep_time)
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(sleep_time)
        await page.locator("li a.hsoub-menu-item-link[href='https://mostaql.com/projects']", ).click()
        await asyncio.sleep(sleep_time)
        if search is not None:
            await page.locator("div input#project__title").fill(search)
            await page.keyboard.press("Enter")
        else:
            await page.locator("div input#project__title").fill("")
            await page.keyboard.press("Enter")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(sleep_time)
        async def detailed_scraping(url, sema):
            async with sema:
                if not isinstance(url, str) or not url.startswith("http"):
                    budget.append(np.nan)
                    description.append(np.nan)
                    status.append(np.nan)
                    time_interval.append(np.nan)
                    acceptance_rating.append(np.nan)
                    skill_sets.append([])
                else:
                    detail_page = await context.new_page()
                    await detail_page.goto(url)
                    await detail_page.wait_for_load_state("networkidle")
                    await asyncio.sleep(sleep_time)
                    if cancel:
                        await browser.close()
                        return None
                    else:
                        pass
                    try:
                        budget.append(await detail_page.locator('#project-meta-panel span[dir="rtl"]').inner_text())
                    except Exception:
                        budget.append(np.nan)
                    if cancel:
                        await browser.close()
                        return None
                    else:
                        pass
                    try:
                        description.append(await detail_page.locator(
                            'div#projectDetailsTab div div.text-wrapper-div.carda__content').inner_text())
                    except Exception:
                        description.append(np.nan)
                    if cancel:
                        await browser.close()
                        return None
                    else:
                        pass
                    try:
                        status.append(
                            await detail_page.locator('div.meta-row div.meta-value bdi.label.label').filter(
                                visible=True).inner_text())
                    except Exception:
                        status.append(np.nan)
                    if cancel:
                        await browser.close()
                        return None
                    else:
                        pass
                    try:
                        time_loc = detail_page.locator("div.meta-row").nth(3).filter(has_text="مدة التنفيذ")
                        time_interval.append(await time_loc.locator("div.meta-value").inner_text())
                    except Exception:
                        time_interval.append(np.nan)
                    try:
                        acceptance_rating.append(await detail_page.locator(
                            "tbody tr td label.label.label-rating-good, tbody tr td label.label.label-rating-poor").filter(
                            visible=True).inner_text())
                    except Exception:
                        acceptance_rating.append(np.nan)
                    if cancel:
                        await browser.close()
                        return None
                    else:
                        pass
                    try:
                        await detail_page.wait_for_selector("ul li a.tag bdi", timeout=40000)
                        await detail_page.locator("ul li a.tag bdi").filter(visible=False).first.wait_for(
                            state="attached")
                        skill_locs = await detail_page.locator("ul li a.tag bdi").filter(visible=False).all()
                        skill_list = [await loc.inner_text() for loc in skill_locs]
                        skill_sets.append(skill_list)
                    except Exception:
                        skill_sets.append([])
                    await detail_page.close()
                    await asyncio.sleep(sleep_time)
        while True and not cancel:
            current_url = []
            next_button = page.locator('ul li a.page-link[rel="next"][href]')
            projects = await page.locator("table tbody tr.project-row").all()
            if cancel:
                await browser.close()
                return None
            else:
                pass
            for project in projects:
                try:
                    await asyncio.sleep(sleep_time)
                    title.append(await project.locator("div h2 a").inner_text())
                except Exception:
                    title.append(np.nan)
                if cancel:
                    await browser.close()
                    return None
                else:
                    pass
                try:
                    job_url.append(await project.locator("a.details-url").get_attribute("href"))
                    current_url.append(await project.locator("a.details-url").get_attribute("href"))
                except Exception:
                    job_url.append(np.nan)
                    current_url.append(None)
                if cancel:
                    await browser.close()
                    return None
                else:
                    pass
                try:
                    posted_date.append(await project.locator("ul li time").get_attribute("datetime"))
                except Exception:
                    posted_date.append(np.nan)
                if cancel:
                    await browser.close()
                    return None
                else:
                    pass
                try:
                    client_name.append(await project.locator("ul li bdi").inner_text())
                except Exception:
                    client_name.append(np.nan)
                if cancel:
                    await browser.close()
                    return None
                else:
                    pass
                try:
                    proposes_count.append(await project.locator("ul li.text-muted").get_by_text(
                        re.compile(r"عرض|عرضان|عروض")).inner_text())
                except Exception:
                    proposes_count.append(np.nan)
            if cancel:
                await browser.close()
                return None
            else:
                pass
            try:
                semaphore = asyncio.Semaphore(5)
                tasks = [detailed_scraping(url, semaphore) for url in current_url]
                await asyncio.gather(*tasks, return_exceptions=True)
                current_url.clear()
            except Exception:
                budget.append(np.nan)
                description.append(np.nan)
                status.append(np.nan)
                time_interval.append(np.nan)
                acceptance_rating.append(np.nan)
                skill_sets.append([])
            if cancel:
                await browser.close()
                return None
            else:
                pass
            if await next_button.count() > 0 and await next_button.is_visible():
                await next_button.click()
                continue
            else:
                await browser.close()
                break
    # building dataset
    max_len = max(
        [len(title), len(description), len(status), len(acceptance_rating), len(budget), len(job_url),
         len(skill_sets),
         len(client_name), len(proposes_count), len(time_interval), len(posted_date)])
    platform = ["Mostaql"] * max_len
    mostaql_jobs = pd.DataFrame({
        "Title": pd.Series(title),
        "Description": pd.Series(description),
        "Client Name": pd.Series(client_name),
        "Budget": pd.Series(budget),
        "Status": pd.Series(status),
        "Posted Date": pd.Series(posted_date),
        "Accepting Percentage": pd.Series(acceptance_rating),
        "Skill Sets": pd.Series(skill_sets),
        "Number of Proposals": pd.Series(proposes_count),
        "Time Interval (Days)": pd.Series(time_interval),
        "Platform": pd.Series(platform),
        "URL": pd.Series(job_url)
    })
    # return mostaql_jobs
    return mostaql_jobs