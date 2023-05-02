import pydealer as pd
import random

wiz = pd.card.Card("Wizard", "Wizard")
jester = pd.card.Card("Jester", "Jester")

new_ranks = {
    "values": {
        "Wizard": 14,
        "Ace": 13,
        "King": 12,
        "Queen": 11,
        "Jack": 10,
        "10": 9,
        "9": 8,
        "8": 7,
        "7": 6,
        "6": 5,
        "5": 4,
        "4": 3,
        "3": 2,
        "2": 1,
        "Jester": 0
    },
    "suits": {
        "Wizard": 3,
        "Spades": 2,
        "Hearts": 1,
        "Clubs": 1,
        "Diamonds": 1,
        "Jester": 0
    }
}

def compare(a,b, ranks):
    if a.suit == b.suit and a.value == b.value:
        return True
    else:
        if ranks["suits"][a.suit] > ranks["suits"][b.suit]:
            return True
        elif ranks["suits"][a.suit] == ranks["suits"][b.suit]:
            return ranks["values"][a.value] >= ranks["values"][b.value]
        else:
            return False

def run_two_sim(num_players):
    new_ranks = {
    "values": {
        "Wizard": 14,
        "Ace": 13,
        "King": 12,
        "Queen": 11,
        "Jack": 10,
        "10": 9,
        "9": 8,
        "8": 7,
        "7": 6,
        "6": 5,
        "5": 4,
        "4": 3,
        "3": 2,
        "2": 1,
        "Jester": 0
    },
    "suits": {
        "Wizard": 4,
        "Spades": 2.5,
        "Hearts": 1,
        "Clubs": 1,
        "Diamonds": 1,
        "Jester": 0
    }
}
    d = pd.Deck()
    for i in range(4):
        d.add(wiz)
        d.add(jester)
    lead_rounds_appeared = {}
    second_rounds_appeared = {}
    lead_tricks_won = {}
    second_tricks_won = {}
    total_rounds_appeared = {}
    total_tricks_won = {}
    for card in d:
        lead_rounds_appeared[card] = 0
        second_rounds_appeared[card] = 0
        lead_tricks_won[card] = 0
        second_tricks_won[card] = 0
        total_rounds_appeared[card] = 0
        total_tricks_won[card] = 0
    for i in range(20000): 
        hands = []
        ranks = new_ranks
        d = pd.Deck()
        for i in range(4):
            d.add(wiz)
            d.add(jester)
        d.shuffle()
        for i in range(num_players):
            hands.append(pd.Stack())
            cards = d.deal(1)
            total_rounds_appeared[cards[0]] += 1
            if i == 0:
                lead_rounds_appeared[cards[0]] += 1
            else:
                second_rounds_appeared[cards[0]] += 1
            hands[i].add(cards)
    #for simplification, let Spades be trump

# Now time to play the tricks
        lead_suit = hands[0][0].suit
        ranks["suits"][lead_suit] += 1
        if (compare(hands[0][0], hands[1][0], ranks)):
            lead_tricks_won[hands[0][0]] += 1
            total_tricks_won[hands[0][0]] += 1
        else:
            second_tricks_won[hands[1][0]] += 1
            total_tricks_won[hands[1][0]] += 1
        ranks["suits"][lead_suit] -= 1

    lead_avg_tricks_won = {}
    second_avg_tricks_won = {}
    total_avg_tricks_won = {}
    # Avg tricks won by first card
    for card in lead_rounds_appeared:
        if lead_rounds_appeared[card] != 0:
            lead_avg_tricks_won[card] = lead_tricks_won[card] / lead_rounds_appeared[card]
        else:
            lead_avg_tricks_won[card] = 0
    # Can sort into list if necessary
    #sorted_lead_avg_tricks_won = sorted(lead_avg_tricks_won.items(), key=lambda x:x[1], reverse=True)

    # Avg tricks won by second card
    for card in second_rounds_appeared:
        if second_rounds_appeared[card] != 0:
            second_avg_tricks_won[card] = second_tricks_won[card] / second_rounds_appeared[card]
        else:
            second_avg_tricks_won[card] = 0
    # Can sort into list if necessary
    #sorted_second_avg_tricks_won = sorted(second_avg_tricks_won.items(), key=lambda x:x[1], reverse=True)

    # Avg tricks won by cards without considering placement
    for card in total_rounds_appeared:
        if total_rounds_appeared[card] != 0:
            total_avg_tricks_won[card] = total_tricks_won[card] / total_rounds_appeared[card]
        else:
            total_avg_tricks_won[card] = 0
    # Can sort into list if necessary
    #sorted_total_avg_tricks_won = sorted(total_avg_tricks_won.items(), key=lambda x:x[1], reverse=True)

    return [lead_avg_tricks_won, second_avg_tricks_won, total_avg_tricks_won]
    
def available_cards(cards_in_trick, hand):
    if len(cards_in_trick) == 0:
        return hand
    available = pd.Stack()
    for card in hand:
        if card.suit == "Wizard" or card.suit == "Jester":
            available.add(card)
        if card.suit == cards_in_trick[0].suit:
            available.add(card)
    if (len(available) == 0):
        return hand
    else:
        return available

def random_choice(hand):
    #print(hand)
    return hand[0], str(hand[0])

def best_play_two(hand, tricks_remaining, position_in_round, tricks_dict, trick_cards):
    #print(hand)
    if (len(hand) == 1):
        return hand[0], str(hand[0])
    expected_tricks_won = 0
    min_val = 100
    best_card = hand[0]
    #print("new hand")
    for card in hand:
        if isinstance(card, list):
            card = card[0]
        expected_tricks_won += tricks_dict[card]
    for card in hand:
        prob_winning = 0
        if isinstance(card, list):
            card = card[0]
        if position_in_round == 0:
            if card.suit == "Wizard":
                prob_winning = 1
            elif card.suit == "Spades":
                card_num = new_ranks["values"][card.value]
                prob_winning = 1 - ((17 - card_num)/59)
            else:
                card_num = new_ranks["values"][card.value]
                prob_winning = (30 + card_num - 1)/59
        else:
            if not compare(trick_cards[0], card, new_ranks):
                prob_winning = 1
        win_diff = abs(expected_tricks_won - tricks_dict[card] - (tricks_remaining - prob_winning))
        if win_diff <= min_val:
            min_val = win_diff
            best_card = card
        return best_card, str(best_card)

def two_game(num_players, num_cards):
    card_dict = run_two_sim(num_players)
    total_card_dict = card_dict[-1]
    #first_card_dict = card_dict[0]
    #second_card_dict = card_dict[1]
    hands = []
    for i in range(num_players):
        hands.append(pd.Stack())
    deck = pd.Deck()
    for i in range(4):
        deck.add(wiz)
        deck.add(jester)
    deck.shuffle()
    # Deal out the hands and settle bids
    bids = []
    for i in range(num_players):
        cards = deck.deal(num_cards)
        #print("Dealing Hand #" + str(i))
        hands[i].add(cards)
        hand_bid = 0
        if i == 1:
            for card in cards:
                hand_bid += total_card_dict[card]
        else:
            hand_bid = random.randint(0, num_cards)
        bids.append(round(hand_bid))
        # for j in range(num_cards):
        #     print(hands[i][j])
        #     print(total_card_dict[hands[i][j]])
    tricks_left = []
    for bid in bids:
        tricks_left.append(bid)
    tricks_won = [0,0]
    # Play the rounds
    lead_player = 0
    # Loop through each trick
    for i in range(num_cards):
        # Loop through each player, starting with first player
        trick_winner = lead_player # 0 or 1
        cards_in_trick = []
        for j in range(num_players):
            player = (trick_winner + j) % num_players
            if player == 1:
                card_choices = available_cards(cards_in_trick, hands[player])
                choice = best_play_two(card_choices, tricks_left[player], j, total_card_dict, cards_in_trick)
                cards_in_trick.append(choice[0])
                hands[player], _ = pd.tools.get_card(hands[player], choice[1], limit=1, sort=False)
            else:
                card_choices = available_cards(cards_in_trick, hands[player])
                choice = random_choice(card_choices)
                cards_in_trick.append(choice[0])
                hands[player], _ = pd.tools.get_card(hands[player], choice[1], limit=1, sort=False)
        if compare(cards_in_trick[lead_player], cards_in_trick[1-lead_player], new_ranks):
            lead_player = lead_player
            tricks_won[lead_player] += 1
            tricks_left[lead_player] -= 1
        else:
            lead_player = 1 - lead_player
            tricks_won[lead_player] += 1
            tricks_left[lead_player] -= 1
    scores = []
    #print(bids)
    #print(tricks_won)
    for i in range(2):
        if tricks_won[i] == bids[i]:
            scores.append(20 + 10 * bids[i])
        else:
            scores.append(-10*(abs(tricks_won[i] - bids[i])))
    return scores
        

if __name__ == '__main__':
    total_scores = [0, 0]
    num_trials = 10
    cards_in_round = 8
    for i in range(num_trials):
        game_score = two_game(2, cards_in_round)
        total_scores[0] += game_score[0]
        total_scores[1] += game_score[1]
    avg_scores = []
    for val in total_scores:
        avg_scores.append(val / num_trials)
    print(avg_scores)
    