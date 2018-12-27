import pandas as pd 

def drop_exist_id(tweet_data):
    df_tweet_data = pd.DataFrame(tweet_data, columns=["id", "time", "text", "name"])
    project_id = "strategic-alter-207405"
    query = """
        SELECT 
            id
        FROM 
            twitter_img.id_set
        WHERE 
            id IN 
        """

    id_arr = [str(x[0]) for x in tweet_data]
    query += "('" + "', '".join(id_arr) + "')"

    result = pd.read_gbq(query=query, project_id=project_id, dialect="standard")

    # resultとdf_tweet_dataの差分をとる
    df_exist = result.merge(df_tweet_data, how="left") # すでに取ってきたid
    diff = df_tweet_data[~df_tweet_data["id"].isin(df_exist["id"])] # df_tweet_dataとdf_existの差分

    return diff.values.tolist()
    

def insert_to_bq(tweet_data, img_nums):
    df_tweet_data = pd.DataFrame(tweet_data, columns=["id", "time", "text", "name"]) 

    project_id = "strategic-alter-207405"
    query = """
        INSERT INTO id_set (id, img_num, timestamp) 
        VALUES 
        """
    i = 0
    for tweet, num in zip(tweet_data, img_nums):
        value = "( '" + tweet[0] + "', " + num + ", CURRENT_TIMESTAMP()) "
        if i==0:
            value = "," + value 
            i += 1
        
        query += value 

    pd.read_gbq(query=query, project_id=project_id, dialect="standard")