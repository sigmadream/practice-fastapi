from database import SessionLocal
from user.infra.db_models.user import User
from datetime import datetime

with SessionLocal() as db:
    for i in range(50):
        user = User(
            id=f"UserId-{str(i).zfill(2)}",
            name=f"TestUser{i}",
            email=f"testUser{i}@app.com",
            password="qwer1234",
            memo=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(user)
    db.commit()
