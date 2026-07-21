from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.common.schemas import ErrorResponse
from app.core.http_exceptions import HttpException


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


async def http_exception_handler(request: Request, exc: HttpException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error_code=exc.error_code,
            detail=exc.detail,

        ).model_dump()
    )

app = FastAPI(
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HttpException, http_exception_handler)


from app.users.router import users_router
app.include_router(users_router,
                   prefix="/auth",
                   tags=["Auth"])

from app.products.router import product_router
app.include_router(product_router,
                   prefix="/products",
                   tags=["Products"])

from app.moderation.routers.role_application import role_application_router
app.include_router(role_application_router,
                   prefix="/role-applications",
                   tags=["Role Applications"])

from app.moderation.routers.moderator_role_application import moderator_role_application_router
app.include_router(moderator_role_application_router,
                   prefix="/admin/role-applications",
                   tags=["Role Applications"])

from app.sellers.routers.profile import profile_seller_router
app.include_router(profile_seller_router,
                   prefix="/sellers",
                   tags=["Sellers"])


@app.get("/ping")
async def ping():
    return {"status": "success", "message": "pong"}