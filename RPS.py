# Defines the main function 'player' which is called every round
def player(prev_play, opponent_history=[]):
    def beats(move):
        return {'R': 'P', 'P': 'S', 'S': 'R'}[move]

    if prev_play:
        opponent_history.append(prev_play)

    if not hasattr(player, 'my_moves'):
        player.my_moves = []

    history_len = len(opponent_history)

    if history_len == 0:
        move_to_play = 'R'
        player.my_moves.append(move_to_play)
        return move_to_play

    # Quincy cycle detection and prediction
    quincy_cycle = ["R", "R", "P", "P", "S"]

    def detect_quincy_offset():
        if history_len < 5:
            return None
        for offset in range(5):
            matched = True
            for i in range(min(history_len, 10)):
                if opponent_history[history_len - 1 - i] != quincy_cycle[(offset + history_len - 1 - i) % 5]:
                    matched = False
                    break
            if matched:
                return offset
        return None

    offset = detect_quincy_offset()

    def is_kris():
        if history_len < 3 or len(player.my_moves) < history_len:
            return False
        for i in range(1, history_len):
            if opponent_history[i] != beats(player.my_moves[i - 1]):
                return False
        return True

    def is_mrugesh():
        if history_len < 10 or len(player.my_moves) < 10:
            return False
        from collections import Counter
        my_last_10 = player.my_moves[-10:]
        freq = Counter(my_last_10)
        most_common = freq.most_common(1)[0][0]
        count = sum(1 for m in opponent_history[-10:] if m == beats(most_common))
        return count >= 6

    def abbey_counter():
        if len(player.my_moves) < 2:
            import random
            return random.choice(['R', 'P', 'S'])
        last_two_my = "".join(player.my_moves[-2:])
        pair_counts = {}
        for i in range(len(player.my_moves) - 2):
            pair = "".join(player.my_moves[i:i + 2])
            next_move_my = player.my_moves[i + 2]
            if pair not in pair_counts:
                pair_counts[pair] = {'R': 0, 'P': 0, 'S': 0}
            pair_counts[pair][next_move_my] += 1
        if last_two_my in pair_counts:
            predicted_my_next = max(pair_counts[last_two_my], key=pair_counts[last_two_my].get)
            abbey_expected_move = beats(predicted_my_next)
            return beats(abbey_expected_move)
        else:
            import random
            return random.choice(['R', 'P', 'S'])

    if offset is not None:
        predicted_next = quincy_cycle[(offset + history_len) % 5]
        move_to_play = beats(predicted_next)
    elif is_kris():
        last_my_move = player.my_moves[-1]
        predicted_kris_move = beats(last_my_move)
        move_to_play = beats(predicted_kris_move)
    elif is_mrugesh():
        from collections import Counter
        my_last_10 = player.my_moves[-10:]
        freq = Counter(my_last_10)
        most_common = freq.most_common(1)[0][0]
        expected_mrugesh_move = beats(most_common)
        move_to_play = beats(expected_mrugesh_move)
    else:
        move_to_play = abbey_counter()

    player.my_moves.append(move_to_play)
    return move_to_play
