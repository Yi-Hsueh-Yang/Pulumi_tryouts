import pandas as pd
from kafka import KafkaConsumer
import time

def datacollection(collection_time, kafka_broker='localhost:9092', topic_name='movielog18'):

    # Creating Kafka consumer
    try:
        consumer = KafkaConsumer(topic_name, bootstrap_servers=kafka_broker)
    except Exception as e:
        print(f"Failed to create Kafka consumer: {e}")
        return pd.DataFrame()
    # Initializing an empty list to store the data
    data_list = []

    # Consume messages for the specified collection time
    start_time = time.time()
    for message in consumer:
        if time.time() - start_time >= int(collection_time):
            break
        try:
            # Parse the message
            parts = message.value.decode('utf-8').split(',')
            timestamp = pd.to_datetime(parts[0], errors='coerce')
            try: 
                userid = int(parts[1])
            except Exception as e:
                print(f"Failed to parse userid, wrong schema: {e}")
            request = parts[2]
            if pd.isnull(timestamp) or pd.isnull(userid):
                continue
            data_list.append({
                "timestamp": timestamp,
                "userid": userid,
                "request": request
            })
        except Exception as e:
            print(f"Failed to process message: {e}")

    # Close the consumer
    try:
        consumer.close()
    except Exception as e:
        print(f"Failed to close Kafka consumer: {e}")

    try:
        # Create a pandas DataFrame from the collected data
        df = pd.DataFrame(data_list)
    except Exception as e:
        print(f"Failed to process data into DataFrame: {e}")
        return pd.DataFrame()

    print("--- Data Collection From Kafka Complete! ---")
    return df

def seperate_ratings_and_movies(df):

    df_ratingsdata = df[df['request'].str.startswith('GET /rate')]
    extracted_data = df_ratingsdata.iloc[:, 2].str.extract(r'/rate/(.*?)=(\d+)')
    df_ratingsdata.loc[:, 'movieid'] = extracted_data[0]
    df_ratingsdata.loc[:, 'rating'] = extracted_data[1]

    # try and except to see if the rating value in df_ratingsdata is an integer within 1 to 5, else delete the row
    try:
        df_ratingsdata['rating'] = df_ratingsdata['rating'].astype(int)
        df_ratingsdata = df_ratingsdata[df_ratingsdata['rating'].between(1, 5)]
    except Exception as e:
        print(f"Rating value in wrong format or range: {e}")
        df_ratingsdata = df_ratingsdata.drop(df_ratingsdata.index)

    print("--- Data Separated to Ratings and Movies ---")

    return df_ratingsdata[['userid', 'movieid', 'rating']]


raw_data = datacollection(20)
seperate_ratings_and_movies(raw_data).to_json('ratings.json', orient='records')      