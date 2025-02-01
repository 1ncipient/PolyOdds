def polymarket_to_american(probability):
    if not 0 < probability < 1:
        raise ValueError("Probability must be between 0 and 1")
    if probability >= 0.5:
        american_odds = -100 * (probability / (1 - probability))
    else:
        american_odds = 100 * ((1 - probability) / probability)
    return int(round(american_odds))

def calculate_hedge_bet(total_payout, hedge_odds):
    if hedge_odds > 0:
        hedge_amount = total_payout / (1 + hedge_odds / 100)
    else:
        hedge_amount = total_payout / (1 + 100 / abs(hedge_odds))
    
    if hedge_odds > 0:
        hedge_profit = (hedge_amount * hedge_odds) / 100
    else:
        hedge_profit = (hedge_amount * 100) / abs(hedge_odds)
    
    return hedge_amount, hedge_profit

def calculate_positions(shares, probabilities, hedge_odds):
    total_cost = 0
    total_shares = sum(shares)
    total_payout = sum(shares)  # Each share pays $1 if event occurs
    
    print("\nPolymarket Positions:")
    for i in range(len(shares)):
        cost = shares[i] * probabilities[i]
        total_cost += cost
        print(f"Position {i+1}: {shares[i]} shares @ {probabilities[i]:.3f} = ${cost:.2f}")
    
    weighted_prob = sum(shares[i] * probabilities[i] for i in range(len(shares))) / total_shares
    combined_american = polymarket_to_american(weighted_prob)
    
    print(f"\nCost: ${total_cost:.2f}")
    print(f"Payout: ${total_payout:.2f}")
    print(f"Combined Probability: {weighted_prob:.3f}")
    print(f"Combined American Odds: {combined_american:+d}")
    
    hedge_amount, hedge_profit = calculate_hedge_bet(total_payout, hedge_odds)
    
    print(f"\nHedge (for {hedge_odds:+d}):")
    print(f"Hedge Amount: ${hedge_amount:.2f}")
    print(f"If Polymarket wins: ${(total_payout - total_cost) - hedge_amount:.2f}")
    print(f"If Hedge wins: ${hedge_profit - total_cost:.2f}")

# Test Case
shares = [18, 300]
probabilities = [0.34, 0.35]
hedge_odds = -110

calculate_positions(shares, probabilities, hedge_odds)