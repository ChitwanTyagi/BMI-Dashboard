BMI DASHBOARD & dATA PIPELINE
A Full-stack web application designed to calculate Body Mass Index(BMI) and provide health-conscious feedback, featuring a custom Python/FastApi backend and an SQLite database for persistent, privacy-focused data storage.

TECH STACK
~ Backend : Python, FastAPI, SQLALchemy
~ Database : SQLite
~ Frontend : Vanilla JAvASCRIPT, Tailwind CSS, HTML5
~ Version Control: Git/GitHub

KEY FEATURES
~ Custom API Architecture: Built a FastAPi bacekend to handle POST requests and perform backend calculations, ensuring separation between logic and UI.
~ Privacy-First Design: Implemented a user-consent flag that allows users to opt-in to database storage. If unchecked, the server discards the record after calculation.
~ Persistent Storage: Used SQLALchemy ORM to manage SQLite database transactions, ensuring reliable data logging.
Dynamic Frontend: Rsponsive UI using Tailwind CSS with real time DOM manipulation based on backend responses.

CHALLENGES OVERCOME
~ JSON Serialisation: Debugged complex nested payload mismatches between the server and the frontend client.
~ Scope Management: Resolved Python scope-level syntax errors by restructuring route decorators and function control flow.
~ State Management: Utilized localstorage to bridge data persistence gaps during pages refreshes, improving the user experience.

FUTURE SCOPE
integrating data visualisation libraries(like Chart.js) to provide users with historical BMI trends based on their stored data-an essential next step for my focus on Statistics for Data Science