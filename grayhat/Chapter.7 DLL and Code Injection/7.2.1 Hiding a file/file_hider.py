import sys
import os
import subprocess

# NTFS Alternate Data Stream（ADS）
# https://www.cnblogs.com/zUotTe0/p/13455971.html


if len(sys.argv) == 3:
    file_name = sys.argv[1]
    stream_file_name = sys.argv[2]
    print("get input arguments:")
    print(f"{'sys.argv[0]':12}: {sys.argv[0]} ")
    print(f"{'sys.argv[1]':12}: {file_name} ")
    print(f"{'sys.argv[2]':12}: {stream_file_name} ")

    # Read in the DLL
    fd = open(stream_file_name, "r")
    stream_contents = fd.read()
    fd.close()

    # Now write it out to the ADS
    fd = open(f"{file_name}:{stream_file_name}", "w")
    fd.write(stream_contents)
    fd.close()

    print(f"{stream_file_name} has attached to the {file_name} file")
    exit()

file_name = "aaa"
stream_contents = b"abcdefg"

fd = open(f"{file_name}:bbb", "wb")
fd.write(stream_contents)
fd.close()

file_size = os.path.getsize(file_name)
print(f'File size is: {file_size} Bytes')

file_stats = os.stat(file_name)
# print(file_stats)
print(f'File Size is: {file_stats.st_size} Bytes')

print(66*"=")

# print(os.listdir())

a = subprocess.run(["dir", "aaa"], capture_output=True, shell=True, text=True)
print(a.stdout.split('\n\n')[2])
a = subprocess.run(["dir", "/r", "aaa"],
                   capture_output=True, shell=True, text=True)
print(a.stdout.split('\n\n')[2])
