def settings(request):
    """
    Add settings (or some) to the templates
    """
    from django.conf import settings

    tags = {}
    tags["GOOGLE_MAPS_KEY"] = settings.GOOGLE_MAPS_KEY
    tags["GOOGLE_ANALYTICS_ENABLED"] = getattr(
        settings, "GOOGLE_ANALYTICS_ENABLED", True
    )
    tags["MAP_PROVIDER"] = settings.MAP_PROVIDER
    if hasattr(settings, "GOOGLE_ANALYTICS_KEY"):
        tags["GOOGLE_ANALYTICS_KEY"] = settings.GOOGLE_ANALYTICS_KEY
    return tags
