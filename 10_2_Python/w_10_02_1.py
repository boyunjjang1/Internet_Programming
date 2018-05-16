# import mymodule

from mymodule import *

# mymodule.showHello('강보윤')
# mymodule.showHello(title='거지같은')
# showHello(name = '강보윤',title='귀여운')






# -------------------------------------------------

# print(Person.numberOfPerson) # 처음에 몇개인지 출력

# o1 = Person()
# o1.setName('강보윤')
# print(o1.getName())
# print(o1.name)
# print(Person.numberOfPerson, o1.numberOfPerson)

# o2 = Person()
# print(Person.numberOfPerson, o1.numberOfPerson)

# o2 = [] # 날림
# print(Person.numberOfPerson, o1.numberOfPerson)

# del(o1)
# print(Person.numberOfPerson)

# 교수 목록

print(Person.numberOfPerson, Professor.numberOfProfessor)
p1 = Professor()
p1.setName('교수1')
p1.addSubjects('인프1')
p1.addSubjects('인프2')

print(Person.numberOfPerson, Professor.numberOfProfessor)
p2 = Professor()
p2.setName('교수2')
p2.addSubjects('웹프1')
p2.addSubjects('웹프2')

print(Person.numberOfPerson, Professor.numberOfProfessor)
print(p1.name, p1.getName(), p1.subjects)
print(p2.name, p2.getName(), p2.subjects)


# 학생 목록


print(Person.numberOfPerson)

s1 = Student('학생1')
s1.setSubjectAndGrade('인프1','A+')
s1.setSubjectAndGrade('인프2','A+')

print(Person.numberOfPerson, Student.numberOfStudent)
s2 = Student('학생2')
s2.setSubjectAndGrade('웹프1','A+')
s2.setSubjectAndGrade('웹프2','A+')

print(s1.name,s1.getName(),s1.subjectAndGrade)
print(s2.name,s2.getName(),s2.subjectAndGrade)

print(Person.numberOfPerson)