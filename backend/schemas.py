from pydantic import BaseModel, ConfigDict, EmailStr, Field


class HealthStatus(BaseModel):
    status: str


class ErrorResponse(BaseModel):
    message: str


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str


class AuthResponse(BaseModel):
    token: str
    user: UserOut


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    name: str
    description: str
    price: float
    category: str
    stock: int
    image_url: str = Field(serialization_alias="imageUrl")


class CartItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    product_id: int = Field(serialization_alias="productId")
    quantity: int
    product: ProductOut


class CartOut(BaseModel):
    items: list[CartItemOut]
    total: float


class AddToCartRequest(BaseModel):
    product_id: int = Field(validation_alias="productId")
    quantity: int


class UpdateCartItemRequest(BaseModel):
    cart_item_id: int = Field(validation_alias="cartItemId")
    quantity: int


class RemoveFromCartRequest(BaseModel):
    cart_item_id: int = Field(validation_alias="cartItemId")


class FavoriteRequest(BaseModel):
    product_id: int = Field(validation_alias="productId")
