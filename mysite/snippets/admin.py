
from django.contrib import admin
from snippets.models import Snippet, Keyword

class SnippetAdmin(admin.ModelAdmin):
    fields = ['text', 'url']
    list_dispslay = ('text', 'url')


admin.site.register(Snippet, site=SnippetAdmin)
admin.site.register(Keyword, site=SnippetAdmin)

# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3

# class PollAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),

#     ]
#     inlines = [ChoiceInline]
#     list_display = ('question', 'pub_date', 'was_published_today')
#     list_filter = ['pub_date']
#     search_fields = ['question']
#     date_hierarchy = 'pub_date'

# admin.site.register(Poll, PollAdmin)

def make_singlecolumn(modeladmin, request, queryset):
    queryset.update(width='w0')
make_singlecolumn.short_description = "Change width to single column."

# class SnippetAdmin(admin.ModelAdmin):
#     fields = ['title', 'url', 'text', 'media', 'mediaType', 'date_added', 'last_viewed', 'width','height']
#     list_display = ('title', 'media', 'mediaType', 'url', 'width', 'height','date_added')
#     save_as = True
#     search_fields = ['title']
#     actions = [make_singlecolumn]

# class SnippetAdmin2(admin.ModelAdmin):
#     fields = ['title']
#     list_display = ('title')


