#Popular based reccommender
#https://towardsdatascience.com/a-complete-guide-to-recommender-system-tutorial-with-sklearn-surprise-keras-recommender-5e52e8ceace1

'''
votes = number of votes for item
min = min votes required to be listed in popular items
    defined by > percentile 80 of total votes
rating = average rating for item
average = average rating across whole dataset
'''
def weighted_rating(votes, min, Rating, Average):
   return ((votes / (votes + min)) * Rating) + ((min / (votes + min)) * Average)

def assign_popular_based_score(rating_df, item_df, user_col, item_col, rating_col):
    '''
    assigns popular based score based on the IMDB weighted average
    
    rating = pd.DataFrame contaning ['item_id', 'rating'] for eahc user

    Returns:
    popular_items = pd.DataFrame containing item and IMDB weighted score

    '''

    #pre processing
    vote_count = (
        rating_df
        .groupby(item_col, as_index=False)
        .agg({user_col:'count', rating_col:'mean'})
        #what does this do?
    )
    vote_count.columns = [item_col, 'vote_count', 'avg_rating'] #setting up columns of data frame?

    #calculate input params
    Average = np.mean(vote_count['avg_rating'])
    min = np.percentile(vote_count['vote_count'], 70)
    vote_count = vote_count[vote_count['vote_count'] >= min]
    Rating = vote_count['avg_rating']
    votes = vote_count['vote_count']
    vote_count['weighted_rating'] = weighted_rating(votes, min, Rating, Average)

    #post processing
    vote_count = vote_count.merge(item_df, on = [item_col], how = 'left') #ivestigate syntax of .merge()
    popular_items = vote_count.loc[:, [item_col, 'genres', 'vote_count', 'avg_rating', 'weighted_rating']]

    return popular_items

#init constants
USER_COL = 'user_id'
ITEM_COL =  'item_id'
RATING_COL = 'rating'

#calculate popularity based
pop_items = assign_popular_based_score(ratings, items, USER_COL, ITEM_COL, RATING_COL)
pop_items = pop_items.sort_values('weighted_rating', ascending = False)

#plot the popularity based on the weighted score
fix, ax = plt.subplots(figsize=(9, 6))
sns.barplot(data = pop_items.head(10),
            y = 'item_id',
            x = 'weighted_rating',
            pallete = 'mako');
sns.despise();
