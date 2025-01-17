from datetime import datetime
from typing import Annotated, Dict, List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from containers import Container
from user.application.user_service import UserService
from user.domain.user import User

router = APIRouter(prefix="/users")


class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


@router.post("", status_code=201, response_model=UserResponse)
@inject
def create_user(user: CreateUserBody,
                user_service: UserService = Depends(Provide[Container.user_service])):
    created_user = user_service.create_user(
        name=user.name, email=user.email, password=user.password
    )
    return created_user


class UpdateUser(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)


@router.put("/{user_id}")
@inject
def update_user(
        user_id: str,
        user: UpdateUser,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    user = user_service.update_user(
        user_id=user_id,
        name=user.name,
        password=user.password,
    )
    return user


class GetUsersResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]


@router.get("")
@inject
def get_users(
        page: int = 1,
        items_per_page: int = 10,
        user_service: UserService = Depends(Provide[Container.user_service]),
) -> dict[str, int | list[User]]:
    total_count, users = user_service.get_users(page, items_per_page)
    return {
        "total_count": total_count,
        "page": page,
        "users": users,
    }


@router.delete("", status_code=204)
@inject
def delete_user(
        user_id: str,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    user_service.delete_user(user_id)


@router.post("/login")
@inject
def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    print(form_data.username, form_data.password)
    access_token = user_service.login(
        email=form_data.username,
        password=form_data.password,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
