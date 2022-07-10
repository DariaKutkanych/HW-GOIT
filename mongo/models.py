from datetime import datetime
from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import DateTimeField, EmbeddedDocumentField, ListField, StringField


class Phone(EmbeddedDocument):
    number = StringField(min_length=10)

class Email(EmbeddedDocument):
    email = StringField(max_length=50)

class Address(EmbeddedDocument):
    address = StringField(max_length=50)


class Record(EmbeddedDocument):
    name = StringField(max_length=50)
    birthday = DateTimeField()
    phones = ListField(EmbeddedDocumentField(Phone))
    addresses = ListField(EmbeddedDocumentField(Address))
    emails = ListField(EmbeddedDocumentField(Email))
    meta = {'allow_inheritance': True}

class AddressBook(Document):
    records = ListField(EmbeddedDocumentField(Record))
    meta = {'allow_inheritance': True}
