import json
from django.http import JsonResponse
from rest_framework.views import APIView

from .models import *
from .serializers import *

class Customers(APIView):
    def get(self, request):
        data = Customer.objects.all()

        serializer = CustomerSerializer(data, many=True)
        return JsonResponse({
            'status': 'success',
            'data': serializer.data if serializer else []
        }, status=200)

    def post(self, request):
        customer_data = request.data
        serializer = CustomerSerializer(data=customer_data)
        
        if serializer.is_valid():
            customer = serializer.save() 

            return JsonResponse({
                'status': 'success',
                'message': 'Customer added successfully.'
            }, status=201)
        else:
            return JsonResponse({
                'status': 'fail',
                'message': 'Invalid data provided.',
                'errors': serializer.errors
            }, status=400)

    def put(self, request, id):
        customer_obj = Customer.objects.filter(id=id).first()

        if not customer_obj:
            return JsonResponse({
                'status': 'fail',
                'message': 'Customer with provided ID does not exist.'
            }, status=404)

        serializer = CustomerSerializer(customer_obj, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Customer updated successfully.'
            }, status=200)
        else:
            return JsonResponse({
                'status': 'fail',
                'message': 'Invalid data provided.',
                'errors': serializer.errors
            }, status=400)

class Products(APIView):
    def get(self, request):
        data = Product.objects.all()

        serializer = ProductSerializer(data, many=True)
        return JsonResponse({
            'status': 'success',
            'data': serializer.data if serializer else []
        }, status=200)

    def post(self, request):
        product_data = request.data

        serializer = ProductSerializer(data=product_data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'status': 'success',
                'message': 'product created successfully.',
                'product_id': serializer.data['id']
            }, status=201)
        else:
            return JsonResponse({
                'status': 'fail',
                'message': 'Invalid data provided.',
                'errors': serializer.errors
            }, status=400)

class Orders(APIView):
    def get(self, request):
        customer = request.GET.get('customer', None)
        products = request.GET.get('products', None)
        data = []
        if customer:
            customer_obj = Customer.objects.filter(name=customer).first()
            if not customer_obj:
                return JsonResponse({
                    'status': 'fail',
                    'message': 'Customer with provided name does not exist.'
                }, status=404)

            data = Order.objects.filter(customer=customer_obj)

        elif products:            
            products = json.loads(products)
            order_items = OrderItem.objects.filter(product__name__in=products)

            if not order_items.exists():
                return JsonResponse({
                    "status":'fail',
                    "message": "No matching orders found for the given products."
                }, status=400)

            data = Order.objects.filter(order_items__in=order_items).distinct()
        
        else:
            data = Order.objects.all()

        serializer = OrderSerializer(data, many=True)

        return JsonResponse({
            'status': 'success',
            'data': serializer.data if serializer else []
        }, status=200)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Order added successfully.'
            }, status=201)
        return JsonResponse({
                'status': 'fail',
                'message': 'Invalid data provided.',
                'errors': serializer.errors
            }, status=400)

    def put(self, request, id):
        order_obj = Order.objects.filter(id=id).first()

        if not order_obj:
            return JsonResponse({
                'status': 'fail',
                'message': 'Order with provided ID does not exist.'
            }, status=404)

        serializer = OrderSerializer(order_obj, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Order updated successfully.'
            }, status=200)
        else:
            return JsonResponse({
                'status': 'fail',
                'message': 'Invalid data provided.',
                'errors': serializer.errors
            }, status=400)
