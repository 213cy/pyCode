
# https://www.cnblogs.com/ranson7zop/p/7657874.html

import winsound

# 参数配置
sample_rate = 44100 // 2  # 22050Hz
freq = 440  # hz

samples_per_cycle = sample_rate // freq
coff = 0x8F // samples_per_cycle

audio_data = b''.join([bytes([0, int(coff*i) & 0xff])
                             for i in range(samples_per_cycle)])
total_samples = int(freq*samples_per_cycle)  # duration ~~= 1

audio_format_fix = 1        # PCM格式
num_channels_fix = 1         # 单声道
bytes_per_sample = 2        # 2字节采样

# 计算关键参数
bits_per_sample = bytes_per_sample * 8     # 16位采样,位深度
block_align = num_channels_fix * bytes_per_sample  # 块对齐 = 声道数 × 位深度/8
byte_rate = sample_rate * block_align          # 字节率 = 采样率 × 块对齐
# total_samples = int(sample_rate * duration)    # 总样本数
data_size = total_samples * block_align        # 音频数据大小

# RIFF文件头计算
riff_size = 36 + data_size  # 文件总大小（fmt块24+data头8+数据）
riff_header = b'RIFF' + riff_size.to_bytes(4, 'little') + b'WAVE'

# fmt块参数（严格小端序）
fmt_chunk = (
    b'fmt ' +
    b'\x10\x00\x00\x00' +  # 无附加信息时的块大小(16字节)
    audio_format_fix.to_bytes(2, 'little') +  # 音频格式
    num_channels_fix.to_bytes(2, 'little') +  # 声道数
    sample_rate.to_bytes(4, 'little') +  # 采样率
    byte_rate.to_bytes(4, 'little') +    # 字节率
    block_align.to_bytes(2, 'little') +  # 块对齐
    bits_per_sample.to_bytes(2, 'little')  # 位深度
)

assert len(fmt_chunk) == int.from_bytes(
    fmt_chunk[4:7], 'little') + 8, "fmt块大小错误"

# data块参数
data_header = b'data' + data_size.to_bytes(4, 'little')


# 组合完整WAV文件
wav_bytes = riff_header + fmt_chunk + data_header + freq * audio_data

# 验证关键参数
assert len(wav_bytes) == 36 + data_size + 8, "文件总大小错误"

if 0:
    with open('aaa.wav', 'wb') as f:  # 'wb'模式表示二进制写入
        f.write(wav_bytes)

    winsound.PlaySound('aaa.wav', winsound.SND_FILENAME)

winsound.PlaySound(wav_bytes, winsound.SND_MEMORY)
