from pandas import DataFrame, Series
import numpy

countries = ['Russian Fed.', 'Norway', 'Canada', 'United States',
             'Netherlands', 'Germany', 'Switzerland', 'Belarus',
             'Austria', 'France', 'Poland', 'China', 'Korea',
             'Sweden', 'Czech Republic', 'Slovenia', 'Japan',
             'Finland', 'Great Britain', 'Ukraine', 'Slovakia',
             'Italy', 'Latvia', 'Australia', 'Croatia', 'Kazakhstan']

gold = [13, 11, 10, 9, 8, 8, 6, 5, 4, 4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
silver = [11, 5, 10, 7, 7, 6, 3, 0, 8, 4, 1, 4, 3, 7, 4, 2, 4, 3, 1, 0, 0, 2, 2, 2, 1, 0]
bronze = [9, 10, 5, 12, 9, 5, 2, 1, 5, 7, 1, 2, 2, 6, 2, 4, 3, 1, 2, 1, 0, 6, 2, 1, 0, 1]

df = DataFrame({'Country_name':Series(countries),
                'Gold':Series(gold),
                'Silver':Series(silver),
                'Bronze':Series(bronze)})

def avg_bronze_medal_count():
    '''
    compute the average number of bronze medals earned by countries who
    earned at least one gold medal.

    Save this to a variable named avg_bronze_at_least_one_gold.

    '''
    avg = df[['Bronze','Gold','Silver']].apply(numpy.mean)
    print avg


def points():
    '''
        Imagine a point system in which each country is awarded 4 points for each
        gold medal,  2 points for each silver medal, and one point for each
        bronze medal.

        Using the numpy.dot function, create a new dataframe called
        'olympic_points_df' that includes:
            a) a column called 'country_name' with the country name
            b) a column called 'points' with the total number of points the country
               earned at the Sochi olympics.
    '''
    score = [4,2,1]
    scores = numpy.dot(df[['Gold','Silver','Bronze']],score)
    olympic_points_df =DataFrame({'Country_name':Series(countries),
                                  'Points':Series(scores)})
    #print scores
    print  olympic_points_df

def points_2():
    df['points'] = df[['Gold','Silver','Bronze']].dot([4,2,1])
    olympic_points_df = df[['Country_name','points']]
    print olympic_points_df
    
points_2()











