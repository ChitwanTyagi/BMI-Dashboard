from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
DATABASE_URL = "sqlite:///./bmi_calculator.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BMIRecord(Base):
    __tablename__ = "bmi_records"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    weight_kg = Column(Float)
    height_meters = Column(Float)
    bmi_value = Column(Float)
    category = Column(String)

Base.metadata.create_all(bind=engine)
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

class UserInfo(BaseModel):
    name: str
    age: int
    weight_kg: float
    weight_unit: str
    height_meters: float
    height_unit: str
    consent: bool = True

@app.get("/", response_class=HTMLResponse)
def read_root():
    return FileResponse("index.html")

@app.get("/favicon.ico")
def get_favicon():
    return FileResponse("favicon.ico")

@app.post("/calculate_bmi")
def calculate_bmi(user_info: UserInfo, db: Session = Depends(get_db)):
    #1. Normalize Weight to true kg
    actual_kg = user_info.weight_kg
    if user_info.weight_unit == "lbs":
        actual_kg = user_info.weight_kg * 0.453592
    #2. Normalize Height to true meters
    actual_m = user_info.height_meters   
    if user_info.height_unit == "cm":
        actual_m = user_info.height_meters * 0.01
    elif user_info.height_unit == "in":
        actual_m = user_info.height_meters * 0.0254
    elif user_info.height_unit == "ft":
        actual_m = user_info.height_meters * 0.3048
    #3. Calculate BMI
    bmi_value = actual_kg / (actual_m ** 2)
    rounded_bmi = round(bmi_value, 2)
    # Determine BMI category
    if rounded_bmi < 18.5:
        category = "Underweight"
        diet_plan = "Focus on a healthy caloric surplus. Prioytize clean complex carbohydrates, lean proteins, and healthy fats. Consider consulting a nutritionist for personalized advice. Do Better Please!!!!"
    elif 18.5 <= rounded_bmi < 25:
        category = "Normal weight"
        diet_plan = "Maintain a balanced approach. Maintain an equal proportion of lean protiens, high-fiber veggies, and whole grains. Doing great Bravv Keep Supporting good deeds for urself!!!!"
    elif 25 <= rounded_bmi < 30:
        category = "Overweight"
        diet_plan = "Aim for a moderte, controlled caloric deficit. Increase lean proteins intake and scale back on refined sugars. Littebit here and there will do the trick. You got this!!!!"
    else:
        category = "Obese"
        diet_plan = "Structured caloric management. Focus heavy on lean proteins, high -volume foods like veggies, and whole grains. AND hit the gym BRavvv!!!!"

    # Create and save the BMI record
    if user_info.consent:
        new_db_record = BMIRecord(
            name=user_info.name,
            age=user_info.age,
            weight_kg=actual_kg,
            height_meters=actual_m,
            bmi_value=rounded_bmi,
            category=category,
        )
        db.add(new_db_record)
        #print("Incoming data:", user_info)
        db.commit()
        db.refresh(new_db_record)

    return {
        "name": user_info.name,
        "calculated_bmi": rounded_bmi,
        "category": category,
        "diet_plan": diet_plan,
    }
