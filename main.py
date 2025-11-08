"""Quick example - Set your own stop loss and target prices."""
from src.data_providers import CryptoCompareProvider
from src.position import PositionCalculator
from src.strategies import SimpleStopLossStrategy


def main():
    """Quick example with user-defined price levels."""
    
    # 1. Set your max loss amount
    MAX_LOSS = 300  # Maximum amount you're willing to lose
    
    # 2. Initialize
    data_provider = CryptoCompareProvider()
    calculator = PositionCalculator(max_loss_amount=MAX_LOSS)
    
    crypto = "BTC"
    currency = "USD"

    # 4. Set YOUR stop loss and target prices
    YOUR_STOP_LOSS = 99000.0   # ← Set your stop loss price here
    YOUR_TARGET = 108000.0      # ← Set your target price here
    
    strategy = SimpleStopLossStrategy(
        data_provider=data_provider,
        position_calculator=calculator,
        symbol=crypto,
        currency=currency
    )
    
    # 3. Get current price
    current_price = strategy.get_current_price()
    print(f"Current {crypto} Price: ${current_price:,.2f}\n")
    
    strategy.set_levels(
        stop_loss_price=YOUR_STOP_LOSS,
        target_price=YOUR_TARGET
    )
    
    # 5. Calculate position size automatically
    result = strategy.execute_strategy()
    
    if result:
        entry = result['entry']
        
        print("=" * 50)
        print("TRADE SETUP")
        print("=" * 50)
        print(f"Entry Price:    ${entry['current_price']:,.2f}")
        print(f"Stop Loss:      ${entry['stop_loss']:,.2f}")
        print(f"Target:         ${entry['target_price']:,.2f}")
        print(f"\nPosition Size:  {entry['position_size']:.6f} BTC")
        print(f"Entry Cost:     ${entry['entry_cost']:,.2f}")
        print(f"\nMax Loss:       ${entry['potential_loss']:,.2f}")
        print(f"Potential Gain: ${entry['potential_profit']:,.2f}")
        print(f"Risk/Reward:    1:{entry['risk_reward_ratio']:.2f}")
        print("=" * 50)
    
    # Alternative: Direct calculation without strategy
    print("\n\nDirect Calculation Method:")
    print("-" * 50)
    
    position = calculator.calculate_position_size(
        current_price=current_price,
        stop_loss=YOUR_STOP_LOSS,
        target_price=YOUR_TARGET
    )
    
    print(f"Position Size: {position['position_size']:.6f} BTC")
    print(f"Max Loss: ${position['potential_loss']:,.2f}")
    print(f"Potential Profit: ${position['potential_profit']:,.2f}")


if __name__ == "__main__":
    main()
