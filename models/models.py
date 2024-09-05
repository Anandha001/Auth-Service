from datetime import datetime, timezone
from sqlalchemy import (
    UUID,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    text,
    LargeBinary,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, mapped_column
from uuid import uuid4
import bcrypt

CASCADE = "CASCADE"


class Base(DeclarativeBase):
    pass


class Organisation(Base):
    __tablename__ = "organisation"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    name = mapped_column(String, nullable=False, unique=True)
    status = mapped_column(Integer, default=0, nullable=False)
    personal = mapped_column(Boolean, default=False, nullable=True)
    settings = mapped_column(
        JSONB,
        default=text("'{}'::jsonb"),
        server_default=text("'{}'::jsonb"),
        nullable=True,
    )

    created_at = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at = mapped_column(DateTime, onupdate=datetime.now(timezone.utc))


class User(Base):
    __tablename__ = "user"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    email = mapped_column(String, nullable=False, unique=True)
    password = mapped_column(LargeBinary, nullable=False)
    profile = mapped_column(
        JSONB,
        default=text("'{}'::jsonb"),
        server_default=text("'{}'::jsonb"),
        nullable=False,
    )
    status = mapped_column(Integer, default=0, nullable=False)
    settings = mapped_column(
        JSONB,
        default=text("'{}'::jsonb"),
        server_default=text("'{}'::jsonb"),
        nullable=True,
    )

    created_at = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at = mapped_column(DateTime, onupdate=datetime.now(timezone.utc))

    def hash_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(14))
        print(self.password)

    def verify_password(self, password):
        if bcrypt.checkpw(password.encode("utf-8"), self.password):
            return True
        else:
            return False


class Role(Base):
    __tablename__ = "role"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    name = mapped_column(String, nullable=False, unique=True)
    description = mapped_column(String, nullable=True)
    org_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(Organisation.uuid, ondelete=CASCADE),
        nullable=False,
    )


class Member(Base):
    __tablename__ = "member"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    org_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(Organisation.uuid, ondelete=CASCADE),
        nullable=False,
    )
    user_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey(User.uuid, ondelete=CASCADE), nullable=False
    )
    role_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey(Role.uuid, ondelete=CASCADE), nullable=False
    )
    status = mapped_column(Integer, default=0, nullable=False)
    settings = mapped_column(
        JSONB,
        default=text("'{}'::jsonb"),
        server_default=text("'{}'::jsonb"),
        nullable=True,
    )

    created_at = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at = mapped_column(DateTime, onupdate=datetime.now(timezone.utc))
