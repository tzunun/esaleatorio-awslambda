import get_news
import os
import glob

if __name__ == "__main__":

    #Delete the posts/post*.MD files
#    files = glob.glob('content/posts/post*.md', recursive=True)
#    for file in files:
#        os.remove(file)
#

    script_directory = get_news.script_directory
    posts_directory = get_news.posts_directory
    maxitem_url = get_news.maxitem_url
    maxitem = get_news.maxitem
   # latest_post_file = get_news.latest_post_file
   # latest_post_id = get_news.get_latest_post_id(latest_post_file)
    item_list = []
    stories_urls_list = []
    new_items = maxitem - 200
    post_count = 0

    for i in range(new_items, maxitem):
        new_items += 1
        item_list.append(new_items)
    
    # If url are stories then 
    items_urls_list = get_news.new_items_url(item_list)

    for item in items_urls_list:

        if post_count >= 2:
            #get_news.save_latest_post_id(latest_post_id)
            break

        response = get_news.check_url(item)

        if isinstance(response, dict):
            new_post = get_news.Story(item)
            new_post.id = str(response['id'])
            new_post.title = response['title']
            new_post.story_url = response['url']
            new_post.story_content()
            if new_post.content != None:
                get_news.create_post(new_post.id, new_post.title, new_post.story_url, new_post.markdown)
                post_count += 1
                #latest_post_id = new_post.id
        else:
            pass