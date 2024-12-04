import json

from django.forms.models import model_to_dict
from django.http import JsonResponse
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


@api_view(["GET", "POST"])
def api_home(request, *args, **kwargs):
    if request.method == "GET":
        try:
            instance = Product.objects.all().order_by("?").first()
            data = {}
            if instance:
                data = ProductSerializer(instance).data
            return Response(data)
        except Product.DoesNotExist:
            return JsonResponse({"Error": "No products found"})
        except Exception as e:
            return Response({"Error": str(e)}, status=500)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.data)
            return Response(serializer.data)
        return Response({"Invalid": "Missing or wrong fields provided"}, status=400)
    else:
        return Response({"Error": "Invalid method"}, statu=400)
