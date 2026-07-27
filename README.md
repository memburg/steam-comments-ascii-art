# steam-comments-ascii-art

ASCII art generator for Steam comments using Braille characters. Converts images to 25×13 character grids that fit Steam's comment limits.

## Requirements

- [JRuby](https://www.jruby.org/) — bundles a Java runtime, no other dependencies

## Install

```bash
brew install jruby          # macOS
# or download from https://www.jruby.org/download
```

## Usage

```bash
jruby generator.rb <image> [--t threshold]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--t` | `100` | Threshold (0–255). Lower = darker, higher = lighter |

## Examples

```bash
jruby generator.rb samples/lenna.png --t 130
jruby generator.rb samples/naruto.png --t 110
jruby generator.rb samples/mr-incredible.png --t 128
```

### Lenna (`--t 130`)

```
⣿⣿⡇⢀⢀⡈⣻⣿⣿⡿⡟⢿⣿⣟⣟⢀⢹⣿⣿⣿⣿⣆⢀⡱⢂
⡟⣿⡇⢀⢀⢀⡒⡛⢩⣶⣾⣶⣾⣍⡀⢀⢸⣿⢿⣿⣿⣿⢆⢀⢀
⢀⣿⡇⢀⢀⢀⡀⢀⣰⣾⢿⣿⣿⣿⣿⣤⢸⣿⡈⢻⡿⢃⢀⢀⣴
⢀⣿⡇⢀⢀⢠⡀⢀⣥⢗⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⡟⢀⢀⣾⣿
⢀⣿⡇⢀⢀⢸⣿⢘⢷⣽⢋⢝⡙⣛⣿⣿⣿⣿⢟⡫⢁⢀⣾⣿⣿
⢀⣿⡇⢀⢀⢀⡟⣱⢑⢁⢀⢀⣨⣿⣿⣿⣷⢐⡉⢀⢀⣾⣿⣿⣿
⢀⣿⡇⢀⢀⣴⡙⢁⢀⢀⢀⡿⡛⣋⢽⡿⢋⢀⡇⢀⣼⣿⣿⣿⣿
⢀⣿⡇⢀⡚⢄⢀⢀⡄⣐⢏⣸⣿⣿⡞⣿⣷⢀⢃⢠⣿⣿⣿⣻⣿
⢀⣿⡇⣁⢀⢑⢂⣀⢄⢃⢀⢸⣿⢿⢿⢿⢇⢀⢘⣾⣿⣿⣿⣿⣿
⢀⣿⡿⢀⢁⢀⡷⡓⢀⢀⢀⢀⢻⣷⣿⡏⢀⢀⢸⢿⣿⣿⢹⣿⡿
⡆⣼⣷⢀⢀⡈⢀⢮⢀⢀⢀⢀⣾⣿⣿⣿⣷⣄⢸⣿⣦⢴⣾⢏⢀
⣷⢸⣿⢀⢀⢀⢀⡈⢅⢀⢀⢢⣿⣿⣿⣿⣿⣿⡜⢿⢷⣾⡟⢀⢀
⢻⢸⡇⢀⢀⢀⢀⢁⢀⢀⢀⣽⣿⣿⣿⣿⣿⣿⣧⢀⢀⢋⢀⢀⢀
```

### Naruto (`--t 110`)

```
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⡟⡛⣛⣩⣻⣭⣭⣭⣭⣭⣉⣋⡉⡛⢻⢿⣿⣿⣿⣿
⣿⡿⢋⢁⢰⣮⣿⣿⣿⣿⣿⣫⣲⡺⣿⣿⣿⣿⣿⣶⡀⡙⢿⣿⣿
⡟⢀⢀⢀⣏⣿⣿⣿⣿⣿⣛⣙⣖⣣⣿⣿⣿⣿⣿⣟⡇⢀⢀⡙⣷
⡇⢀⢀⢀⡘⡘⡛⢛⣉⣉⣉⣉⣉⣩⣝⣋⣙⣛⡛⢹⢀⢀⢀⢀⣽
⡿⣄⣠⣴⣶⣿⣿⣿⣿⣯⣿⣿⣿⣿⣻⣾⣿⡿⣿⣿⣷⣶⢄⣜⣿
⣿⡿⣽⣿⣷⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿
⡿⣽⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿
⣿⣿⣿⣻⣿⣽⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣭⣷⣿
⣿⣿⣿⣭⢿⣿⣿⢿⣽⣿⣿⣟⣿⣟⣿⣿⣿⢿⣿⣿⣿⣾⣿⣿⣿
⣟⣿⣿⢟⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣟⣿⣸⣾⡿⣟⣿⣿⣿⣿⣿⣿⣿⣿⢿⣯⣞⢿⢻⡏⣿⣿⣿
⣿⣿⣟⣯⣿⣿⣻⣭⢿⣿⣿⣿⣿⣿⣽⣾⣿⣷⣿⣿⣯⣿⣽⣿⣷
```

### Mr. Incredible (`--t 128`)

```
⣿⣿⣿⣿⣿⣇⢀⢀⢀⣀⡄⢀⢀⢀⢀⡙⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢆⢀⢀⢀⢀⢀⡙⡛⢻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣦⢷⢄⢀⢀⢀⢀⢀⢀⢻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⡟⡉⢀⢀⢋⢁⢀⢀⢀⢀⢀⢀⢀⢀⣸⣿⣿⣿⣿⣿
⣿⣿⣿⡟⢁⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢿⣿⣿⣿⣿⣿
⡏⣙⡿⣿⡄⡀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⡈⢿⣿⣿⣿⣿
⣿⣮⣽⣿⡿⡟⢃⢀⢀⢀⢀⣸⡀⢀⢀⢀⢀⢀⢀⢀⢀⢀⡉⡙⡛
⣿⡿⣩⣿⣿⡃⢀⢀⢀⢀⣠⡌⢁⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀
⢋⢸⣿⣿⣿⣧⡀⣀⣠⣶⣤⣤⣤⡤⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀
⢀⢀⢻⣿⣿⣿⣿⣿⣿⣿⣟⡅⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀
⢀⢀⢀⢻⢿⣿⣿⣿⣿⣿⣿⢆⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀
⢀⢀⢀⢀⡈⡉⢻⣿⣿⣿⡟⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀
⢀⢀⢀⢀⢀⢀⢀⢀⡉⡉⢁⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀
```

## References

- [Braille patterns (Unicode)](https://en.wikipedia.org/wiki/Braille_Patterns)
- [Image thresholding](https://en.wikipedia.org/wiki/Thresholding_(image_processing))
