import pysubs2

file = ""
while not file.endswith(".srt"):
    file = input("Enter the subtitle file name and path (with .srt extension): ")

output = file.replace(".srt", "_shifted.srt")

shift_seconds = float(
    input("Enter number of seconds to shift (negative for backward): ")
)

# Load subtitles
subs = pysubs2.load(file)

# pysubs2 uses milliseconds
subs.shift(ms=int(shift_seconds * 1000))

# Save output
subs.save(output)

print(f" Subtitles shifted by {shift_seconds} seconds and saved as {output}")