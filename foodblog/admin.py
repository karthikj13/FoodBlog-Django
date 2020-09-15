from django.contrib import admin
from .models import Food, Comment

class FoodAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'publish', 'status')
    list_filter = ('status','created','publish','author')
    search_fields = ('title','desc')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status','publish']

admin.site.register(Food, FoodAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'food', 'created', 'active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')

admin.site.register(Comment, CommentAdmin)