import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import datetime

def generate_rss():
    url = ' https://www.xnxx.com/search/ 国产'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': ' https://www.xnxx.com/ '
    }
    
    try:
        # 发起请求
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 创建RSS
        fg = FeedGenerator()
        fg.title('XNXX国产视频更新')
        fg.link(href=url)
        fg.description('国产视频每日更新')
        
        # 提取视频
        for item in soup.select('.thumb-block'):
            title_elem = item.select_one('.thumb-under p a')
            link_elem = item.select_one('.thumb a')
            
            if not (title_elem and link_elem):
                continue
                
            title = title_elem.text.strip()
            link = ' https://www.xnxx.com ' + link_elem['href']
            metadata = item.select_one('.metadata').text if item.select_one('.metadata') else ""
            
            # 添加条目
            fe = fg.add_entry()
            fe.title(title)
            fe.link(href=link)
            fe.description(f"时长/清晰度: {metadata}")
            fe.guid(link)
        
        # 生成文件
        fg.rss_file('feed.xml')
        print("RSS生成成功！")
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    generate_rss()
