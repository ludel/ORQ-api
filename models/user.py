from notaorm.datatype import Int, Varchar
from notaorm.table import Table

User = Table('user', rows=(
    Int('id', primary_key=True, not_null=True),
    Varchar('email', length=255, unique=True, not_null=True),
    Varchar('password', not_null=True),
    Varchar('watchlist'),
    Varchar('token', not_null=True),
))
