from fastapi import Depends, FastAPI, HTTPException

from app.db import User, create_db_and_tables
from app.schemas import UserCreate, UserRead, UserUpdate, PredictData
from app.users import auth_backend, current_active_user, fastapi_users
from app.model import k_neighbors_classification_model, \
    mlp_classification_model, \
    embed_bert_cls, categories

from transformers import AutoTokenizer, AutoModel


tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
model = AutoModel.from_pretrained("cointegrated/rubert-tiny")

app = FastAPI()

classifiers = {
    "k_neighbors": {
        "classifier": k_neighbors_classification_model.create_model(),
        "price": k_neighbors_classification_model.get_price()
    },
    "mlp": {
        "classifier": mlp_classification_model.create_model(),
        "price": mlp_classification_model.get_price()
    }
}

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.get("/balance")
async def get_balance(user: User = Depends(current_active_user)):
    return {"balance": user.credits}


@app.get("/predict")
async def predict_category_k_neighbors(predict_data: PredictData, user: User = Depends(current_active_user)):
    classifier = classifiers[predict_data.classifier_name]
    print(predict_data.classifier_name, classifier["price"])
    new_user_balance = predict_data.user_balance - classifier["price"]
    if new_user_balance < 0:
        raise HTTPException(status_code=404, detail="Недостаточно средств")

    product_name_vec = embed_bert_cls(predict_data.product_name, model, tokenizer)
    category = classifier["classifier"].predict(product_name_vec.reshape(1, -1))[0]
    return {"category": categories[category], "balance": new_user_balance}


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
