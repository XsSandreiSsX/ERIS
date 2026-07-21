import datetime
from typing import Annotated

from sqlalchemy import DateTime, text
from sqlalchemy.orm import mapped_column

IntPk = Annotated[int, mapped_column(primary_key=True)]

CreatedAt = Annotated[datetime.datetime, mapped_column(DateTime(timezone=True),
                                                       server_default=text("TIMEZONE('utc', now())"))]

UpdatedAt = Annotated[datetime.datetime, mapped_column(DateTime(timezone=True),
                                                       server_default=text("TIMEZONE('utc', now())"),
                                                       onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))]
