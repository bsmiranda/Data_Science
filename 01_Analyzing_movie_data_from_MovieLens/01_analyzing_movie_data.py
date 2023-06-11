# -*- coding: utf-8 -*-
"""01-Analyzing_movie_data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_LfIL1WUxC9hJ2B-dhg8Ea3h29fwAx0W

## Analyzing Movie Data from MovieLens

MovieLens is a movie recommendation system for its users to watch, based on their preferences. In this notebook, we will analyze a MovieLens movie dataset, performing exploratory data analysis using Python and libraries such as Pandas, Matplotlib, and Seaborn.

Project path:

Knowing our database;
Visualize the data with histograms and boxplot;
Exploratory data analysis;
View charts by category;
Visualization refinement;
Statistical data (mean, median, standard deviation, boxplot, histogram, central tendency and dispersion)

## Getting the Data

The database used in this project can be found at grouplens.org.

We will use a dataset with 100,000 ratings applied to 9,000 movies by 600 users.

Download the database here: ml-latest-small.zip
"""

!pip install seaborn==0.9.0

import seaborn as sns
print(sns.__version__)

import pandas as pd

notes = pd.read_csv("ratings.csv")
notes.head()

notes.shape

""".unique() returns us the unique values of the Series object that are returned in order of appearance, from most frequent to least frequent.

So we can see that note 4 is the most frequent, followed by notes 5 and 3 which were the most frequent.

Notes 2.5, 0.5 and 1.5 were the least frequent.

"""

notes["rating"].unique()

""".value_counts() Returns a Series containing counts of unique values.

The resulting object will be in descending order in which the first element occurs most frequently.

So we can see how many times each note was given.
"""

notes["rating"].value_counts()

""".mean() and .median() return the average and median of the notes respectively. The average score was 3.5 and the median score was 4.0"""

print("Mean" ,notes["rating"].mean())
print("Median" ,notes["rating"].median())

notes.rating.head()

"""Now we can plot the notes in a histogram with .plot() passing the kind='hist' parameter of pandas in a very easy way.

Looking at the graph below, it is easy to see that notes 4, 3 and 5 were the most evaluated in the survey.
"""

notes.rating.plot(kind='hist')

"""Generating descriptive statistics with .describe(). Descriptive statistics include those that summarize the central tendency, dispersion, and distribution shape of a data set."""

notes["rating"].describe()

"""We can use a box method to graph groups of numerical data with their quartiles. Outliers are plotted as separate data."""

sns.boxplot(notes["rating"])

"""# Looking at the movies

Now let's look at some specific movies from the movies.csv file. This file contains 3 columns (movieId, title and genres) and 9742 movies that were rated.
"""

films = pd.read_csv("movies.csv")
films.head()

films.shape

notes.head()

"""## Analyzing some specific notes per film

With .query() we can query specific columns of a DataFrame with a boolean expression, for example, checking the average scores of each movie.
"""

notes.query("movieId==1")["rating"].mean() # (Toy Story)

notes.query("movieId==2")["rating"].mean() # Jumanji

"""Grouping the notes by the film column, we will have a grouping of the notes for each film and thus we can take the average of all films at once.

After that I can save this grouping of averages per film in a variable and plot the data.
"""

notes.groupby("movieId")

notes.groupby("movieId")["rating"].mean()

averages_per_film = notes.groupby("movieId")["rating"].mean()
averages_per_film.head()

averages_per_film.plot(kind='hist')

"""Let's create a boxplot with seaborn and import the matplotlib.pyplot library to have more control over the boxplot settings.

With .figure() we can pass the figsize parameter, which allows us to have greater control over the width and height in inches.
"""

import matplotlib.pyplot as plt

plt.figure(figsize=(5,8))
sns.boxplot(y=averages_per_film)

averages_per_film.describe()

sns.distplot(averages_per_film) # distribution graph with sns.distplot

plt.hist(averages_per_film)
plt.title("Histogram of Movies Averages")

"""## Analisando tmdb_5000

Let's look at another dataset called tmdb_5000. It contains some data like budget, genre, original language, popularity... let's check the data related to the original language of movies.
"""

tmdb = pd.read_csv("tmdb_5000_movies.csv")
tmdb.head()

tmdb["original_language"].unique()

tmdb["original_language"].value_counts().index

tmdb["original_language"].value_counts().values

"""Vamos contar quantas vezes cada lingua aparece e guardar esse valor em uma variável. Depois, criar um DataFrame com to_frame() e resetar o index."""

language_count = tmdb["original_language"].value_counts() # return the values 
language_count

language_count = tmdb["original_language"].value_counts().to_frame() # turns the Series into a DataFrame
language_count.head()

language_count = tmdb["original_language"].value_counts().to_frame().reset_index() # reset the index
language_count.head()

sns.catplot(x = "original_language", kind="count", data = tmdb)

"""There is a much simpler way to plot this data using catplot, where we pass "original_language" on the x-axis, kind="count" and data = tmdb. But the graph below does not show the information very clearly, it just shows that there are many more films in English than in the others."""

sns.catplot(x="original_language", kind="count", data = tmdb)

"""To pass on the information that the English language has a much greater prominence than other languages, we can compare English with other languages at once."""

total_per_language = tmdb["original_language"].value_counts() # count all languages
grand_total = total_per_language.sum() # sum of all languages
total_english = total_per_language.loc["en"] # total english
total_other_languages = grand_total - total_english # total of all languages - ingles
print(total_english, total_other_languages)

"""Now we can use these values to create a DataFrame and plot the data using seaborn in a barplot."""

language_data = {
    'language': ['english', 'others'],
    'total': [total_english, total_other_languages]
}
language_data = pd.DataFrame(language_data)
language_data

sns.barplot(x="language", y="total", data = language_data)

plt.pie(language_data["total"], labels = language_data["language"])

"""Let's analyze the category of movies that are in other languages. To do this, let's take the entire DataFrame containing all the original language categories and remove the films that are in English, thus leaving the films that are in other languages."""

tmdb.query("original_language == 'en'") # here we have all the movies in English

tmdb.query("original_language != 'en'") # here we have all movies with language other than English

"""Extracting the values for each language using .value_counts(). We can see that French is the most frequent language in the non-English language category. But even so, the difference between the number of films made in English and in French is very large. There are 4,505 films in English against 70 films in French."""

tmdb.query("original_language != 'en'").original_language.value_counts()

# storing language data from other movies in a new variable
total_language_other_films = tmdb.query("original_language != 'en'").original_language.value_counts()
total_language_other_films

"""Plotting the data from movies in other languages with sns.catplot() we get an interesting graph where we can see the significant differences in the number of movies in other languages. But this chart is still quite disorganized and could be improved."""

films_without_original_language_english = tmdb.query("original_language != 'en'")

sns.catplot(x="original_language", kind="count",
            data = films_without_original_language_english)

"""A more organized chart configuring the parameters that sns.boxplot allows us.

Here I put the data in order from most frequent to least frequent, set the color palette in shades of blue (from darkest to lightest) and tweaked the scalar aspect.
"""

sns.catplot(x = "original_language",
            kind = "count",
            data = films_without_original_language_english,
            aspect = 2,
            order = total_language_other_films.index,
            palette = "GnBu_d")

