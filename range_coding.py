from timeit import default_timer
import constriction
import numpy as np

with open("./data/moby.txt", "r") as f:
    text = f.read()

ascii_array = np.frombuffer(text.encode("ascii"), dtype=np.uint8)

symbols, inverse = np.unique(ascii_array, return_inverse=True)
inverse = inverse.astype(np.int32)

counts = np.bincount(inverse, minlength=len(symbols)).astype(np.float32)
freqs = counts + 1
model = constriction.stream.model.Categorical(freqs, perfect=False)

start_time = default_timer()
encoder = constriction.stream.queue.RangeEncoder()
encoder.encode(inverse, model)
compressed = encoder.get_compressed()
encoding_time = default_timer() - start_time

start_time = default_timer()
decoder = constriction.stream.queue.RangeDecoder(compressed)
decoded_indices = decoder.decode(model, len(inverse))
decoded_bytes = symbols[decoded_indices]
decoding_time = default_timer() - start_time

decoded_text = bytes(decoded_bytes).decode("ascii")

if decoded_text == text:
    print("Decompression successful. The files match.")
else:
    raise RunTimeError("Decoded text does not match original text!")

print(f"Original size\t\t: {len(ascii_array.tobytes()):,}\t bytes")
print(f"Compressed size\t\t: {len(compressed) + freqs.nbytes:,}\t bytes")
print(f"Compression time\t: {1000 * encoding_time:.4f}\t ms")
print(f"Decompression time\t: {1000 * decoding_time:.4f}\t ms")
print(f"Compression ratio\t: {len(ascii_array) / (len(compressed) + freqs.nbytes):.2f}")
