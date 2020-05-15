import os
import requests
import html2text
from datetime import datetime
from readability import Document

script_directory = os.path.dirname(os.path.abspath(__file__)) 
posts_directory = '/tmp'
maxitem_url = 'https://hacker-news.firebaseio.com/v0/maxitem.json'
maxitem = requests.get(maxitem_url, timeout=20).json()

class Story: 

    '''
    Create a story markdown, by first obtaining information from news.ycombinator using the item number 
    the json response contains the id, stroy title and the the story url. 
    Using that url we are able to get the story content and the this gets converted to markdown in order to be translated to Spanish.

    The markdown convertion helps to get the story in a format that can then be saved a posted almost immediately.
    ''' 

    def __init__(self, url): 
        self.id = ''
        self.title = '' 
        self.content = None
        self.markdown = '' 
        self.story_url = '' 
    
    def story_content(self): 
        response = requests.get(self.story_url, timeout=20) 
        try: 
            if response.ok: 
                self.content = Document(response.content).summary() 
                self.story_markdown()
        except: 
            pass
    
    def story_markdown(self): 
        ''' Will return the story's text in markdown format ''' 
        html_to_markdown = html2text.HTML2Text() 
        html_to_markdown.ignore_links = False 
        self.markdown = html_to_markdown.handle(self.content) 
    

def new_items_url(items):
    base_url = "https://hacker-news.firebaseio.com/v0/item/"
    """ Generator of urls, each url will return a dictionary containing information about the story including the story's source url. """
    for item in items:
        yield ''.join([base_url, str(item), '.json'])

def check_url(url):
    """ Return the actual story url, the one that was submitted to HN. """
    try:
        response = requests.get(url, timeout=20)
        if response.ok and isinstance((response.json()), dict):
            if response.json()['type'] == 'story' and response.json()['url']:
                return response.json()
            else:
                return 'empty'
    except:
        pass  # This is intentional I don't want to keep track of failed urls

def create_post(story_id, story_title, story_url, story_markdown_content):
    today = datetime.today().strftime('%Y-%m-%d')
    file_name = ''.join(['post-', story_id, '.md'])
    new_post = os.path.join(posts_directory, file_name)
    post_header = ''.join(['---\ntitle: ', '\"', story_title, '\"', ' \ndate: ', str(today), ' \ndraft: false \n---\n\n'])
    post_content = ''.join([post_header, 'Story source:', '\n\n', story_url, '\n\n\n', story_markdown_content]) 

    with open(new_post, 'w') as file:
        file.write(post_content)