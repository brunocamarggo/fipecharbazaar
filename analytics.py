import pandas as pd
import matplotlib.pyplot as plt
import datetime

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


def treat_data(data_frame):
    def to_date(timestamp):
        date = datetime.date.fromtimestamp(timestamp)
        return pd.to_datetime(date)

    data_frame['auctionEnd'] = data_frame['auctionEnd'].apply(to_date)
    return data_frame


if __name__ == '__main__':
    df = pd.read_json('./data/auction_history_16_06_2024.jsonl', lines=True)
    df = treat_data(df)
    tibiacoins_vs_time(df)