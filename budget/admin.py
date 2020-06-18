from django.contrib import admin

from budget.models import Budget
# Admin arayüzünde listelerken görünecek alanlar, hangi alanlardan detaya girilebileceği,
# filtreleme kriterleri, arama çubuğu tanımları yapıldı


class BudgetAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    list_display = ['tax_title', 'grup_ismi', 'tax_number', 'user', 'saving_date', 'period']

    list_display_links = ['tax_title', 'tax_number']

    list_filter = ['saving_date', 'tax_title', 'grup_ismi', 'period']

    search_fields = ['tax_title', 'tax_number', 'grup_ismi', 'period']

    list_per_page = 25

    class Meta:
        model = Budget


admin.site.register(Budget, BudgetAdmin)



