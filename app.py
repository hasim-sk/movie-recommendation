from flask import Flask, render_template, request
import pandas as pd
import pickle
import requests

# load the nlp model and tfidf vectorizer from disk
data = pd.DataFrame(pickle.load(open('data.pkl','rb')))
movies = pd.read_csv('./archive/IMDB Movies.csv', dtype=str)

app=Flask(__name__)
app.config["CACHE_TYPE"] = "null"

def get_suggestions():
    #data = pd.read_csv('./archive/IMDB Movies.csv')
    return [(movies.loc[movies['imdb_title_id'] == row]['title']).item() for index, row in data.iloc[0].iteritems()]

def get_poster(movie_id):
    API_KEY = '69270bf301979a5401e919eb05fa9a53'
    url = 'https://api.themoviedb.org/3/movie/' + movie_id + '?api_key=' + API_KEY
    response = requests.get(url).json()
    if 'success' not in response:
        if response['poster_path']:
            poster = 'https://image.tmdb.org/t/p/original' + response['poster_path']
        else:
            poster = 'static/default.jpg'
    else:
        poster = 'static/default.jpg'
    return poster

def get_recommended_movies(title):
    movie_id_list = data[movies.loc[movies['title'] == title].iloc[0]['imdb_title_id']]

    rec_id = [(movies.loc[movies['imdb_title_id'] == row]['imdb_title_id']).item() for index, row in movie_id_list.iteritems()]
    rec_title = [(movies.loc[movies['imdb_title_id'] == row]['title']).item() for index, row in movie_id_list.iteritems()]
    rec_org_title = [(movies.loc[movies['imdb_title_id'] == row]['original_title']).item() for index, row in movie_id_list.iteritems()]
    rec_year = [(movies.loc[movies['imdb_title_id'] == row]['year']).item() for index, row in movie_id_list.iteritems()]
    rec_avg_vote = [(movies.loc[movies['imdb_title_id'] == row]['avg_vote']).item() for index, row in movie_id_list.iteritems()]
    rec_poster = [get_poster(row) for index, row in movie_id_list.iteritems()]

    return rec_poster, rec_title, rec_org_title, rec_year, rec_avg_vote

@app.route("/")
@app.route("/home")
def home():
    suggestions=get_suggestions()
    return render_template('home.html',suggestions=suggestions)

@app.route("/recommend",methods=["POST"])
def recommend():
    # getting data from AJAX request
    title = request.form['title']
    poster = get_poster(movies.loc[movies['title'] == title].iloc[0]['imdb_title_id'])
    overview = (movies.loc[movies['title'] == title].iloc[0]['description'])
    vote_average = (movies.loc[movies['title'] == title].iloc[0]['avg_vote'])
    release_date = (movies.loc[movies['title'] == title].iloc[0]['date_published'])
    runtime = (movies.loc[movies['title'] == title].iloc[0]['duration'])
    genres = (movies.loc[movies['title'] == title].iloc[0]['genre'])

    recom_movies = get_recommended_movies(title)

    # combining multiple lists as a dictionary which can be passed to the html file so that it can be processed easily and the order of information will be preserved
    movie_cards = {recom_movies[0][i]: [recom_movies[1][i],recom_movies[2][i],recom_movies[4][i],recom_movies[3][i]] for i in range(len(recom_movies[0]))}

    '''cast_ids = request.form['cast_ids']
    cast_names = request.form['cast_names']
    cast_chars = request.form['cast_chars']
    cast_bdays = request.form['cast_bdays']
    cast_bios = request.form['cast_bios']
    cast_places = request.form['cast_places']
    cast_profiles = request.form['cast_profiles']
    imdb_id = request.form['imdb_id']
    poster = request.form['poster']
    genres = request.form['genres']
    overview = request.form['overview']
    vote_average = request.form['rating']
    vote_count = request.form['vote_count']
    rel_date = request.form['rel_date']
    release_date = request.form['release_date']
    runtime = request.form['runtime']
    status = request.form['status']
    rec_movies = request.form['rec_movies']
    rec_posters = request.form['rec_posters']
    rec_movies_org = request.form['rec_movies_org']
    rec_year = request.form['rec_year']
    rec_vote = request.form['rec_vote']'''

    # get movie suggestions for auto complete
    #suggestions = get_suggestions()

    # call the convert_to_list function for every string that needs to be converted to list
    '''rec_movies_org = convert_to_list(rec_movies_org)
    rec_movies = convert_to_list(rec_movies)
    rec_posters = convert_to_list(rec_posters)
    cast_names = convert_to_list(cast_names)
    cast_chars = convert_to_list(cast_chars)
    cast_profiles = convert_to_list(cast_profiles)
    cast_bdays = convert_to_list(cast_bdays)
    cast_bios = convert_to_list(cast_bios)
    cast_places = convert_to_list(cast_places)
    
    # convert string to list (eg. "[1,2,3]" to [1,2,3])
    cast_ids = convert_to_list_num(cast_ids)
    rec_vote = convert_to_list_num(rec_vote)
    rec_year = convert_to_list_num(rec_year)'''
    
    # rendering the string to python string
    '''for i in range(len(cast_bios)):
        cast_bios[i] = cast_bios[i].replace(r'\n', '\n').replace(r'\"','\"')

    for i in range(len(cast_chars)):
        cast_chars[i] = cast_chars[i].replace(r'\n', '\n').replace(r'\"','\"') 
    
    # combining multiple lists as a dictionary which can be passed to the html file so that it can be processed easily and the order of information will be preserved
    movie_cards = {rec_posters[i]: [rec_movies[i],rec_movies_org[i],rec_vote[i],rec_year[i]] for i in range(len(rec_posters))}

    casts = {cast_names[i]:[cast_ids[i], cast_chars[i], cast_profiles[i]] for i in range(len(cast_profiles))}

    cast_details = {cast_names[i]:[cast_ids[i], cast_profiles[i], cast_bdays[i], cast_places[i], cast_bios[i]] for i in range(len(cast_places))}'''

    # web scraping to get user reviews from IMDB site
    # sauce = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
    # soup = bs.BeautifulSoup(sauce,'lxml')
    # soup_result = soup.find_all("div",{"class":"text show-more__control"})

    # reviews_list = [] # list of reviews
    # reviews_status = [] # list of comments (good or bad)
    # for reviews in soup_result:
    #    if reviews.string:
    #        reviews_list.append(reviews.string)
            # passing the review to our model
            # movie_review_list = np.array([reviews.string])
            # movie_vector = vectorizer.transform(movie_review_list)
            # pred = clf.predict(movie_vector)
            # reviews_status.append('Positive' if pred else 'Negative')

    # getting current date
    '''movie_rel_date = ""
    curr_date = ""
    if rel_date:
        today = str(date.today())
        curr_date = datetime.strptime(today,'%Y-%m-%d')
        movie_rel_date = datetime.strptime(rel_date, '%Y-%m-%d')'''

    # combining reviews and comments into a dictionary
    # movie_reviews = {reviews_list[i]: reviews_status[i] for i in range(len(reviews_list))}     

    # passing all the data to the html file
    # return render_template('recommend.html',title=title,poster=poster,overview=overview,vote_average=vote_average,
    #    vote_count=vote_count,release_date=release_date,movie_rel_date=movie_rel_date,curr_date=curr_date,runtime=runtime,status=status,genres=genres,movie_cards=movie_cards,reviews=movie_reviews,casts=casts,cast_details=cast_details)
    return render_template('recommend.html',title=title,poster=poster,overview=overview,vote_average=vote_average,release_date=release_date,runtime=runtime,genres=genres,movie_cards=movie_cards)

if __name__ == '__main__':
    app.run(debug=True)