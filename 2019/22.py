from collections import deque
from re import I

# part 1

# if __name__ == "__main__":
#     with open('./input/22.txt') as f:
#         data = f.read().splitlines()

#         #total_cards = 10006
#         total_cards = 119315717514047
#         #card_to_track = 2019
#         card_to_track = 2020
#         #total_cards = 9
#         #card_to_track = 3
#         cards_left = card_to_track
#         cards_right = total_cards - card_to_track

#         for move in data:
#             line = move.split(" ")
#             if move == "deal into new stack":
#                 cards_left, cards_right = cards_right, cards_left
#             elif line[0] == "cut":
#                 n = int(line[1])
#                 if n > 0:
#                     if cards_left >= n:
#                         cards_left -= n
#                         cards_right += n
#                     else:
#                         diff =  n - cards_left - 1
#                         cards_left += cards_right - diff
#                         cards_right = total_cards - cards_left
#                 if n < 0:
#                     n = abs(n)
#                     if cards_right >= n:
#                         cards_left += n
#                         cards_right -= n
#                     else:
#                         diff = n - cards_right - 1
#                         cards_right += cards_left - diff
#                         cards_left = total_cards - cards_right
#             else:
#                 #incr
#                 n = int(line[3])
#                 pos = (n * cards_left) % (total_cards+1)
#                 cards_left = pos
#                 cards_right = total_cards - cards_left
#             print(move, cards_left, cards_right)

#         print(cards_left)

# part 2

if __name__ == "__main__":
    with open('./input/22.txt') as f:
        data = f.read().splitlines()

        #total_cards = 10006
        total_cards = 119315717514047
        #card_to_track = 2019
        card_to_track = 2020
        #total_cards = 9
        #card_to_track = 3
        cards_left = card_to_track
        cards_right = total_cards - card_to_track
        seen = set()
        for i in range(101741582076661):
            if cards_left in seen:
                print(i)
                exit()
            seen.add(cards_left)
            for move in data:
                line = move.split(" ")
                if move == "deal into new stack":
                    cards_left, cards_right = cards_right, cards_left
                elif line[0] == "cut":
                    n = int(line[1])
                    if n > 0:
                        if cards_left >= n:
                            cards_left -= n
                            cards_right += n
                        else:
                            diff =  n - cards_left - 1
                            cards_left += cards_right - diff
                            cards_right = total_cards - cards_left
                    if n < 0:
                        n = abs(n)
                        if cards_right >= n:
                            cards_left += n
                            cards_right -= n
                        else:
                            diff = n - cards_right - 1
                            cards_right += cards_left - diff
                            cards_left = total_cards - cards_right
                else:
                    #incr
                    n = int(line[3])
                    pos = (n * cards_left) % (total_cards+1)
                    cards_left = pos
                    cards_right = total_cards - cards_left
                #print(move, cards_left, cards_right)
            #print(cards_left)
        print(cards_left)
