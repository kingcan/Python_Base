"""
# @Author: Larkin
# @Date: 2021/8/28 10:07
# @Function:
# @ModuleName:KugouMusic
"""
import re, requests
import parsel, time, os
from multiprocessing.dummy import Pool

headers = {
    "authority": "www.kugou.com",
    "method": "GET",
    "path": "/yy/rank/home/1-6666.html?from=rank",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "cookie": "kg_mid=628fb7a3fc8e7dab426f2846c32b409f; kg_dfid=3dpnap3DlhYI2QcUiN4BVBki; KuGooRandom=66411627561045001; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1627561043,1627564661,1630060779,1630066172; ACK_SERVER_10016=%7B%22list%22%3A%5B%5B%22gzreg-user.kugou.com%22%5D%5D%7D; ACK_SERVER_10017=%7B%22list%22%3A%5B%5B%22gzverifycode.service.kugou.com%22%5D%5D%7D; ACK_SERVER_10015=%7B%22list%22%3A%5B%5B%22gzlogin-user.kugou.com%22%5D%5D%7D; kg_mid_temp=628fb7a3fc8e7dab426f2846c32b409f; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1630066414",
    "pragma": "no-cache",
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
}


# 请求函数
def html_respense(url):
    for i in range(3):
        try:
            resp = requests.get(url, headers=headers, timeout=20)
            resp.encoding = 'utf-8'
            if resp.status_code == 200:
                return resp
        except:
            time.sleep(1)
            print(f"正在尝试重新请求第{i}次")
            continue
    else:
        print("请求失败，请检查")


# 解析1
def html_parsel(resp):
    selector = parsel.Selector(resp.text)
    return selector


def html_parsel2(li):
    print("进程池开启")
    title = li.css("a::attr(title)").get()
    li_href = li.css("a::attr(href)").get()
    resp_2 = html_respense(li_href)
    hashs = re.findall('"Hash":"(.*?)"', resp_2.text)
    album_ids = re.findall('"album_id":(.*?),', resp_2.text)
    file_names = re.findall('"FileName":"(.*?)",', resp_2.text)
    file_names = [name.encode(encoding="utf-8").decode("unicode-escape") for name in file_names]
    for index in zip(hashs, album_ids, file_names):
        # name = index[2].encode(encoding="utf-8")  # 第一步 先将包含有没有解码的unicode字符串str转unicode编码
        # name1 =  name.decode("unicode-escape") #第二步 统一用decode(“unicode-escape”)相当是反向编码.然后再进行utf-8编码
        # print(index[0],index[1],name1)
        music_down(index, title)


# 下载
def music_down(index, title):
    if not os.path.exists(title):
        os.makedirs(title)
    params = {
        "r": "play/getdata",
        "hash": index[0],
        "dfid": "3dpnap3DlhYI2QcUiN4BVBki",
        "mid": "628fb7a3fc8e7dab426f2846c32b409f",
        "platid": "4",
        "album_id": index[1],
        "_": int(time.time() * 1000),
    }
    resp_2 = requests.get(url=callback_url, headers=headers, params=params).json()
    music_down_url = resp_2['data']['play_url']
    print(music_down_url)
    resp_3 = requests.get(url=music_down_url, headers=headers).content
    path = title + "\\" + index[2] + ".mp3"
    with open(path, 'wb')  as f:
        f.write(resp_3)
        print(index[2], "下载完成")


# 入口函数
def main():
    resp_1 = html_respense(start_url)
    selector = html_parsel(resp_1)
    lis = selector.xpath("/html/body/div[3]/div/div[1]/div[1]/ul/li")
    pool.map(html_parsel2, lis)


if __name__ == '__main__':
    pool = Pool(4)
    start_url = "https://www.kugou.com/yy/rank/home"
    callback_url = 'https://wwwapi.kugou.com/yy/index.php?'
    main()
    pool.close()
    print("进程池关闭")
    pool.join()