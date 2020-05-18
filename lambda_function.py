import json
import os
import boto3
import subprocess
import requests
import html2text
from glob import glob
from datetime import datetime
from readability import Document

subprocess.call('rm -rf /tmp/*', shell=True)

posts_directory = os.path.abspath('/tmp')
maxitem_url = 'https://hacker-news.firebaseio.com/v0/maxitem.json'
maxitem = requests.get(maxitem_url, timeout=20).json()
repository_name = 'esaleatorio'
commit_message = ''.join(['From AWS Lambda pushed new posts and deleted old ones at ', str(datetime.now())])
folder_path = 'content/'
branch_name = 'master'
    
client = boto3.client('codecommit')
s3= boto3.resource('s3')
bucket = s3.Bucket('esaleatorios3bucket')

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

    return post_content


#### Original Lambda function below

repository_name = 'esaleatorio'
commit_message = ''.join(['From AWS Lambda pushed new posts and deleted old ones at ', str(datetime.now())])
folder_path = 'content/'
branch_name = 'master'
    
def lambda_handler(event, context):
    response = client.get_folder(repositoryName=repository_name, folderPath=folder_path)
    current_posts = response['files']
    commit_id = response['commitId']
    posts = []
    new_posts = []
    old_posts = []

# Original Lambda function above
    item_list = []
    new_items = maxitem - 200
    post_count = 0

    for _ in range(new_items, maxitem):
        new_items += 1
        item_list.append(new_items)
    
    # If url are stories then 
    items_urls_list = new_items_url(item_list)

    for item in items_urls_list:

        if post_count >= 10:
            break

        response = check_url(item)

        if isinstance(response, dict):
            new_post = Story(item)
            new_post.id = str(response['id'])
            new_post.title = response['title']
            new_post.story_url = response['url']
            new_post.story_content()
            if new_post.content != None:
                posts.append(create_post(new_post.id, new_post.title, new_post.story_url, new_post.markdown))
                post_count += 1
        else:
            pass

# Original Lambda function below

    for current_post in current_posts:
        old_posts.append({'filePath': current_post.get('absolutePath')})


    for index,post in enumerate(posts, start=0):
        
        new_posts.append({'filePath': ''.join(['content/posts/post', str(index)],'.md'),
                        'fileContent': str.encode(post)
                        })


    print(new_posts)
    

    commit_response = client.create_commit(
        repositoryName=repository_name,
        branchName=branch_name,
        parentCommitId=commit_id,
        authorName='Antonio Hernandez',
        email='antonio@mlmusings.com',
        commitMessage=commit_message,
        #keepEmptyFolders=True,
        putFiles=new_posts
        #deleteFiles = old_posts
        )
    
    