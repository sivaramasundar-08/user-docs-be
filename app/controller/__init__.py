from fastapi import FastAPI
from app.controller.user_docs_controller import user_router
from app.middleware.auth_middleware import AuthMiddleware


def create_public_app() -> FastAPI:
    pub_app = FastAPI()
    pub_app.add_middleware(AuthMiddleware)
    return pub_app


routes = [
    {
        "prefix": "",
        "router": user_router,
    }
]

public_app = create_public_app()
for route in routes:
    if route.get("prefix", "") != "":
        public_app.include_router(route.get("router"), prefix=route.get("prefix"))
    public_app.include_router(route.get("router"))


