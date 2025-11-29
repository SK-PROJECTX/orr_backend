from django.contrib import admin

from .models import Availability, Calendar, Event, MeetingRequest


class EventInline(admin.TabularInline):
    model = Event
    extra = 0
    fields = ("title", "start", "end", "cancelled")
    readonly_fields = ("start", "end")


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner_user", "owner_org", "created_at")
    search_fields = ("name", "owner_user__username", "owner_org__name")
    list_filter = ("owner_org",)
    inlines = [EventInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "calendar",
        "start",
        "end",
        "created_by",
        "cancelled",
    )
    list_filter = ("cancelled", "calendar")
    search_fields = ("title", "description", "calendar__name", "created_by__username")
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("attendees",)


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner_user",
        "owner_org",
        "start",
        "end",
        "slot_length",
        "is_free",
    )
    search_fields = ("owner_user__username", "owner_org__name")
    list_filter = ("is_free", "owner_org")
    readonly_fields = ("created_at", "updated_at")


@admin.register(MeetingRequest)
class MeetingRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "requester",
        "calendar",
        "meeting_type",
        "status",
        "chosen_slot",
        "processed_by",
        "created_at",
    )
    search_fields = ("requester__username", "calendar__name", "agenda", "note")
    list_filter = ("meeting_type", "status", "calendar")
    readonly_fields = (
        "created_at",
        "updated_at",
        "processed_at",
        "cancelled_at",
    )
    autocomplete_fields = ("requester", "calendar", "processed_by", "event")
