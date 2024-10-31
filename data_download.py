import yfinance as yf
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, filemode='w', filename='py.log',
                    format='%(asctime)s | %(levelname)s | %(message)s')


def fetch_stock_data(ticker, period=None, start_date=None, end_date=None):
    """

    :param ticker: тикер акции
    :param period: временной период (1d, 2d, 5d...)
    :param start_date: пользвательсакя дата начала времненого периода в формате YYYY-MM-DD
    :param end_date: пользвательсакя дата конца времненого периода в формате YYYY-MM-DD
    :return:
    """
    stock = yf.Ticker(ticker)

    if period:  # Если задан период
        data = stock.history(period=period)
    elif start_date and end_date:  # Если заданы начальная и конечная даты
        data = stock.history(start=start_date, end=end_date)
    else:
        raise ValueError("Необходимо указать либо период, либо начальную и конечную даты.")

    return data


def add_moving_average(data, window_size=5):
    """

    :param data: pd.DataFraim
    :param window_size: количество дней, за которые будет рассчитано среднее значение.
    :return:
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    """
    :param data: Принимает БД с данными по запрошенной акции
    :return: Возвращает среднее значение колонки 'Close'
    """
    avg = data['Close'].mean(axis=0)
    logging.info(f'средняя цена закрытия акций: {avg}')
    return avg


def notify_if_strong_fluctuations(data, threshold=20):
    """

    :param threshold:
    :param data: Принимает БД с данными по запрошенной акции :param threshold: Принимает пороговое значение колебаний
    в процентах от средней цены цены закрытия за указанный период :return: Возвращает предупреждение,
    если цена закрытия акций за заданный перуд изменяется больше значения threshold
    """
    min_price = data['Close'].min()
    max_price = data['Close'].max()

    dif = max_price - min_price
    percent = dif / (calculate_and_display_average_price(data) / 100)
    if percent >= threshold:
        logging.warning('высокий уровень колебания акций!')
        return 'Компания не стабильна, будьте внимательны!'


def calculate_rsi(data, window=14):
    """
    Рассчитывает индекс относительной силы (RSI) для данных о ценах акций.

    :param data: DataFrame с историческими данными о ценах акций
    :param window: Период расчета RSI
    :return: DataFrame с добавленным столбцом 'RSI'
    """
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Рассчитывает Moving Average Convergence Divergence (MACD) для данных о ценах акций.

    :param data: DataFrame с историческими данными о ценах акций
    :param short_window: Период для короткой экспоненциальной скользящей средней (EMA)
    :param long_window: Период для длинной экспоненциальной скользящей средней (EMA)
    :param signal_window: Период для сигнальной линии MACD
    :return: DataFrame с добавленными столбцами 'MACD' и 'Signal'
    """
    data['EMA_short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_long'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA_short'] - data['EMA_long']
    data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data


def calculate_and_display_std_dev(data):
    """
    Рассчитывает стандартное отклонение цен закрытия и добавляет его в DataFrame.

    :param data: DataFrame с историческими данными о ценах акций
    :return: DataFrame с добавленным столбцом 'Std_Dev'
    """
    std_dev = data['Close'].std()
    data['Std_Dev'] = std_dev
    logging.info(f'Стандартное отклонение цен закрытия акций: {std_dev}')
    return data
