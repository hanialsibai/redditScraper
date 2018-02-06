import praw
import os
import atexit
try:
    import cPickle as pickle
except:
    import pickle

reddit = praw.Reddit('bot1')

# Create a set(so no duplicates) of all posts already downloaded
SEEN_POSTS = set()

#Choose subreddit
subreddit = reddit.subreddit("dailyprogrammer")

# Determine folder path
hard = 'Hard'
easy = 'Easy'
intermediate = 'Intermediate'

# Load seen posts data from disk
if os.path.exists('seen.pkl'):
    with open('seen.pkl','rb') as data_file:
        SEEN_POSTS = pickle.load(data_file)

# Write submission to new file
def writeToFile(path):
    with open(os.path.join('/media/hani/Hani/Work/Projects/challengeScraper/Data/' + path,title),'w') as f:
        f.write(submission.shortlink +"\n" + submission.selftext.encode('ascii','ignore'))

# @atexit guarantees that the seen posts set will be saved no matter how the programs
# is ended
@atexit.register
def save_seen_posts():
    with open("seen.pkl",'wb') as f:
        pickle.dump(SEEN_POSTS,f)

def runScript():
    for submission in subreddit.new(limit=None):
        if submission.id in SEEN_POSTS:
            continue
        #Replacing any possible "/" so that the file will be saved to a correct path
        title = submission.title.replace('/',' ')
        if easy in title:
            writeToFile(easy)
        elif intermediate in title:
            writeToFile(intermediate)
        elif hard in title:
            writeToFile(hard)
        #mark submission as seen
        SEEN_POSTS.add(submission.id)
        print("Success!!")

save_seen_posts()
runScript()
