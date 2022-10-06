from faker import Faker
fake = Faker(['it_IT', 'en_US', 'ja_JP'])
print("### ALL faker Attribute")
print(dir(fake))

profile = """
### Faker Profile ###
Name : {}
Email : {}
Social Security number (SSN) : {}
Address : {}
Location : {}, {}
URL : {}
""".format(fake.name(),
           fake.email(),
           fake.ssn(),
           fake.address(),
           fake.latitude(), fake.longitude(),
           fake.url()
            )

print(profile)
