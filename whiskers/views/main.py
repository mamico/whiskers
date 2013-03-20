from pyramid.renderers import get_renderer


def whiskers_view(request):
    main = get_renderer('whiskers:views/templates/master.pt').implementation()
    return {'project': 'whiskers', 'main': main}
