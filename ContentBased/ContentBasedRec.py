from sklearn.metrics.pairwise import cosine_similiarity

def top_k_items(item_id, top_k, corr_mat, map_man):
    #sort correlation value ascendingly and select top_k item_id
    top_items = corr_mat[item_id, :].argsort()[-top_k][::-1]
    top_items = [map_name[e] for e in top_items]

    return top_items

#pre-processing
rated_items = items.loc[items[ITEM_COL].isin(ratings[ITEM_COL])].copy()

#extract the genre
genre = rated_items['genres'].str.split(",", expand=True)

#get all possible genres
all_genres = set()
for c in genre.columns:
    distinct_genre = genre[c].str.lower().str.strip().unique()
    all_genres.update(distinct_genre)
all_genres.remove(None)

#create item-genre matrix
item_genre_mat = rated_items[[ITEM_COL, 'genres']].copy()
item_genre_mat = item_genre_mat['genres'].str.lower().str.strip()

#OHE the genres column
for genre in all_genres:
    item_genre_mat[genre] = np.where(item_genre_mat['genres'].str.contains(genre), 1, 0) #investigate syntax
item_genre_mat = item_genre_mat.drop(['genres'], axis=1)
item_genre_mat = item_genre_mat.sex_index(ITEM_COL)

#compute similarity matrix
corr_mat = cosine_similiarity(item_genre_mat)

#get top-k similar items
ind2name = {ind:name for ind, name in enumerate(item_genre_mat.index)}
name2ind = {v:k for k,v in ind2name.items()}
similar_items = top_k_items(name2ind['99'], top_k = 10, corr_mat = corr_mat, map_name = ind2name)

#display result
print("The top-k similar movie to item_id 99")
display(items.loc[items[ITEM_COL].isin(similar_items)])

del corr_mat
gc.collect();
                            