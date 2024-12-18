# English-Phonetic-Symbols-Comparison :
# https://memo.doraemon-yu.site/English-Phonetic-Symbols-Comparison/
# about "utf-8-sig" :
# https://docs.python.org/3/library/codecs.html#encodings-and-unicode
# word api :
# https://api.dictionaryapi.dev/api/v2/entries/en/imperative


import httpx
import asyncio


async def fetch_info(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response


async def main(block_list, query_url):
    groups = []
    for block in block_list:
        tasks = [fetch_info(query_url+line[0]) for line in block]
        groups.append(asyncio.gather(*tasks))

    # await asyncio.gather(
    # *(
    # asyncio.gather(  *(fetch() for line in block)   )
    # for block in block_list
    # )
    # )
    response_groups = await asyncio.gather(*groups)
    return response_groups


def sanitize(phone):
    if isinstance(phone, int):
        return str(phone)
    p = phone.strip()[1:-1]
    # '[əˈkædˌəˌmi]''[ˈdɹiːˌmi]''[ˈfɪlmi]'
    # [əˈkadəmi]/əˈkæd.ə.mi/ /ˈdriː.mi/
    # p = p.replace('\'', 'ˈ').replace('.', 'ˌ').replace('a', 'æ')
    p = p.replace('ɹ', 'r').replace('.', '')
    p = p.replace('l̩', 'l')
    p = p.replace('i', 'ɪ').replace('ɪː', 'iː')
    p = p.replace('ɛ', 'e')
    phone = f"[{p}]"
    return phone


def parse_response(response):
    if response.status_code == 200:
        word_info = response.json()[0]

        if 'phonetic' in word_info:
            phone = sanitize(word_info['phonetic'])
            return (phone, 1)
        else:
            for ind, phonetic in enumerate(word_info.get('phonetics')):
                if 'text' in phonetic and phonetic.get('text'):
                    phone = sanitize(phonetic['text'])
                    return (phone, ind+1)
            return (response.reason_phrase, 9)
    else:
        return (response.reason_phrase, 0)


def create_words_file(config):

    with open(config.words_proto_file, 'r', encoding="utf-8-sig") as f:
        data = f.readlines()

    # =================================================
    block_list = []
    current_block = []

    for line in data:
        stripped_line = line.strip()
        if stripped_line:
            current_block.append(stripped_line.split())
        elif current_block:
            block_list.append(current_block)
            current_block = []

    if current_block:
        block_list.append(current_block)

    # block_list = [[['academy', '学院'], ['aeronomy', '航空学']],
    #               [['dreamy', '恍惚的'], ['filmy', '薄膜的']]]
    # =================================================

    # words =[]
    # for block in block_list : words.extend([k[0] for k in block])
    words = [k[0] for block in block_list for k in block]
    words_ind = 0

    response_group_list = asyncio.run(main(block_list, config.QUERYURL))


    for block, response_list in zip(block_list, response_group_list):
        for line, response in zip(block, response_list):
            (phone, stat) = parse_response(response)
            line.insert(1, phone)
            words[words_ind] += f' {stat}'
            words_ind += 1


    for k in words:
        print(k)
    # ========================
    def fun(lines): return '\n'.join(' '.join(line) for line in lines)
    block_text = map(fun, block_list)
    output_text = '\n\n'.join(block_text)

    with open(config.words_file, 'w', encoding="utf-8-sig") as file:
        file.write(output_text)


# Run the tasks
if __name__ == "__main__":
    from configuration import config
    create_words_file(config)
# ==========================
