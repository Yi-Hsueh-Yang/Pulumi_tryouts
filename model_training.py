import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

rating = pd.read_json('src/ratings.json')
user = rating.userid.unique()

# Create a user-item rating matrix
rating_matrix = rating.pivot_table(index='userid', columns='movieid', values='rating').fillna(0)

# Convert the rating matrix to a sparse matrix for efficiency
rating_matrix_sparse = sparse.csr_matrix(rating_matrix.values)

# Compute the cosine similarity between users
user_similarity = cosine_similarity(rating_matrix_sparse)

# Convert to DataFrame for easier manipulation
user_similarity_df = pd.DataFrame(user_similarity, index=rating_matrix.index, columns=rating_matrix.index)
