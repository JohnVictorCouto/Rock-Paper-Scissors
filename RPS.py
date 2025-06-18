# Defines the main function 'player' which is called every round
def player(prev_play, opponent_history=[]):
    
    # Helper function that returns the move that beats the given move
    def beats(move):
        return {'R': 'P', 'P': 'S', 'S': 'R'}[move]  # Rock loses to Paper, Paper loses to Scissors, Scissors loses to Rock

    # If there was a previous move from the opponent, add it to the opponent's history
    if prev_play:
        opponent_history.append(prev_play)

    # Initialize player's move history if it doesn't already exist
    if not hasattr(player, 'my_moves'):
        player.my_moves = []

    # Get the current length of opponent's history
    history_len = len(opponent_history)

    # If this is the first round, play 'R' (Rock) by default
    if history_len == 0:
        move_to_play = 'R'                   # Choose Rock
        player.my_moves.append(move_to_play) # Save this move to player's history
        return move_to_play                  # Return the chosen move

    # Define the specific Quincy cycle pattern to detect
    quincy_cycle = ["R", "R", "P", "P", "S"]

    # Function to detect if opponent is following the Quincy cycle with some offset
    def detect_quincy_offset():
        if history_len < 5:
            return None  # Not enough history to detect the cycle yet
        # Check all possible starting offsets in the cycle
        for offset in range(5):
            matched = True
            # Compare up to the last 10 moves
            for i in range(min(history_len, 10)):
                # Check if opponent's move matches the Quincy pattern at this offset
                if opponent_history[history_len - 1 - i] != quincy_cycle[(offset + history_len - 1 - i) % 5]:
                    matched = False
                    break  # If any mismatch, stop checking this offset
            if matched:
                return offset  # If fully matched, return the detected offset
        return None  # No matching offset found

    # Call the cycle detection function
    offset = detect_quincy_offset()

    # Function to detect if opponent is using the Kris strategy
    def is_kris():
        # Requires at least 3 moves of history and enough player moves for comparison
        if history_len < 3 or len(player.my_moves) < history_len:
            return False
        # Check if opponent's moves are always beating the player's previous move
        for i in range(1, history_len):
            if opponent_history[i] != beats(player.my_moves[i - 1]):
                return False  # If any mismatch, it's not Kris
        return True  # If all match, opponent is following Kris

    # Function to detect if opponent is using the Mrugesh strategy
    def is_mrugesh():
        # Requires at least 10 moves in both histories
        if history_len < 10 or len(player.my_moves) < 10:
            return False
        from collections import Counter
        my_last_10 = player.my_moves[-10:]  # Get player's last 10 moves
        freq = Counter(my_last_10)          # Count frequency of player's moves
        most_common = freq.most_common(1)[0][0]  # Get player's most common move
        # Count how many times opponent responded with the counter to this common move
        count = sum(1 for m in opponent_history[-10:] if m == beats(most_common))
        return count >= 6  # If opponent countered at least 6 times, likely Mrugesh

    # Function to choose move against Abbey strategy
    def abbey_counter():
        # If not enough move history, choose randomly
        if len(player.my_moves) < 2:
            import random
            return random.choice(['R', 'P', 'S'])  # Random pick from Rock, Paper, Scissors
        last_two_my = "".join(player.my_moves[-2:])  # Get last two player moves as a string
        pair_counts = {}  # Dictionary to store occurrences of each 2-move sequence and following move
        # Iterate through player's history to count occurrences
        for i in range(len(player.my_moves) - 2):
            pair = "".join(player.my_moves[i:i + 2])   # Get each 2-move sequence
            next_move_my = player.my_moves[i + 2]      # Move that followed this pair
            if pair not in pair_counts:
                pair_counts[pair] = {'R': 0, 'P': 0, 'S': 0}  # Initialize counts
            pair_counts[pair][next_move_my] += 1  # Increment count for that next move
        # If the last two moves exist in our tracking
        if last_two_my in pair_counts:
            # Predict player's next move based on historical data
            predicted_my_next = max(pair_counts[last_two_my], key=pair_counts[last_two_my].get)
            # Abbey will likely counter this predicted move, so we counter Abbey's expected move
            abbey_expected_move = beats(predicted_my_next)
            return beats(abbey_expected_move)  # Play the move that beats Abbey's counter
        else:
            import random
            return random.choice(['R', 'P', 'S'])  # If no history, pick randomly

    # Decision logic to select the strategy based on detected patterns

    # If a Quincy pattern was detected
    if offset is not None:
        predicted_next = quincy_cycle[(offset + history_len) % 5]  # Predict opponent's next move in the cycle
        move_to_play = beats(predicted_next)  # Play the move that beats opponent's predicted move

    # Else, if Kris strategy detected
    elif is_kris():
        last_my_move = player.my_moves[-1]  # Get player's last move
        predicted_kris_move = beats(last_my_move)  # Predict Kris will play the counter to player's last move
        move_to_play = beats(predicted_kris_move)  # So play the move that beats that

    # Else, if Mrugesh strategy detected
    elif is_mrugesh():
        from collections import Counter
        my_last_10 = player.my_moves[-10:]  # Get last 10 player moves
        freq = Counter(my_last_10)          # Count their frequencies
        most_common = freq.most_common(1)[0][0]  # Most common move played
        expected_mrugesh_move = beats(most_common)  # Predict Mrugesh will counter the common move
        move_to_play = beats(expected_mrugesh_move)  # So play the move that beats Mrugesh's expected counter

    # Else, fallback to countering Abbey strategy
    else:
        move_to_play = abbey_counter()  # Use Abbey countering logic

    # Save the chosen move to player's history
    player.my_moves.append(move_to_play)

    # Return the chosen move for this round
    return move_to_play
