from backend.v1.api import endpoints as rest_endpoints
from core.application import create_app
from core.settings import settings

app = create_app()
app.include_router(rest_endpoints.api_router, prefix=f'{settings.BASE_URL}/v1')
