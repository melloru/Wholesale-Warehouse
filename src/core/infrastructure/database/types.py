T = TypeVar("T")
TCreate = TypeVar("TCreate")
IdType = TypeVar("IdType", int, UUID, str)
AsyncSession = TypeVar("AsyncSession")

T = TypeVar("T", bound=Base)
TCreate = TypeVar("TCreate", bound=BaseModel)

SQLAlchemyModelType = TypeVar("SQLAlchemyModelType", bound=Base)
PydanticSchemaType = TypeVar("PydanticSchemaType", bound=BaseModel)