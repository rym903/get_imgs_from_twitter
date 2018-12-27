import pandas as pd 

def drop_exist_id(tweet_data):
    df_tweet_data = pd.DataFrame(tweet_data, columns=["id", "time", "text", "name"])
    project_id = "strategic-alter-207405"
    query = """
        SELECT 
            id
        FROM 
            twitter_img.id
        WHERE 
            id IN 
        """

    id_arr = [str(x[0]) for x in tweet_data]
    query += "('" + "', '".join(id_arr) + "')"

    result = pd.read_gbq(query=query, project_id=project_id, dialect="standard")
    result = result.merge(df_tweet_data, how="left")

    return result.values.tolist()
    