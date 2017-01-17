def media_root(request):
  from django.conf import settings
  return {'media_root': settings.MEDIA_ROOT}

