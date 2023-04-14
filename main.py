from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dataBase import engine
from router import branch, admin_auth, product, user, user_auth

app = FastAPI()

# Base.metadata.create_all(bind=engine)

app.include_router(admin_auth.router)

app.include_router(user_auth.router)

app.include_router(user.router)

app.include_router(branch.router)

app.include_router(product.router)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)