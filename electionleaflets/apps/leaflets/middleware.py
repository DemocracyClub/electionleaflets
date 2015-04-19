class SourceTagMiddleware(object):

    def process_request(self, request):
        if request.method == 'GET' and 'source' in request.GET:
            request.session['source'] = request.GET.get('source')

