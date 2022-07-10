from models import AddressBook, Record, Phone, Address, Email
import connect
from datetime import date


email1 = Email(email="e1@gmail.com")
email2 = Email(email="e2@gmail.com")
email3 = Email(email="e3@gmail.com")

phone1 = Phone(number="0956753318")
phone2 = Phone(number="0256753316")
phone3 = Phone(number="0656753334")

address1 = Address(address="Teatralna str")
address2 = Address(address="Prermohy str")
address3 = Address(address="Deputatska str")

user1 = Record(name="Marina", birthday=date(year=2001, month=11, day=5), phones=[phone1, phone2], emails=[email1], addresses=[address1, address2])
user2 = Record(name="Peter", phones=[phone3,], emails=[email2, email3], addresses=[address3,])
address_book = AddressBook(records=[user1, user2])

address_book.save()

books = AddressBook.objects

for book in books:
    for record in book.records:
        print(f"Name: {record.name}, Bday: {record.birthday}, Phones: {[x.number for x in record.phones]},\
            Emails: {[x.email for x in record.emails]}, Addresses: {[x.address for x in record.addresses]}")