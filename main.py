from datetime import datetime

import data_download as dd
import data_plotting as dplt


def main():
    global stock_data, period, start_date, end_date
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet "
        "Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")

    preset_periods = {
        '1d': '1 день',
        '5d': '5 дней',
        '1mo': '1 месяц',
        '3mo': '3 месяца',
        '6mo': '6 месяцев',
        '1y': '1 год',
        '2y': '2 года',
        '5y': '5 лет',
        '10y': '10 лет',
        'ytd': 'С начала года',
        'max': 'Максимальный период'}
    style_dict = {
        '1': 'Solarize_Light2',
        '2': '_classic_test_patch',
        '3': '_mpl-gallery',
        '4': '_mpl-gallery-nogrid',
        '5': 'bmh',
        '6': 'classic',
        '7': 'dark_background',
        '8': 'fast',
        '9': 'fivethirtyeight',
        '10': 'ggplot',
        '11': 'grayscale',
        '12': 'seaborn-v0_8',
        '13': 'seaborn-v0_8-bright',
        '14': 'seaborn-v0_8-colorblind',
        '15': 'seaborn-v0_8-dark',
        '16': 'seaborn-v0_8-dark-palette',
        '17': 'seaborn-v0_8-darkgrid',
        '18': 'seaborn-v0_8-deep',
        '19': 'seaborn-v0_8-muted',
        '20': 'seaborn-v0_8-notebook',
        '21': 'seaborn-v0_8-paper',
        '22': 'seaborn-v0_8-pastel',
        '23': 'seaborn-v0_8-poster',
        '24': 'seaborn-v0_8-talk',
        '25': 'seaborn-v0_8-ticks',
        '26': 'seaborn-v0_8-white',
        '27': 'seaborn-v0_8-whitegrid',
        '28': 'tableau-colorblind10'
    }

    while True:
        ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
        choice = input(
            "Вы хотите (1) использовать предустановленные промежутки времени или (2) ввести свои даты? (введите 1 или "
            "2): ")
        if choice == '1':
            print("Выберите период:")
            for key, value in preset_periods.items():
                print(f"{key}: {value}")
            period = input("Введите выбранный период: ")

            # Проверка корректности выбранного периода
            if period not in preset_periods:
                print("Ошибка: неверный выбор периода.")
                continue
            stock_data = dd.fetch_stock_data(ticker, period)
        elif choice == '2':
            start_date = input("Введите дату начала интересующего вас периода в формате YYYY-MM-DD")
            end_date = input("Введите дату конца интересующего вас периода в формате YYYY-MM-DD")
            # Проверка корректности введенных дат
            try:
                start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
                if start_date_dt >= end_date_dt:
                    print("Ошибка: начальная дата должна быть раньше конечной даты.")
                    continue
            except ValueError:
                print("Ошибка: неверный формат даты. Пожалуйста, используйте формат YYYY-MM-DD.")
                continue
            stock_data = dd.fetch_stock_data(ticker, start_date, end_date)
            # Проверка наличия данных о акции
        if stock_data.empty:
            print(
                f"Нет данных для тикера '{ticker}'. Пожалуйста, проверьте правильность введенного тикера и "
                f"запрашиваемого перода времени")
            continue  # Возврат к началу цикла для повторного ввода
        threshold = int(input(
            'Введите порог колебания акций относительно средней цены закрытия в процентах (по умолчанию 20%) ').strip() or '20')

        # Добавление скользящего среднего, RSI, MACD и стандартного отклонения цены закрытия
        stock_data = dd.add_moving_average(stock_data)  # Добавляем расчет Скользящего среднего
        stock_data = dd.calculate_rsi(stock_data)  # Добавляем расчет RSI
        stock_data = dd.calculate_macd(stock_data)  # Добавляем расчет MACD
        stock_data = dd.calculate_and_display_std_dev(
            stock_data)  # Добавляем рассчет стандартного отклонения цены закрытия
        print(stock_data)
        for key, value in style_dict.items():
            print(f"{key}: {value}")
        num_of_style = input("Введите номер выбранного стиля для графика: ")

        # Отрисовка графика и сохранение БД в csv-файл
        if choice == '1':
            dplt.create_and_save_plot(stock_data, ticker, period, style_dict[num_of_style])
            dplt.export_data_to_csv(stock_data, f'{ticker}_{period}')
        else:
            dplt.create_and_save_plot(stock_data, ticker, f"{start_date} to {end_date}")
            dplt.export_data_to_csv(stock_data, f'{ticker}_{start_date}_{end_date}')

        print(dd.calculate_and_display_average_price(stock_data))

        # Расчет процента колебаний
        if dd.notify_if_strong_fluctuations(stock_data, threshold) is not None:
            print(dd.notify_if_strong_fluctuations(stock_data, threshold))

        break  # Выход из цикла, если данные успешно получены


if __name__ == "__main__":
    main()
