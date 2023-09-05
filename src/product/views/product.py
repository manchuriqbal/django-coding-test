from typing import Any, Dict
from datetime import datetime
from django.db.models import Q, Subquery, OuterRef
from django.views import generic
from django.shortcuts import render
from django.db.models import Count
from product.models import Variant, Product, ProductVariant



from django.http import JsonResponse
import json 


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            title = data.get('title')
            sku = data.get('sku')
            description = data.get('description')
            
            # Perform product creation and save it to the database
            product = Product(title=title, sku=sku, description=description)
            product.save()

            # You can also handle variants and prices here if needed

            return JsonResponse({'message': 'Product created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


    
class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    queryset = Product.objects.all()
    context_object_name = "product_list"



    def get_queryset(self):
        queryset = super().get_queryset()
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')

        if date:
            date = datetime.strptime(date, '%Y-%m-%d').date()
            queryset = queryset.filter(updated_at__date=date)

        if self.request.GET.get('title'):
            queryset = queryset.filter(title__contains=self.request.GET.get('title'))

        # Modify the queryset to filter based on related ProductVariantPrice instances
        if price_from and price_to:
            queryset = queryset.filter(
                product_variant_price__price__gte=price_from,
                product_variant_price__price__lte=price_to
            )
        elif price_from:
            queryset = queryset.filter(product_variant_price__price__gte=price_from)
        elif price_to:
            queryset = queryset.filter(product_variant_price__price__lte=price_to)

        queryset = queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate the total_product_count based on the filtered queryset
        total_product_count = context['product_list'].count()

        context['total_product_count'] = total_product_count

        context['products_variants'] = ProductVariant.objects.values('variant_title')\
            .annotate(Count('id')).order_by().filter(id__count__gt=1)

        return context
    
        
