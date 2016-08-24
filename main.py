import webapp2
import cgi
import jinja2
import os


# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

# we'll use this template in a few places
t_scaffolding = jinja_env.get_template("scaffolding.html")

# a list of movies that nobody should be allowed to watch
terrible_movies = [
    "Gigli",
    "Star Wars Episode 1: Attack of the Clones",
    "Paul Blart: Mall Cop 2",
    "Nine Lives"
]


def getUnwatchedMovies():
    """ Returns the list of movies the user wants to watch (but hasn't yet) """

    # for now, we are just pretending
    return [ "Star Wars", "Minions", "Freaky Friday", "My Favorite Martian" ]


def getWatchedMovies():
    """ Returns the list of movies the user has watched """

    # for now, just pretending
    return [ "The Matrix", "Wall-E", "The Act of Killing", "The Big Green" ]


class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """

    def get(self):
        t_frontpage = jinja_env.get_template("frontpage.html")
        frontpage_content = t_frontpage.render(
                        unwatched_movies = getUnwatchedMovies(),
                        error = self.request.get("error"))
        response = t_scaffolding.render(
                    title = "FlickList: Movies I Want to Watch",
                    content = frontpage_content)
        self.response.write(response)


class AddMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/add'
        e.g. www.flicklist.com/add
    """

    def post(self):
        new_movie = self.request.get("new-movie")

        # if the user typed nothing at all, redirect and yell at them
        if (not new_movie) or (new_movie.strip() == ""):
            error = "Please specify the movie you want to add."
            self.redirect("/?error=" + cgi.escape(error))

        # if the user wants to add a terrible movie, redirect and yell at them
        if new_movie in terrible_movies:
            error = "Trust me, you don't want to add '{0}' to your Watchlist.".format(new_movie)
            self.redirect("/?error=" + cgi.escape(error, quote=True))

        # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
        new_movie_escaped = cgi.escape(new_movie, quote=True)

        # render the confirmation message
        t_add = jinja_env.get_template("add.html")
        add_content = t_add.render(movie = new_movie_escaped)
        response = t_scaffolding.render(
                        title = "FlickList: Add a Movie",
                        content = add_content)
        self.response.write(response)


class WatchMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/cross-off'
        e.g. www.flicklist.com/cross-off
    """

    def post(self):
        watched_movie = self.request.get("watched-movie")

        # if the movie movie is just whitespace (or nonexistant), reject.
        if not watched_movie or watched_movie.strip() == "":
            self.error(400)
            return

        # if user tried to cross off a movie that is not in their list, reject
        if not (watched_movie in getUnwatchedMovies()):
            self.error(400)
            return

        # render confirmation page
        t_watched_it = jinja_env.get_template("watched-it.html")
        watched_it = t_watched_it.render(movie = watched_movie)
        response = t_scaffolding.render(
                    title = "FlickList: You Watched a Movie",
                    content = watched_it)
        self.response.write(response)


class MovieRatings(webapp2.RequestHandler):
    """ Handles requests coming in to '/ratings'
        e.g. www.flicklist.com/ratings
    """

    def get(self):
        t_ratings = jinja_env.get_template("ratings.html")
        ratings_content = t_ratings.render(movies = getWatchedMovies())
        response = t_scaffolding.render(
                    title = "FlickList: My Ratings",
                    content = ratings_content)
        self.response.write(response)




app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', AddMovie),
    ('/watched-it', WatchMovie),
    ('/ratings', MovieRatings)
], debug=True)
