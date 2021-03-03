CREATE TABLE Gender (
    id SERIAL PRIMARY KEY,
    gender TEXT
);
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE Personal_details (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users,
    name TEXT,
    gender_id INTEGER REFERENCES Gender,
    age INTEGER,
    height INTEGER,
    weight DECIMAL,
    activity DECIMAL,
    calorie_goal INTEGER
);
CREATE TABLE Food_diaries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users,
    date DATE NOT NULL DEFAULT CURRENT_DATE
);
CREATE TABLE Meals (
    id SERIAL PRIMARY KEY,
    name TEXT
);
CREATE TABLE Foodstuffs (
    id SERIAL PRIMARY KEY,
    name TEXT,
    calories INTEGER,
    fat DECIMAL,
    carbs DECIMAL,
    protein DECIMAL,
    fiber DECIMAL,
    added_by INTEGER REFERENCES Users,
    visible BOOLEAN
);
CREATE TABLE Portions (
    id SERIAL PRIMARY KEY,
    diary_id INTEGER REFERENCES Food_diaries,
    foodstuff_id INTEGER REFERENCES Foodstuffs,
    meal_id INTEGER REFERENCES Meals,
    amount INTEGER
);
