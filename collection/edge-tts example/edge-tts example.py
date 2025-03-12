import asyncio
import edge_tts

choice = 2

if choice == 1 :
    async def amain() -> None:
        text_list = ["clothes", "close"]
        VOICE = "en-GB-RyanNeural"
        tasks = [edge_tts.Communicate(str, VOICE).save(
            f"test.mp3") for str in text_list]
        await asyncio.gather(*tasks)

    asyncio.run(amain())



# ============================

async def amain0():
    await asyncio.sleep(1)
    # tasks = [asyncio.sleep(1), asyncio.sleep(1)]
    tasks = [asyncio.sleep(t) for t in range(1, 3)]
    await asyncio.gather(*tasks)

if choice == 2 :
    async def amain1() -> None:
        TEXT = """这个男人叫小帅，他正躲在屋顶，而他的女友金发妹正在找他"""
        VOICE = "zh-CN-YunxiNeural"
        communicate = edge_tts.Communicate(TEXT, VOICE)
        await communicate.save("test.mp3")
    asyncio.run(amain1())

async def amain2() -> None:
    # await edge_tts.list_voices()
    #  !!!raise "RuntimeError('Event loop is closed')" exception at exit!!!
    voices = await edge_tts.VoicesManager.create()

    # voice = voices.find(Gender="Male", Language="en")
    # voice = voices.find(Gender="Male", Language="zh")
    voice = voices.find(Locale="en-GB")

    TEXT = "Hello World!"
    tasks = [edge_tts.Communicate(TEXT, v["Name"]).save(
        f"sounds/{v['ShortName']}.mp3") for v in voice]
    await asyncio.gather(*tasks)


# ============================


print('done!')