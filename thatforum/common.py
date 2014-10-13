from forum.models import ForumCategory

def context(request):
    c = {}
    c['top_level'] = ForumCategory.objects.filter(parent=None)
    return c
