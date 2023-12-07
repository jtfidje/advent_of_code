from collections import Counter, OrderedDict

from pathlib import Path

from solver import utils

data_path = Path(__file__).parent.parent.absolute() / "data"


def calc_score(count, multiplier):
    return sum(map(lambda x: x[0] * (x[1] * multiplier), count))


def rank_hand(hand):
    hand = ",".join(list(hand))
    hand = hand.replace("T", "10").replace("J", "11").replace("Q", "12").replace("K", "13").replace("A", "14")
    hand = list(map(int, hand.split(",")))
    
    hand_count = OrderedDict(sorted(Counter(hand).items(), reverse=True))
    count = list(OrderedDict(sorted(hand_count.items(), key=lambda x: x[1], reverse=True)).items())

    # High card
    if len(hand_count) == 5:
        high_card = list(hand_count)[0]
        return calc_score(count, multiplier=0.01)
    
    # Pair
    elif len(hand_count) == 4:
        high_card = count[0][0]
        return calc_score(count, multiplier=0.1)
    
    # Two pairs and three of a kind
    elif len(hand_count) == 3:
        if count[0][1] == 3:
            # Three of a kind
            return calc_score(count, multiplier=10)
        
        # Two pairs
        return calc_score(count, multiplier=1)
    
    # Four of a kind and full house
    elif len(hand_count) == 4:
        if count[0][1] == 4:
            # Four of a kind:
            return calc_score(count, multiplier=1_000)
        
        # Full house
        return calc_score(count, multiplier=100)

    # 5 of a kind
    else:
        return calc_score(count, multiplier=10_000)
    




def solve(path: str):
    data = utils.read_lines(path)
    data = [line.split() for line in data]

    data = sorted(data, key=lambda x: rank_hand(x[0]))

    return sum([i * int(line[1]) for i, line in enumerate(data, start=1)])

if __name__ == "__main__":
    answer = solve(Path(data_path, "input.txt"))
    print(f"Problem 1: {answer}")