CREATE TABLE Gender (
    id SERIAL PRIMARY KEY,
    name TEXT
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
    weight INTEGER,
    activity NUMERIC
);
CREATE TABLE Food_diaries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users,
    diarydate DATE NOT NULL DEFAULT CURRENT_DATE,
    calorie_intake INTEGER,
    use_of_energy INTEGER
);
CREATE TABLE Meals (
    id SERIAL PRIMARY KEY,
    name TEXT
);
CREATE TABLE Foodstuffs (
    id SERIAL PRIMARY KEY,
    name TEXT,
    calories INTEGER,
    fat INTEGER,
    carbs INTEGER,
    protein INTEGER,
    fiber INTEGER
);
CREATE TABLE Portions (
    id SERIAL PRIMARY KEY,
    diary_id INTEGER REFERENCES Food_diaries,
    foodstuff_id INTEGER REFERENCES Foodstuffs,
    meal_id INTEGER REFERENCES Meals,
    amount INTEGER
);
