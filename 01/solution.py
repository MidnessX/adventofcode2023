import re

DIGITS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}
matcher = re.compile(r"zero|one|two|three|four|five|six|seven|eight|nine")

def parse_line(line:str) -> str:
    parsed_line =  matcher.sub(lambda x: str(DIGITS[x.group()]), line)

    return parsed_line

with open("01/input.txt") as cv:
    val_sum = 0

    for line in cv.readlines():
        parsed_line = parse_line(line)

        i = 0
        j = len(line) - 1

        fd = -1
        ld = -1
        
        while fd == -1 or ld == -1:
            if fd == -1 and line[i].isdigit():
                fd = line[i]
            if ld == -1 and line[j].isdigit():
                ld = line[j]

            i += 1
            j -= 1

        val = int(f"{fd}{ld}")
        val_sum += val
    
    print(val_sum)