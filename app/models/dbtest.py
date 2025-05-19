from app.infrastructure.database import Base, engine

print("=====================")
Base.metadata.create_all(bind=engine)




