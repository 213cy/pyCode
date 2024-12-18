import asyncio
import edge_tts
import os


async def amain(voice, folder_words):
    groups = []
    for folder, words in folder_words:
        tasks = [edge_tts.Communicate(word, voice).save(
            f"{folder}/{word}.mp3") for word in words]
        groups.append(asyncio.gather(*tasks))
    await asyncio.gather(*groups)


async def group_task(voice, folder, words):
    tasks = [edge_tts.Communicate(word, voice).save(
        f"{folder}/{word}.mp3") for word in words]
    return await asyncio.gather(*tasks)


async def async_main(voice, folder_words):
    groups = [
        group_task(voice, folder, words) for folder, words in folder_words]
    await asyncio.gather(*groups)


def download_speechs(config):
    file = open(config.words_file, 'r', encoding="utf-8-sig")
    content = file.read().strip()
    file.close()

    block_list = content.split('\n\n')
    page_list = [b.split('\n') for b in block_list]

    folder_words = []
    for ind, page in enumerate(page_list):
        page_folder = f"{config.project_path}/{config.page_folder_prefix}{ind:02d}"
        if not os.path.exists(page_folder):
            os.makedirs(page_folder)
        words = [line.split()[0] for line in page]
        folder_words.append((page_folder, words))
    # asyncio.run(async_main(config.VOICE, folder_words))
    asyncio.run(amain(config.VOICE, folder_words))


def ggg(config):
    file = open(config.words_file, 'r', encoding="utf-8-sig")
    line_list = file.readlines()
    file.close()

    word_list = [line.split(' ')[0] for line in line_list]
    # tasks = [item for page in self.pages for item in page.tasks]

if __name__ == "__main__":
    from configuration import config
    image = download_speechs(config)
