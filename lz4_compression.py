from timeit import default_timer
import lz4.frame
import numpy as np

with open("./data/moby.txt", "r") as f:
    text = f.read()

ascii_array = np.frombuffer(text.encode("ascii"), dtype=np.uint8)

symbols, inverse = np.unique(ascii_array, return_inverse=True)
inverse = inverse.astype(np.int32)

inv_arr = inverse.astype(np.int32)

start_time = default_timer()
compressed = lz4.frame.compress(
    inv_arr.tobytes(), compression_level=lz4.frame.COMPRESSIONLEVEL_MAX
)
encoding_time = default_timer() - start_time
compressed_size = len(compressed)

start_time = default_timer()
decompressed = np.frombuffer(lz4.frame.decompress(compressed), dtype=np.int32)
decoding_time = default_timer() - start_time
decompressed_bytes = symbols[decompressed]
decompressed_text = bytes(decompressed_bytes).decode("ascii")

if decompressed_text == text:
    print("Decompression successful. The files match.")
else:
    raise RunTimeError("Decoded text does not match original text!")

print(f"Original size\t\t: {len(ascii_array.tobytes()):,}\t bytes")
print(f"Compressed size\t\t: {len(compressed):,}\t bytes")
print(f"Compression time\t: {1000 * encoding_time:.4f}\t ms")
print(f"Decompression time\t: {1000 * decoding_time:.4f}\t ms")
print(f"Compression ratio\t: {len(ascii_array) / len(compressed):.2f}")
