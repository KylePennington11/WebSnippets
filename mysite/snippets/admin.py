from snippets.models import Snippet,Keyword,SnippetKeywordLink
from django.contrib import admin

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

class SnippetAdmin(admin.ModelAdmin):
    fields = ['title', 'url', 'text', 'image', 'date_added', 'last_viewed']
    list_display = ('title', 'image', 'url', 'date_added')

admin.site.register(Snippet, SnippetAdmin)