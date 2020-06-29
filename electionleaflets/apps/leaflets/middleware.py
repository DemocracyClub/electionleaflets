class SourceTagMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.method == "GET" and "source" in request.GET:
            request.session["source"] = request.GET.get("source")

        response = self.get_response(request)
        return response
