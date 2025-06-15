from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ChoicesMixin:
    """
    Mixin untuk menambahkan endpoint choices yang mengekspos model choices ke frontend.
    
    Cara pakai:
    1. Tambahkan mixin ke ViewSet
    2. Definisikan choices_config di ViewSet dengan format:
       {
           'field_name': {
               'choices': choices_data,
               'description': 'Deskripsi untuk field ini'
           }
       }
    """
    
    choices_config = None
    
    def get_choices_data(self):
        """Override method ini jika perlu kustomisasi format choices"""
        if not self.choices_config:
            raise NotImplementedError("choices_config harus didefinisikan di ViewSet")
            
        result = {}
        for field_name, config in self.choices_config.items():
            result[field_name] = [
                {"value": value, "label": label}
                for value, label in config['choices']
            ]
        return result
    
    def get_choices_schema(self):
        """Generate schema untuk Swagger documentation"""
        if not self.choices_config:
            return openapi.Schema(type=openapi.TYPE_OBJECT)
            
        properties = {}
        for field_name, config in self.choices_config.items():
            properties[field_name] = openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'value': openapi.Schema(type=openapi.TYPE_STRING, description='Kode pilihan'),
                        'label': openapi.Schema(type=openapi.TYPE_STRING, description='Label pilihan')
                    }
                ),
                description=config.get('description', '')
            )
        return openapi.Schema(type=openapi.TYPE_OBJECT, properties=properties)
    
    @swagger_auto_schema(
        operation_description="Mendapatkan pilihan yang tersedia",
        responses={
            200: openapi.Response(
                description="Daftar pilihan yang tersedia",
                schema=openapi.Schema(type=openapi.TYPE_OBJECT)  # Placeholder schema
            )
        },
        paginator_inspectors=[],
        filter_backends=[],
        search_fields=None,
        ordering_fields=None
    )
    @action(detail=False, methods=['get'])
    def choices(self, request):
        """
        Mendapatkan pilihan yang tersedia.
        """
        choices = self.get_choices_data()
        return Response(choices)
    
    def get_swagger_auto_schema(self):
        """Override method ini untuk kustomisasi schema Swagger"""
        return swagger_auto_schema(
            operation_description="Mendapatkan pilihan yang tersedia",
            responses={
                200: openapi.Response(
                    description="Daftar pilihan yang tersedia",
                    schema=self.get_choices_schema()
                )
            },
            paginator_inspectors=[],
            filter_backends=[],
            search_fields=None,
            ordering_fields=None
        )