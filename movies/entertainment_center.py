import media
import fresh_potatoes

flipped = media.Movie("Flipped",
                      "A puppy lovestory of a boy and a girl",
                      "https://baike.baidu.com/pic/%E6%80%A6%E7%84%B6%E5%BF%83%E5%8A%A8/413/18592731/10dfa9ec8a136327c04074c8978fa0ec09fac798?fr=lemma#aid=18592732&pic=cf1b9d16fdfaaf51f0d533448a5494eef01f7a12",
                      'http://baidu.boosj.com/watch/01634263454686425181.html?page=videoMultiNeed')


In_the_Mood_for_love = media.Movie('In_The_Mood_For_Love',
                                   'The secrete love between a young man and woman',
                                   'https://baike.baidu.com/pic/%E8%8A%B1%E6%A0%B7%E5%B9%B4%E5%8D%8E/35761/18509540/96dda144ad34598299eced150af431adcaef84d6?fr=lemma#aid=18509540&pic=96dda144ad34598299eced150af431adcaef84d6',
                                   'http://baidu.ku6.com/watch/3370950733675796667.html?fr=ps_ala11&wd=flipped+%D4%A4%B8%E6%C6%AC')

#movies = [flipped,In_the_Mood_for_love]
#fresh_potatoes.open_movies_page(movies)
print(media.Movie.__module__)

