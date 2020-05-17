import get_news

if __name__ == "__main__":

    script_directory = get_news.script_directory
    posts_directory = get_news.posts_directory
    maxitem_url = get_news.maxitem_url
    maxitem = get_news.maxitem
    item_list = []
    stories_urls_list = []
    new_items = maxitem - 2000
    post_count = 0

    for i in range(new_items, maxitem):
        new_items += 1
        item_list.append(new_items)
    
    # If url are stories then 
    items_urls_list = get_news.new_items_url(item_list)

    for item in items_urls_list:

        if post_count >= 50:
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
        else:
            pass