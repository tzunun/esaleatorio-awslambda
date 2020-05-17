import json
import os
import boto3
import subprocess
from datetime import datetime

repository_name = 'esaleatorio'
commit_message = ''.join(['From AWS Lambda pushed new posts and deleted old ones at ', str(datetime.now())])
folder_path = 'content/'
branch_name = 'master'


# Create new posts in tmp directory of the aws lambda environment
subprocess.call('news_handler.py', shell=True)
    
def lambda_handler(event, context):
    client = boto3.client('codecommit')
    response = client.get_folder(repositoryName=repository_name, folderPath=folder_path)
    current_posts = response['files']
    commit_id = response['commitId']
    posts = os.listdir('/tmp/')
    new_posts = []
    old_posts = []


    for current_post in current_posts:
        old_posts.append({'filePath': current_post.get('absolutePath')})


    for post in posts:
        new_posts.append({'filePath': ''.join(['content/posts/', post]),
                        'sourceFile': {'filePath': post}
                        })

    return posts    

    #commit_response = client.create_commit(
    #    repositoryName=repository_name,
    #    branchName=branch_name,
    #    parentCommitId=commit_id,
    #    authorName='Antonio Hernandez',
    #    email='antonio@mlmusings.com',
    #    commitMessage=commit_message,
    #    keepEmptyFolders=True,
    #    putFiles=new_posts,
    #    deleteFiles = old_posts
    #    )