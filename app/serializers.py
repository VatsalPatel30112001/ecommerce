from rest_framework import serializers
from datetime import date
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        # exclude = ['id']
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ['id']

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateField(
        format="%d/%m/%Y", 
        input_formats=["%d/%m/%Y", "%Y-%m-%d"] 
    )
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    order_items = OrderItemSerializer(many=True, read_only=True)
    order_item = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['customer', 'order_date', 'address', 'order_items', 'order_item']

    def validate_order_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("The order date cannot be in the past. It must be today or later.")
        return value

    def validate(self, attrs):
        order_items_data = attrs.get('order_item')
        
        total_weight = 0
        for item_data in order_items_data:
            product = item_data.get('product')
            quantity = item_data.get('quantity', 1)
            total_weight += product.weight * quantity

        if total_weight > 150:
            raise serializers.ValidationError("Total weight of order items exceeds 150 kg.")

        return attrs

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_item')  

        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def update(self, instance, validated_data):
        instance.customer = validated_data.get('customer', instance.customer)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        order_items_data = validated_data.pop('order_item', [])
        instance.order_items.all().delete() 

        for item_data in order_items_data:
            OrderItem.objects.create(order=instance, **item_data)

        return instance