from django.contrib import admin

from .models import Category, Choice, Comment, Question

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    
    
class ChoiceInline(admin.StackedInline):
    model = Choice
    

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'question_text',
        'published_date',
        'category',
    ]
    
    date_hierarchy = 'published_date'
    inlines = [ChoiceInline]
    list_filter = ['published_date', 'category']
    ordering = ['published_date']
    search_fields = ['question_text']
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','text','created_at']
    list_filter = ['created_at','user']
    search_fields = ['text']
    date_hierarchy = 'created_at'
    ordering = ['created_at']
    