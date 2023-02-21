class name_middle:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self,request):
        self.request = request
        self.request.bankname = "Vertigo Credit Union"
        self.response = self.get_response(self.request)
        return self.response