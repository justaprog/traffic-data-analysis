from sqlalchemy import create_engine,text, MetaData
from dotenv import load_dotenv
import os 

# load .env
dotenv_path = os.path.join(os.path.dirname(__file__), '../../../.env')
load_dotenv(dotenv_path)

db_url = os.environ["DATABASE_URL"]
# print(db_url)
# create db engine
engine = create_engine(db_url, echo=True)