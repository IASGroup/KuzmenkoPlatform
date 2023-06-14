import peewee
from .database import db

class Article(peewee.Model):
    uri = peewee.TextField(primary_key=True)
    page = peewee.IntegerField(null=True)
    theme_uri = peewee.TextField(null=True)
    theme_name = peewee.TextField(null=True)
    title = peewee.TextField(null=True)
    authors = peewee.TextField(null=True)
    journal = peewee.TextField(null=True)
    keywords = peewee.TextField(null=True)
    description = peewee.TextField(null=True)
    content = peewee.TextField(null=True)

    class Meta:
        database = db
        db_table = 'articles'

class ParseTask(peewee.Model):
    id = peewee.UUIDField(primary_key=True)
    theme_uri = peewee.TextField()
    theme_name = peewee.TextField()
    from_page = peewee.IntegerField()
    to_page = peewee.IntegerField()
    is_done = peewee.BooleanField(default=False)
    last_parsed_page = peewee.IntegerField()

    class Meta:
        database = db
        db_table = 'parse_tasks'