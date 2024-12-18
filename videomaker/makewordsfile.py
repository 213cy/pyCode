# English-Phonetic-Symbols-Comparison :
# https://memo.doraemon-yu.site/English-Phonetic-Symbols-Comparison/
# about "utf-8-sig" :
# https://docs.python.org/3/library/codecs.html#encodings-and-unicode
# word api :
# https://api.dictionaryapi.dev/api/v2/entries/en/imperative


import httpx
import asyncio
import time

async def fetch_info(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response

async def main(word_list, query_url):
    tasks = [fetch_info(query_url+word) for word in word_list]
    response_groups = await asyncio.gather(*tasks)
    return response_groups


def sanitize(phone):
    if isinstance(phone, int):
        return str(phone)
    p = phone.strip()[1:-1]
    # '[əˈkædˌəˌmi]''[ˈdɹiːˌmi]''[ˈfɪlmi]'
    # [əˈkadəmi]/əˈkæd.ə.mi/ /ˈdriː.mi/
    # p = p.replace('\'', 'ˈ').replace('.', 'ˌ').replace('a', 'æ')

    p = p.replace('.', '')
    p = p.replace('ɹ', 'r').replace('ɾ', 't')
    p = p.replace('l̩', 'l').replace('ɫ̩','l')
    p = p.replace('i', 'ɪ').replace('ɪː', 'iː')
    p = p.replace('ɛ', 'e')  # IPA88
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
    line_list = []
    linecount_list = [0]
    linecount = 0
    for line in data:
        stripped_line = line.strip()
        if stripped_line:
            line_list.append(stripped_line.split())
            linecount += 1
        elif linecount != linecount_list[-1]:
            linecount_list.append(linecount)

    if linecount != linecount_list[-1]:
        linecount_list.append(linecount)

    # =================================================

    words = [line[0] for line in line_list]
    word_failed_ind = []


    print(' -------- first try -------- total number :',len(words))
    response_word_list = asyncio.run(main(words, config.QUERYURL))

    for index, response in enumerate( response_word_list ):
        (phone, stat) = parse_response(response)
        if stat != 0 :
            line_list[index].insert(1, phone)
        else:
            word_failed_ind.append(index)

    words = [line_list[ind][0] for ind in word_failed_ind]
    word_ind = word_failed_ind
    word_failed_ind = []
    print(words)
    print(' -------- second try -------- total number :',len(words))
    time.sleep(10)
    response_word_list = asyncio.run(main(words, config.QUERYURL))

    for index, response in enumerate( response_word_list ):
        (phone, stat) = parse_response(response)
        if stat != 0 :
            line_list[word_ind[index]].insert(1, phone)
        else:
            word_failed_ind.append(index)
        words[index] += f' {stat}'

    print(words)
    # for k in words:
    #     print(k)
    # =================================================
    lines=[' '.join(line) for line in line_list]
    block_text = []
    for ind in range(len(linecount_list)-1):
        block='\n'.join(lines[linecount_list[ind]:linecount_list[ind+1]])
        block_text.append(block)
    output_text = '\n\n'.join(block_text)

    with open(config.words_file, 'w', encoding="utf-8-sig") as file:
        file.write(output_text)


if __name__ == "__main__":
    from configuration import config
    create_words_file(config)
# ==========================
