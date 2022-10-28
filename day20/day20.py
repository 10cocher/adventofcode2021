if __name__ == "__main__":
    if True:
        pos1 = 2 - 1
        pos2 = 7 - 1
    else:
        pos1 = 4 - 1
        pos2 = 8 - 1
    #
    die_rolled = 0
    score1 = 0
    score2 = 0
    #
    die_value = 1
    turns = 1
    while (score1 < 1000) and (score2 < 1000):
        print(f"==== turn {turns} ====")
        die_total = 3 * die_value + 3
        die_value += 3
        die_rolled += 3
        pos1 += die_total
        pos1 = pos1 % 10
        score1 += pos1 + 1
        if score1 >= 1000:
            res = score2 * die_rolled
            print(f"player 1 won, score2={score2}, die_rolled={die_rolled}, res={res}")
            break
        #
        die_total = 3 * die_value + 3
        die_value += 3
        die_rolled += 3
        pos2 += die_total
        pos2 = pos2 % 10
        score2 += pos2 + 1
        if score2 >= 1000:
            res = score1 * die_rolled
            print(f"player 2 won, score1={score1}, die_rolled={die_rolled}, res={res}")
            break
        #print(f"player 1: score = {score1:3} pos = {pos1+1:2}")
        #print(f"player 2: score = {score2:3} pos = {pos2+1:2}")
        turns += 1
