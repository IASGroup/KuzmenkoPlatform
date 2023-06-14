from ...contracts.bondarenko.responses import ResultResponse, MainResponse
from fastapi_cache.decorator import cache
from ...data.bondarenko.sqlite.models import Article
from fastapi import Depends, WebSocket
from fastapi.responses import StreamingResponse
import requests
from bs4 import BeautifulSoup
import asyncio
import json
import io
import pandas as pd

DOMAIN = 'https://cyberleninka.ru'

@cache(expire=86400)
async def get_themes():
    response = requests.get(
        url='https://cyberleninka.ru/article',
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
    )
    print(f"Parse: https://cyberleninka.ru/article")
    results = []
    soup = BeautifulSoup(response.text, features='html.parser')
    uls = soup.find_all('ul', { 'class' : 'oecd'})
    for ul in uls:
        lis = ul.find_all('li')
        for li in lis:
            isGroup = 'class' in li.attrs and li.attrs['class'] != [] and 'letter' in li.attrs['class']
            if isGroup:
                results.append({
                    'name': li.text.strip(),
                    'themes': []
                })
            else:
                a = li.find('a')
                if a != None:
                    results[results.__len__() - 1]['themes'].append({
                        'name': a.text.strip(),
                        'link': None if 'href' not in a.attrs or a.attrs['href'] == '' else a.attrs['href']
                    })
    return ResultResponse.success(results)

@cache(expire=86400)
async def get_max_pages(relativeUrl):
    firstPage = requests.get(
        url=f'{DOMAIN}{relativeUrl}',
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
    )
    soup = BeautifulSoup(firstPage.text, features='html.parser')
    svg = soup.find('svg', {'class' : 'paginator_last'})
    a = svg.parent
    splits = a.attrs['href'].split('/')
    maxPage = int(splits[splits.__len__() - 1])
    return ResultResponse.success(maxPage)
    
async def get_article(relativeUrl):
    page = requests.get(
        url=f'{DOMAIN}{relativeUrl}',
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
    )
    text = page.text
    soup = BeautifulSoup(text, features='html.parser')

    title_meta = soup.find('meta',{'name' : 'citation_title'})
    title = None if title_meta == None else title_meta.attrs['content']

    author_metas = soup.find_all('meta', {'name' : 'citation_author'})
    authors = [] if author_metas == [] else list(map(lambda tag: tag.attrs['content'], author_metas))

    journal_meta = soup.find('meta', {'name' : 'citation_journal_title'})
    journal = None if journal_meta == None else journal_meta.attrs['content']

    description_meta = soup.find('meta', {'name' : 'description'})
    description = None if description_meta == None or description_meta.attrs['content'] == ''  else description_meta.attrs['content']

    content_div = soup.find('div', {'itemprop' : 'articleBody'})
    content_ps = map(lambda tag: tag.text, filter(lambda tag: tag.name == 'p', content_div.children))
    content = ' '.join(content_ps)

    theme_i = soup.find('i', {'itemprop' : 'articleSection'})
    theme = None if theme_i == None else theme_i.text

    keywords_meta = soup.find('meta', {'name': 'citation_keywords'})
    keywords = [] if keywords_meta == None or keywords_meta.attrs['content'] == '' else [key.strip() for key in keywords_meta.attrs['content'].split(',')]

    result = {
        'theme': theme,
        'title': title,
        'authors': '^'.join(authors),
        'journal': journal,
        'description': description,
        'content': content,
        'keywords': '^'.join(keywords)
    }
    return ResultResponse.success(result)

async def get_article_links_on_page(relativeUrl):
    page = requests.get(
        url=f'{DOMAIN}{relativeUrl}',
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
    )
    text = page.text
    soup = BeautifulSoup(text, features='html.parser')

    ul = soup.find('ul', {'class' : 'list'})
    links = list(map(lambda tag: tag.find('a').attrs['href'] ,ul.find_all('li')))

    return ResultResponse.success(links)

async def send_message_to_websocket(topic, message, ws_clients):
    async def send_message(socket,msg,top):
        await socket.send_json({
            'topic' : top,
            'message' : msg
        })
        return socket
    tasks = [asyncio.create_task(send_message(ws, message, topic)) for ws in ws_clients]
    if tasks != []:
        await asyncio.wait(tasks)
    return MainResponse.success()