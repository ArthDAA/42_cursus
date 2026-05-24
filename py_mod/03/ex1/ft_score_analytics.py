import sys

if __name__ == "__main__":
    print("=== Player Score Analytics ===")
    scores = []
    i = 1
    while (i < len(sys.argv)):
        try:
            scores.append(int(sys.argv[i]))
            i += 1
        except ValueError:
            print(f"Invalid Parameter: '{sys.argv[i]}'")
            i += 1
    if (len(scores) > 0):
        print(f"Scores processed: {scores}\n"
              f"Total players: {len(scores)}\n"
              f"Total score: {sum(scores)}\n"
              f"Average score: {sum(scores) / len(scores)}\n"
              f"High score: {max(scores)}\n"
              f"Low scores: {min(scores)}\n"
              f"Score range: {max(scores) - min(scores)}\n"
              )
    else:
        print("No scores provided. Usage: python3 "
              "ft_score_analytics.py <score1> <score2> ...")
