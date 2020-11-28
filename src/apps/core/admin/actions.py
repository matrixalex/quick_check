def delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.safe_delete()
