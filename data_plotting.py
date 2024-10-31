import matplotlib.pyplot as plt
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filemode='w', filename='py.log',
                    format='%(asctime)s | %(levelname)s | %(message)s')


def create_and_save_plot(data, ticker, period, style, filename=None):
    """

    :param data: Принимает на вход DataFraim c информацией об акции
    :param ticker: название акции
    :param period: временной период за который запрашиваются данные
    :param style: стиль оформление графика
    :param filename: название файла
    :return:
    """
    plt.style.use(style)
    plt.figure(figsize=(10, 6))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()
    plt.tight_layout()
    if filename is None:
        filename = f"{ticker}_{period}_{style}_stock_price_chart.png"
    plt.savefig(filename)
    logging.info(f"График сохранен как {filename}")

    # График RSI
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['RSI'], label='RSI', color='blue')
    plt.axhline(70, linestyle='--', alpha=0.5, color='red')
    plt.axhline(30, linestyle='--', alpha=0.5, color='green')
    plt.title(f"RSI для {ticker}")
    plt.xlabel("Дата")
    plt.ylabel("RSI")
    plt.legend()
    plt.savefig(f"{ticker}_{period}_{style}_RSI_chart.png")
    logging.info(f"График RSI сохранен как {ticker}_{period}_RSI_chart.png")

    # График MACD
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['MACD'], label='MACD', color='blue')
    plt.plot(data.index, data['Signal'], label='Signal Line', color='orange')
    plt.title(f"MACD для {ticker}")
    plt.xlabel("Дата")
    plt.ylabel("MACD")
    plt.legend()
    plt.savefig(f"{ticker}_{period}_{style}_MACD_chart.png")
    logging.info(f"График MACD сохранен как {ticker}_{period}_MACD_chart.png")

    # График стандартного отклонения цены закрытия
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['Close'], label='Close Price')
    plt.fill_between(data.index,
                     data['Close'] - data['Std_Dev'],
                     data['Close'] + data['Std_Dev'],
                     color='gray', alpha=0.3, label='Std Dev')
    plt.title(f"Стандартное отклонение для {ticker}")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()
    plt.savefig(f"{ticker}_{period}_{style}_std_dev_chart.png")
    logging.info(f"График стандартного отклонения сохранен как {ticker}_{period}_std_dev_chart.png")


def export_data_to_csv(data, filename):
    """

    :param data: Принимает на вход DataFraim
    :param filename: имя для записи файла
    :return: Создает csv файл с БД, созданной в результате работы программы
    """
    logging.info(f"Таблица сохраена как {filename}.csv")
    return data.to_csv(f'{filename}.csv')
