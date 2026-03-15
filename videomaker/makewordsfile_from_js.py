# English-Phonetic-Symbols-Comparison :
# https://memo.doraemon-yu.site/English-Phonetic-Symbols-Comparison/
# about "utf-8-sig" :
# https://docs.python.org/3/library/codecs.html#encodings-and-unicode
# word api :
# https://api.dictionaryapi.dev/api/v2/entries/en/imperative



def sanitize(phone):
    if isinstance(phone, int):
        return str(phone)
    p = phone.strip()[1:-1]
    # '[əˈkædˌəˌmi]''[ˈdɹiːˌmi]''[ˈfɪlmi]'
    # [əˈkadəmi]/əˈkæd.ə.mi/ /ˈdriː.mi/
    # p = p.replace('\'', 'ˈ').replace('.', 'ˌ').replace('a', 'æ')

    p = p.replace('\'', 'ˈ').replace('(','').replace(')','')
    p = p.replace('.', '')
    p = p.replace('ɹ', 'r').replace('ɾ', 't')
    p = p.replace('l̩', 'l').replace('ɫ̩','l')
    p = p.replace('i', 'ɪ').replace('ɪː', 'iː')
    p = p.replace('ɛ', 'e')  # IPA88
    phone = f"[{p}]"
    return phone


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
    print(len(words))
    print(words)

    response_list = ['[pə(r)ˈsiːv]', "['pɜːsept]", '[pə(r)ˈsent]', '[ˈpɜː(r)tʃəs]', '[ˈpɔː(r)s(ə)lɪn]', "['tʃaɪnə]", "[sə'ræmɪk]", "[prɪ'ses]", '[prɪˈsiːd]', "['presɪdəns]", "['presɪdənt]", "['prezɪdənt]", '[ˈprez(ə)nt]', '[ˈprez(ə)ns]', '[prɪˈzɜː(r)v]', '[preˈstiːʒ]', '[ˈpriːsept]', '[ˌɪntə(r)ˈsept]', "['preʃəs]", "[prɪ'saɪs]", "[prɪ'saɪsli]", "[prɪ'sɪʒ(ə)n]", '[prɒˈsperəti]', "['prɒspekt]", "[.ekspek'teɪʃ(ə)n]", '[ˈprɒˌsteɪt]', '[prəˈsiːdʒə(r)]', '[ˈprəʊses]', '[ˈprəʊˌsesə(r)]', '[prəˈsiːd]', "['præktɪk(ə)l]", "['præktɪs]", '[prɪˈkɔːʃ(ə)n]', '[ˈpreʃə(r)]', '[prɪˈzjuːm]', '[praɪs]', "['praɪsləs]", "['prɪk(ə)l]", "['pɪk(ə)l]", '[ˈprɪz(ə)m]', "['prɪz(ə)n]"]
    
    words_ind = 0
    for block in block_list:
        for line in block:
            line.insert(1,sanitize(response_list[words_ind]))
            # line.insert(1,response_list[words_ind])
            words_ind += 1


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
