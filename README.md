# wordle_bot
A bot to play wordle

# Quick Start

1. Checkout and install requirements
```
    git clone https://github.com/jsearcy1/wordle_bot.git 
    pip install -r requirements.txt 
```

2. In your package directory
```
python wordle_bot.py
```
3. Usage
```
usage: wordle_bot.py [-h] [--show] [--minmax] [--start START]
Wordle Bot by jsearcy1 (with auto mode by davidmm377.)

optional arguments:
  -h, --help     show this help message and exit
  --show         opens world in the browser for you to watch it play!
  --minmax       manual interactive mode by jsearcy1
  --start START  starting word (default: arise)
```
4. Enter the the results from website as a 5 character string 
   * x if the character is grey
   * y if the character is yellow
   * g if the character is green
5. Repeat - As you get close to the end the program will print the possible answers left
### Example Game 
```
>> py .\wordle_bot.py --start sadly --show
sadly yxxxx
rouse xyxgg
['chose', 'obese', 'those', 'whose']
aceta xxyyx
['those']
those ggggg
4/6
```
