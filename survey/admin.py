from django.contrib import admin
from .models import Post, Withdraw, Deposit, Comment2

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')

@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('done','author','name', 'credit')

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('done','author','name', 'credit')

@admin.register(Comment2)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author','message', 'done')
