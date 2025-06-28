def calculate_position_size(balance, risk_percent, stop_loss_percent):
    risk_amount = balance * (risk_percent / 100)
    position_size = risk_amount / stop_loss_percent
    return position_size
