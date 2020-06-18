from django.contrib import admin
from mesaj.models import Mesaj
# Admin arayüzünde listelerken görğnecek alanlar, hangi alanlardan detaya girilebileceği,
# filtreleme kriterleri, arama çubuğu tanımları yapıldı
from haber.models import Haber


class MesajAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(name=request.user)

    list_display = ['id', 'name', 'title', 'date', 'email']

    list_display_links = ['title']

    list_filter = ['date', 'id']

    search_fields = ['title', 'name', 'content']

    class Meta:
        model = Mesaj


admin.site.register(Mesaj, MesajAdmin)

