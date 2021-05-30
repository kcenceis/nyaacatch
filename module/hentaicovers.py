from bs4 import BeautifulSoup
import Utils

def getImageURL(url, nyaa_list):
    # 获取封面 https://hentai-covers.site/images/2019/09/05/seiginoYbutachanbon.jpg
    # 获取图片网页链接
    url = url.replace(r'表紙 / Cover', '').replace('**', '').replace('Cover', '').strip()
    # 请求图片网页链接
    requestCover = Utils.getRequest(url)
    # 抓取IMAGE真实url
    soup = BeautifulSoup(requestCover.text, 'html.parser')
    for kk in soup.find_all('link', rel='image_src'):
        Utils.download_img(kk['href'], nyaa_list)
    # for kk in soup.find_all('a', 'btn btn-download default'):
    #     print("测试kk:"+kk)
    #     # 下载图片
    #     Utils.download_img(kk['href'], mBookTitle)
