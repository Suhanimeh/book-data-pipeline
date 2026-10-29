
# Student Name: Ruchita Jain

# Student ID: ET21BTAI022

# Course: Web Programming

# Program: Third Year B.Tech (AI & DS)

# Semester: 6

# Group: 15 
#  Academic Declaration:
#  I declare that this assignment is my own work and has been completed
#  in accordance with Sarvajanik University's Academic Policy. No part
#  of this assignment has been copied manually or electronically from
#  any other source, including websites, or distributed to other students
#  without authorization.
 
#  Acknowledgement:
#  I sincerely thank my professor for providing guidance, support, and
#  valuable feedback throughout this project. Their encouragement and
#  assistance helped us understand the concepts and complete this project
#  successfully.from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/books"
    scrape_base_url: str = "https://books.toscrape.com/"
    scrape_max_pages: int = 5          # 20 books per page
    request_delay: float = 0.3         # seconds between requests (be polite)
    cors_origins: str = "*"            # comma-separated list
    auto_seed: bool = True             # run the pipeline on startup if the DB is empty


settings = Settings()
