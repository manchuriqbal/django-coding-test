from typing import Any, Dict
from datetime import datetime
from django.db.models.query import QuerySet
from django.db.models import Q, Subquery, OuterRef
from django.views import generic
from django.shortcuts import render
from django.db.models import Count
from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from django.http import Http404


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    
class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    queryset = Product.objects.all()
    context_object_name = "product_list"



    def get_queryset(self):
        queryset =  super().get_queryset()
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')

        if date:
            date = datetime.strptime(date, '%Y-%m-%d').date()
            queryset = queryset.filter(updated_at__date=date)

        if self.request.GET.get('title'):
            queryset = queryset.filter(title__contains=self.request.GET.get('title'))

        if price_from and price_to:
            queryset = queryset.filter(
                Q(productvariantprice__price__gte=price_from) &
                Q(productvariantprice__price__lte=price_to)
            )
        elif price_from:
            queryset = queryset.filter(productvariantprice__price__gte=price_from)
        elif price_to:
            queryset = queryset.filter(productvariantprice__price__lte=price_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['products_variants'] = ProductVariant.objects.values('variant_title')\
        .annotate(Count('id')).order_by().filter(id__count__gt=1)

        return context
    
        
