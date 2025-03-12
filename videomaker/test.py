import requests
import asyncio
import httpx
from PIL import Image, ImageDraw, ImageFont


def shifts_operation_with_negative():


    # The hash value is different when invoked a second time 
    # because recent releases of Python (versions 3.3 and up),
    # by default, apply a random hash seed for this function. 
    # The seed changes on each invocation of Python. 
    # Within a single instance, the results will be identical.
    val = hash('sometext')
    leng = (val.bit_length() + 7) // 8
    res = 0
    for k in range(leng):
        res ^= val & 0xff
        val = val >> 8
    print(res)

    pass


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    ":scheme": "https",
    ':authority': 'api.dictionaryapi.dev'
}


async def fetch_info(url):
    try:
        async with httpx.AsyncClient() as client:
            print(f"Fetching info from {url}")
            response = await client.get(url, headers=headers)
            # response = await client.get(url)
            print("++++++++++")
            response.raise_for_status()  # 如果响应状态码不是200系列，将引发HTTPError
            return response.text  # 或者您可以选择返回其他内容，如response.json()
    except httpx.HTTPStatusError as exc:
        print(f"HTTP error occurred: {exc}")
    except httpx.RequestError as exc:
        # RequestError 是 ConnectError 和 other network-related errors 的父类
        print(f"Request error occurred: {exc}")
    except Exception as exc:
        # 捕获其他未预料的异常
        print(f"An unexpected error occurred: {exc}")
    pass
if __name__ == "__main__":

    # 使用 asyncio 运行 fetch_info 函数
    url = "https://api.bilibili.com/x/v2/dm/web/history/seg.so"
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/briar"
    # asyncio.run(fetch_info(url))
    # res = requests.get(url)
    # print(res.text)
    shifts_operation_with_negative()
    pass
