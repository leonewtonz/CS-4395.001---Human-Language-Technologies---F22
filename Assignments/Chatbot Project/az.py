import pickle

topics = ['movies-anime', 'politics-philosophy', 'books-fiction',
          'games', 'music', 'technology', 'art-photography',
          'fashion-lifestyle', 'games-database', 'what-is-cyberpunk']

print(topics)

d = pickle.load(open('k_base.p', 'rb'))  # read binary

for k, v in d.items():
    print(k, v)
    print('\n*************\n')