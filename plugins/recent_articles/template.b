div (id='recent_articles') [
    ul [ 
        [ recent_articles_item (_i ['value'])
          for _i in v.articles_by_date ['rows'] ] 
    ]
]

