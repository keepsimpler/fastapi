#%%
from app.db import base
from app.db.session import engine
# %%
if __name__ == "__main__":
    base.Base.metadata.create_all(engine)
# %%
