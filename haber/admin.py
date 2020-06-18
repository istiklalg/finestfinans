from django.contrib import admin
from haber.models import Haber
# Register your models here.


class HaberAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'konum', 'position', 'link']

    list_display_links = ['title']

    list_filter = ['id', 'title', 'konum', 'position', 'publishing_date', 'link']

    list_editable = ['konum', 'position', 'link']

    search_fields = ['title', 'content', 'link']

    class Meta:
        model = Haber


admin.site.register(Haber, HaberAdmin)
