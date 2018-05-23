

class Person:
    numberOfPerson = 0 # Person 이라는 객체가 만들어질 때 마다 몇개인지 카운트 하기 위한 변수
    name= ''
    
    def __init__(self): # 생성자
        self.name = 'noname'
        Person.numberOfPerson += 1
    
    def __del__(self): # 소멸자
        Person.numberOfPerson -= 1
        

    def setName(self,name): # 항상 self가 들어가야함, 인스턴스 변수접근할때에는 항상 self로 접근할것
        if len(name) > 2:
            self.name = name
        else:
            print('이름은 3글자 이상 입력해야 함')
            
    def getName(self):
        return ':D' + self.name + '-_-'


# 교수


class Professor(Person):
    numberOfProfessor = 0

    def __init__(self, name=''):
        self.name = name
        self.subjects = [] # 빈리스트
        Person.numberOfPerson += 1
        Professor.numberOfProfessor += 1

    def __del__(self):
        Person.numberOfPerson -= 1
        Professor.numberOfProfessor -= 1

    def addSubjects(self,subject):
        self.subjects.append(subject)
    
    def getSubjects(self,index):
        return self.subjects[index]


# 학생

class Student(Person):
    numberOfStudent = 0
    # subejctAndGrade = {}
    
    def __init__(self, name=''):
        self.name = name
        self.subjectAndGrade = {}
        Person.numberOfPerson += 1
        Student.numberOfStudent += 1

    def __del__(self):
        Person.numberOfPerson -= 1
        Student.numberOfStudent -= 1
    
    def setSubjectAndGrade(self, subject, grade):
        self.subjectAndGrade[subject] = grade # 딕셔너리 추가함
        
    def getSubjects(self):
        return list(self.subjectAndGrade.keys())

    def getGrade(self, subject):
        return self.subjectAndGrade[subject]


def showHello(name='noname', title='이름없는'):
    print('환영합니다. 낯선이여 %s %s' % (title,name))