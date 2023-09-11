from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    template_name = 'hello.html'

    def get(self, request):
        return render(request, self.template_name)
