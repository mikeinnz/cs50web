from django.core.paginator import Paginator

# Number of posts per page
POSTS_PER_PAGE = 10


def posts_list_with_num_likes(posts):
    """
    Add number of likes to each post in a posts list
    """
    plist = []
    for p in posts:
        p.num_likes = p.liked_users.all().count()
        plist.append(p)
    return plist


def paginate_posts(request, posts):
    """
    Paginating posts
    """
    paginator = Paginator(posts_list_with_num_likes(posts), POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
