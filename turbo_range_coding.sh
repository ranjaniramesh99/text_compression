#!/bin/sh

turborc="./bin/turborc"

if [ ! -f "$turborc" ]; then
    echo "Error: $turborc not found. Please build it first."
    exit 1
fi

text_file="./data/moby.txt"

if [ ! -f "$text_file" ]; then
    echo "Error: $text_file not found. Please ensure the file exists."
    exit 1
fi

# Get the file size
file_size=$(stat -c%s "$text_file")

# Compress the text file and store the compression time
compressed_file="./data/moby.rc"

start_time=$(date +%s%N)
$turborc -1 -Ft "$text_file" "$compressed_file"
end_time=$(date +%s%N)
compression_time=$((end_time - start_time))

# Get the compressed file size
compressed_size=$(stat -c%s "$compressed_file")

# Decompress the file and store the decompression time
decompressed_file="./data/moby_decomp.txt"
start_time=$(date +%s%N)
$turborc -d "$compressed_file" "$decompressed_file"
end_time=$(date +%s%N)
decompression_time=$((end_time - start_time))

# Get compression ratio
compression_ratio=$(echo "scale=2; $file_size / $compressed_size" | bc)

# Verify the decompressed file matches the original
if cmp -s "$text_file" "$decompressed_file"; then
    echo "Decompression successful. The files match."
else
    echo "Error: Decompressed file does not match the original."
    exit 1
fi

# Clean up all but the original file
rm -f "$compressed_file" "$decompressed_file"

# Output the results
printf "Original size\t\t: %'d\t bytes\n" "$file_size"
printf "Compressed size\t\t: %'d\t bytes\n" "$compressed_size"
printf "Compression time\t: %d\t\t ms\n" "$((compression_time / 1000000))"
printf "Decompression time\t: %d\t\t ms\n" "$((decompression_time / 1000000))"
printf "Compression ratio\t: %.2f\n" "$compression_ratio"
