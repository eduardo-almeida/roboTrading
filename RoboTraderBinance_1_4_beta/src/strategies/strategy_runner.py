from .moving_average_antecipation import getMovingAverageAntecipationTradeStrategy
from .moving_average import getMovingAverageTradeStrategy
from .ut_bot_alerts import utBotAlerts


def runStrategies(self, stock_data):

    # strategies
    movingAverageAntecipationTrade = getMovingAverageAntecipationTradeStrategy(stock_data, self.volatility_factor)

    # Executa a estratégia de média movel
    maant_trade_decision = movingAverageAntecipationTrade
    final_decision = maant_trade_decision

    if maant_trade_decision == None and self.fallback_activated == True:
        print("Estratégia de MA Antecipation inconclusiva\nExecutando estratégia de fallback...")
        movingAverageTrade = getMovingAverageTradeStrategy(self.stock_data)
        ma_trade_decision = movingAverageTrade
        final_decision = ma_trade_decision

    return final_decision
