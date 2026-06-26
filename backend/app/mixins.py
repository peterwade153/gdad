from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status


class FamilyTreeCacheMixin:
    """
    Mixin to intercept incoming requests, checking the cache backend 
    before allowing the view to compile data.
    """

    cache_prefix = "family_tree"
    cache_timeout = 86400 # 24 hours

    def get_cache_key(self, request, *args, **kwargs):
        identity_number = kwargs.get("identity_number")
        view_name = self.__class__.__name__.lower()
        if view_name == 'personfamilytreelistview':
            max_gen = request.GET.get("max_generation", "10")
            return f"{self.cache_prefix}_person_{identity_number}_gen_{max_gen}"
        return f"{self.cache_prefix}_person_{identity_number}"

    def serve_cached_payload(self, request, *args, **kwargs):
        """
        Executes instead of the view's get(), when a cache entry is present.
        """
        return Response(
            self._cached_payload_data, 
            status=status.HTTP_200_OK, 
            headers={"X-Gdaddy-Api-Cache": "HIT"}
        )
    
    def initial(self, request, *args, **kwargs):
        """
        Runs AFTER DRF sets up headers and query_params, but BEFORE get() is called.
        """
        super().initial(request, *args, **kwargs)
        
        self.cache_key = self.get_cache_key(request, **kwargs)
        cached_data = cache.get(self.cache_key)
        
        if cached_data is not None:
            # --- CACHE HIT ---
            self._cached_payload_data = cached_data
            self.get = self.serve_cached_payload
        else:
            self._cached_payload_data = None
    
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        # If it's a successful fresh response, cache it
        if response.status_code == 200 and not response.has_header('X-DRF-Cache'):
            cache.set(self.cache_key, response.data, timeout=self.cache_timeout)
            response.headers["X-DRF-Cache"] = "MISS"
        return response
