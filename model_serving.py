import numpy as np
from model_training import rating, user_similarity_df, user

def recommend_movies(user_id, num_recommendations=5):
    try:
        # Get the most similar users to the target user_id
        similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:num_recommendations+1].index
        
        # Aggregate the ratings of these similar users
        similar_users_ratings = rating.loc[similar_users].mean(axis=0)
        # Sort the ratings in descending order
        recommended_movies = similar_users_ratings.sort_values(ascending=False).index.tolist()
        
        # Filter out movies the user has already rated
        already_rated = rating.loc[user_id][rating.loc[user_id] > 0].index
        recommendations = [movie for movie in recommended_movies if movie not in already_rated]
        
        return recommendations[:num_recommendations]
    except KeyError:
        # KeyError for when a user_id is not found in user_similarity_df or rating
        # print(f"User {user_id} not found. Returning default recommendations.")
        recommendations = ["the+wall+1975", "seven+samurai+1954", "monty+python+and+the+holy+grail+1975", "whiplash+2014", "the+godfather+1972"][:num_recommendations]
        
        return recommendations[:num_recommendations]

    except Exception as e:
        # Catch-all for any other exceptions
        # print(f"An error occurred: {e}. Returning default recommendations.")
        recommendations = ["stalag+17+1953", "final+destination+2000", "crumb+1994", "mansfield+park+1999", "the+wall+1975"][:num_recommendations]

        return recommendations[:num_recommendations]
        
while True:
    print(recommend_movies(int(np.random.choice(user, 1)), 5))
