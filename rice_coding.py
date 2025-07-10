import os
import numpy as np
import rlgr
from timeit import default_timer

temp_file = b"./data/moby.gr"

with open("./data/moby.txt", "r") as f:
    text = f.read()

ascii_array = np.frombuffer(text.encode("ascii"), dtype=np.uint8)

f = rlgr.file(temp_file, 1)  # Open file in write mode

start_time = default_timer()
f.rlgrWrite(ascii_array, 0)
encoding_time = default_timer() - start_time

f.close()

# Get the compressed size
compressed_size = os.path.getsize(temp_file)

f2 = rlgr.file(temp_file, 0)  # Open file in read mode

start_time = default_timer()
read_back = f2.rlgrRead(len(ascii_array), 0)
decoding_time = default_timer() - start_time
assert np.array_equal(np.array(read_back, dtype=np.uint8), ascii_array)

f2.close()

# Delete the temporary file
if os.path.exists(temp_file):
    os.remove(temp_file)

print(f"Original size\t\t: {len(ascii_array.tobytes()):,}\t bytes")
print(f"Compressed size\t\t: {compressed_size:,}\t bytes")
print(f"Compression time\t: {1000 * encoding_time:.4f}\t ms")
print(f"Decompression time\t: {1000 * decoding_time:.4f}\t ms")
print(f"Compression ratio\t: {len(ascii_array) / compressed_size:.2f}")
