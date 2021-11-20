from django.core.paginator import Paginator

# Number of posts per page
POSTS_PER_PAGE = 3


def paginate_posts(request, posts):
    """
    Paginating posts
    """
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
