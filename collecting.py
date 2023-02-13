import glassdor_scraper as gs

path = "C:/Users/Damian/PycharmProjects/Praca dyplomowa/chromedriver"

df = gs.get_jobs('data scientist',500, path, 5)

df.to_csv('glassdoor_jobs.csv', index = False)