


#instance == object

#method = classㅇㅏㄴ에 있는 func
#constructor = 처음 선언

class Employee:
    salary_raise_per = 1.04

    def __init__(self, first, last, salary):
        self.first = first
        self.last = last
        self.salary = salary

    def show_name(self):
        return self.first + ' ' + self.last

    def salary_raise(self):
        self.salary *= self.salary_raise_per

david = Employee('david', 'jeon', 10000)
angie = Employee('angie', 'kim', 1000000)
jiwon = Employee('jiwon', 'shim', 100000000)

print(david.salary)
print(david.salary_raise())
print(david.salary)