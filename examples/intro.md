# Requirements
Loglan-Core is only a __data model__, a wrapper, and does not contain the dictionary data itself.
To work with a dictionary as an ORM, you need to set up your own database locally or remotely.

You can connect it as follows:
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URI = os.environ.get('LOD_DATABASE_URL')
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine, future=True))
session = Session()
```
where `LOD_DATABASE_URL` is the database URI starting with `postgresql://***`.

Next, we will use the resulting instance of the `Session` class to retrieve data from the database and work with it.
