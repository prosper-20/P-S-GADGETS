from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.models import Product
from store.api.serializers import ProductSerializers



@api_view(['GET'])
def api_list_view(request):
    try:
        products = Product.objects.all()
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializers(products, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def api_detail_view(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    