import threading
import time
from modules.BinanceRobot import BinanceTraderBot
from binance.client import Client
from Models.StockStartModel import StockStartModel
import logging

# Define o logger
logging.basicConfig(
    filename="src/logs/trading_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# fmt: off
# ------------------------------------------------------------------
# 🟢 CONFIGURAÇÕES - PODEM ALTERAR - INICIO 🟢


# Ajustes Técnicos
VOLATILITY_FACTOR           = 0.5       # Interfere na antecipação e nos lances de compra de venda limitados
FALLBACK_ACTIVATED          = True      # Define se a estratégia de Fallback será usada (ela pode entrar comprada em mercados subindo)


# Ajustes de Loss Protection
ACCEPTABLE_LOSS_PERCENTAGE  = 0.5       # (Usar em base 100%) O quando o bot aceita perder de % (se for negativo, o bot só aceita lucro)
STOP_LOSS_PERCENTAGE        = 3.5       # (Usar em base 100%) % Máxima de loss que ele aceita para vender à mercado independente


# Ajustes de Take Profit
                        # Em [X%, Y%]:
TP_AT_PERCENTAGE =      [2, 5, 10]
                        # Vende [A%, B%]:
TP_AMOUNT_PERCENTAGE =  [50, 50, 100]


# Ajustes de Tempo
CANDLE_PERIOD = Client.KLINE_INTERVAL_1HOUR # Périodo do candle análisado
TEMPO_ENTRE_TRADES          = 30 * 60            # Tempo que o bot espera para verificar o mercado (em segundos)
DELAY_ENTRE_ORDENS          = 60 * 60           # Tempo que o bot espera depois de realizar uma ordem de compra ou venda (ajuda a diminuir trades de borda)

# Ajustes de Execução
THREAD_LOCK = True # True = Executa 1 moeda por vez | False = Executa todas simultânemaente


# Moedas negociadas
XRP_USDT = StockStartModel(  stockCode = "XRP",
                            operationCode = "XRPUSDT",
                            tradedQuantity = 100,
                            candlePeriod = CANDLE_PERIOD, volatilityFactor = VOLATILITY_FACTOR, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ACTIVATED, takeProfitAtPercentage=TP_AT_PERCENTAGE, takeProfitAmountPercentage=TP_AMOUNT_PERCENTAGE)

SOL_USDT = StockStartModel(  stockCode = "SOL",
                            operationCode = "SOLUSDT",
                            tradedQuantity = 2,
                            candlePeriod = CANDLE_PERIOD, volatilityFactor = VOLATILITY_FACTOR, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ACTIVATED, takeProfitAtPercentage=TP_AT_PERCENTAGE, takeProfitAmountPercentage=TP_AMOUNT_PERCENTAGE)

ADA_USDT = StockStartModel(  stockCode = "ADA",
                            operationCode = "ADAUSDT",
                            tradedQuantity = 10,
                            candlePeriod = CANDLE_PERIOD, volatilityFactor = VOLATILITY_FACTOR, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ACTIVATED, takeProfitAtPercentage=TP_AT_PERCENTAGE, takeProfitAmountPercentage=TP_AMOUNT_PERCENTAGE)

BTC_USDT = StockStartModel(  stockCode = "BTC",
                            operationCode = "BTCUSDT",
                            tradedQuantity = 0.01,
                            candlePeriod = CANDLE_PERIOD, volatilityFactor = VOLATILITY_FACTOR, stopLossPercentage = STOP_LOSS_PERCENTAGE, tempoEntreTrades = TEMPO_ENTRE_TRADES, delayEntreOrdens = DELAY_ENTRE_ORDENS, acceptableLossPercentage = ACCEPTABLE_LOSS_PERCENTAGE, fallBackActivated= FALLBACK_ACTIVATED, takeProfitAtPercentage=TP_AT_PERCENTAGE, takeProfitAmountPercentage=TP_AMOUNT_PERCENTAGE)

# Array que DEVE CONTER as moedas que serão negociadas
stocks_traded_list = [SOL_USDT]


# 🔴 CONFIGURAÇÕES - PODEM ALTERAR - FIM 🔴
# ---------------------------------------------------------------------------------------------
# LOOP PRINCIPAL

thread_lock = threading.Lock()

def trader_loop(stockStart: StockStartModel):
    MaTrader = BinanceTraderBot(stock_code = stockStart.stockCode
                                , operation_code = stockStart.operationCode
                                , traded_quantity = stockStart.tradedQuantity
                                , traded_percentage = stockStart.tradedPercentage
                                , candle_period = stockStart.candlePeriod
                                , volatility_factor = stockStart.volatilityFactor
                                , time_to_trade = stockStart.tempoEntreTrades
                                , delay_after_order = stockStart.delayEntreOrdens
                                , acceptable_loss_percentage = stockStart.acceptableLossPercentage
                                , stop_loss_percentage = stockStart.stopLossPercentage
                                , fallback_activated = stockStart.fallBackActivated
                                , take_profit_at_percentage = stockStart.takeProfitAtPercentage
                                , take_profit_amount_percentage= stockStart.takeProfitAmountPercentage)

    total_executed:int = 1

    while(True):
        if(THREAD_LOCK):
            with thread_lock:
                print(f"[{MaTrader.operation_code}][{total_executed}] '{MaTrader.operation_code}'")
                MaTrader.execute()
                print(f"^ [{MaTrader.operation_code}][{total_executed}] time_to_sleep = '{MaTrader.time_to_sleep/60:.2f} min'")
                print(f"------------------------------------------------")
                total_executed += 1
        else:
            print(f"[{MaTrader.operation_code}][{total_executed}] '{MaTrader.operation_code}'")
            MaTrader.execute()
            print(f"^ [{MaTrader.operation_code}][{total_executed}] time_to_sleep = '{MaTrader.time_to_sleep/60:.2f} min'")
            print(f"------------------------------------------------")
            total_executed += 1
        time.sleep(MaTrader.time_to_sleep)


# Criando e iniciando uma thread para cada objeto
threads = []

for asset in stocks_traded_list:
    thread = threading.Thread(target=trader_loop, args=(asset,))
    thread.daemon = True  # Permite finalizar as threads ao encerrar o programa
    thread.start()
    threads.append(thread)

print("Threads iniciadas para todos os ativos.")

# O programa principal continua executando sem bloquear
try:
    while True:
        time.sleep(1)  # Mantenha o programa rodando
except KeyboardInterrupt:
    print("\nPrograma encerrado pelo usuário.")


# fmt: on
