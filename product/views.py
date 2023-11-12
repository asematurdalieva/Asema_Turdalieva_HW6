from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category, Review
from product.serializers import (ProductSerializer, CategorySerializer, ReviewSerializer,
                                 ProductCreateValidateSerializer, ReviewCreateValidateSerializer,
                                 CategoryCreateValidateSerializer)
from django.db.models import Avg
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class ProductsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        products_json = ProductSerializer(instance=products, many=True).data
        return Response(data=products_json)

    def post(self, request):
        serializer = ProductCreateValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': 'Request failed', 'errors': serializer.errors}
            )

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        categories = serializer.validated_data.get('category')

        product = Product.objects.create(title=title, description=description, price=price)
        product.category.set(categories)

        return Response(
            status=status.HTTP_201_CREATED,
            data={'id': product.id, 'title': product.title}
        )

class ProductDetailAPIView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product_json = ProductCreateValidateSerializer(product, many=False).data
        return Response(data=product_json)

    def put(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductCreateValidateSerializer(data=request.data)

        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            description = serializer.validated_data.get('description')
            price = serializer.validated_data.get('price')
            category = serializer.validated_data.get('category')

            product.title = title
            product.description = description
            product.price = price
            product.category.set(category)
            product.save()

            return Response(data={'message': 'Product updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'Invalid data', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'message': "Product deleted"})


class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        categories_json = CategorySerializer(categories, many=True).data
        return Response(data=categories_json)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,
                            data={'id': serializer.instance.id, 'name': serializer.instance.name})
        return Response(data={'message': 'Invalid data'},
                        status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category_json = CategorySerializer(category, many=False).data
        return Response(data=category_json)

    def put(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        serializer = CategoryCreateValidateSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,
                            data={'message': 'Category updated'})
        return Response(data={'message': 'Invalid data'},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': "Category deleted"})


class ReviewListAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        reviews_json = ReviewSerializer(reviews, many=True).data
        return Response(data=reviews_json)

    def post(self, request):
        serializer = ReviewCreateValidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,
                            data={'id': serializer.instance.id, 'text': serializer.instance.text})
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'message': 'Invalid data',
                              'errors': serializer.errors})


class ReviewDetailAPIView(APIView):
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        review_json = ReviewCreateValidateSerializer(review, many=False).data
        return Response(data=review_json)

    def put(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewCreateValidateSerializer(data=request.data)

        if serializer.is_valid():
            text = serializer.validated_data.get('text')
            product_id = serializer.validated_data.get('product_id')
            stars = serializer.validated_data.get('stars')

            review.text = text
            review.product_id = product_id
            review.stars = stars

            review.save()

            return Response(data={'message': 'Review updated successfully'}, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data={'message': "Review deleted"})


class ProductReviewsAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        reviews_json = ReviewSerializer(reviews, many=True).data
        return Response(data=reviews_json)


class AverageRatingAPIView(APIView):
    def get(self, request):
        average_rating = Review.objects.aggregate(avg_rating=Avg('stars'))
        return Response({'avg_rating': average_rating['avg_rating']})
