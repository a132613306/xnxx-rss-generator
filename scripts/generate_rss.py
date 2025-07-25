import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import datetime
import os

def parse_xnxx():
    url = ' https://www.xnxx.com/search/ 国产'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    fg = FeedGenerator()
    fg.title('XNXX 国产视频更新')
    fg.link(href=url)
    fg.description('XNXX“国产”关键词每日更新视频')
    
    # 解析视频列表
    for item in soup.select('.thumb-block'):
        title_elem = item.select_one('.thumb-under p a')
        link_elem = item.select_one('.thumb a')
        if not title_elem or not link_elem:
            continue
            
        title = title_elem.text.strip()
        link = ' https://www.xnxx.com ' + link_elem['href']
        
        # 提取元数据（观看量、时长、清晰度）
        metadata = item.select_one('.metadata').text if item.select_one('.metadata') else "N/A"
        
        # 生成 RSS 条目
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=link)
        fe.description(f"元数据: {metadata}")
        fe.guid(link)  # 使用链接作为唯一标识
    
    # 保存 RSS 文件
    fg.rss_file('feed.xml')
    print("RSS 生成成功！")

if __name__ == '__main__':
    parse_xnxx()
