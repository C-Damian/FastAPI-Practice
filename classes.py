class person:
  def __init__(self, name, age, job):
    self.name = name
    self.age = age
    self.job = job

  def __str__(self):
    return f"{self.name} is {self.age} years old and works as a {self.job}."

  def __repr__(self):
    return "test repr"

  def get_older(self):
    self.age += 1

p1 = person("alice", 30, "engineer")

print(p1.name)
print(p1.age)
print(p1.job) 

p1.get_older()
print(p1.age)
print(p1)
