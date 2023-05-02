from .globals import CATEGORIES

def categories(request):
    return {'categories': CATEGORIES}