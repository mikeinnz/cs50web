def posts_list_with_num_likes(posts):
    """
    Add number of likes to each post in a posts list
    """
    plist = []
    for p in posts:
        p.num_likes = p.liked_users.all().count()
        plist.append(p)
    return plist
