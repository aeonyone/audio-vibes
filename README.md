audio-vibes - apply aesthetic effects to an audio from a file or a microphone

# INSTALLATION
Clone repository 

Install requirements
```
pip install -r requirements.txt
```

# USAGE
```
python audio-vibes.py -i INPUT_PATH [-o OUTPUT_PATH] -v VIBE [-r]
```
Valid input path is a relative file path or a youtube url
Valid output path is a relative file path
Valid vibe is one of the following:
- bathroom_at_club
- bathroom_at_party

## Options
```
-h, --help                    Show this help message and exit
-i INPUT, --input INPUT       Input file
-o OUTPUT, --output OUTPUT    Output file
-v VIBE, --vibe VIBE          Vibe to apply
-r, --remove-raw              Remove input file
```

## Examples

### From a file
```
python audio-vibes.py -i input.wav -v bathroom_at_club
```

### From a youtube video
```
python audio-vibes.py -i https://www.youtube.com/watch?v=dQw4w9WgXcQ -v bathroom_at_party
```


```
python audio-vibes.py -i https://www.youtube.com/watch?v=QH2-TGUlwu4 -v bathroom_at_club -r -o output.mp3
```

