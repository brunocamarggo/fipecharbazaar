import pandas as pd
import matplotlib.pyplot as plt
import datetime
import zipfile

VOCATIONS = {
    0: 'none',
    1: 'Knight',
    2: 'Paladin',
    3: 'sorcerer',
    4: 'druid'
}


def vocation_name(vocation_id):
    return VOCATIONS[vocation_id]


def auctions_vs_vocations(data_frame):
    data_frame['vocationId'] = data_frame['vocationId'].apply(vocation_name)
    print(f"Percent bidded: {data_frame['hasBeenBidded'].mean() * 100}")

    vocations = data_frame['vocationId'].value_counts()
    vocations.plot(kind='bar', color='skyblue')
    plt.title('Number of auctions vs. vocation')
    plt.xlabel('Vocation')
    plt.xticks(rotation=45)
    plt.ylabel('Number of auctions')
    plt.show()


def tibiacoins_vs_time(data_frame):
    data_frame = data_frame[data_frame['hasBeenBidded'] != False]
    data_frame.set_index('auctionEnd', inplace=True)
    grouped = data_frame.groupby([data_frame.index.year, data_frame.index.month])['currentBid'].sum()
    grouped.plot(kind="bar", color='skyblue')

    plt.title('Tibia Coins vs. time')
    plt.tight_layout()
    plt.xlabel('Time')
    plt.ylabel('Tibia Coins')
    plt.savefig('tibiacoins_vs_time.svg', format='svg')
    plt.show()


def vocations_tibia_coins_vs_time(data_frame):
    data_frame = data_frame[data_frame['hasBeenBidded'] != False]
    data_frame['vocationId'] = data_frame['vocationId'].apply(vocation_name)
    data_frame['year_month'] = data_frame['auctionEnd'].dt.to_period('M')
    grouped = data_frame.groupby(['year_month', 'vocationId']).agg({
        'currentBid': ['sum']
    }).reset_index()

    grouped.columns = ['year_month', 'vocation', 'total_currentBid']
    print(grouped)
    pivot_table = grouped.pivot(index='year_month', columns='vocation', values='total_currentBid')

    # Plotar gráfico de barras empilhadas
    pivot_table.plot(kind='bar', figsize=(10, 6))

    # Adicionar título e rótulos aos eixos
    plt.title('Soma dos Lances por Mês/Ano e Vocação')
    plt.xlabel('Mês/Ano')
    plt.ylabel('Soma dos Lances (currentBid)')

    # Exibir a legenda
    plt.legend(title='Vocação')
    plt.show()


def treat_data(data_frame):
    def to_date(timestamp):
        date = datetime.date.fromtimestamp(timestamp)
        return pd.to_datetime(date)

    data_frame['auctionEnd'] = data_frame['auctionEnd'].apply(to_date)
    return data_frame


def filter_by_year(dataframe: pd.DataFrame, year: int) -> pd.DataFrame:
    return dataframe[dataframe['auctionEnd'].dt.year == year]


if __name__ == '__main__':
    with zipfile.ZipFile('./output/auction_history_2024_only.zip', 'r') as zip_ref:
        zip_ref.extractall('./output')
    df = pd.read_csv('./output/auction_history_2024_only.csv')
    print(df['auctionEnd'])
    df['auctionEnd'] = pd.to_datetime(df['auctionEnd'])
    # df_2024 = filter_by_year(dataframe=df, year=2024)
    # df_2024.to_csv('./output/auction_history_2024_only.csv')
    tibiacoins_vs_time(df)
    vocations_tibia_coins_vs_time(df)
