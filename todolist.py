from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///todo.db?check_same_thread=False")

Base = declarative_base()

class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_task():
    new_row = Table(task=input("Enter task\n"),
             deadline=datetime.strptime(input("Enter deadline\n").split()[0], '%Y-%m-%d').date())
    session.add(new_row)
    session.commit()
    print("The task has been added!\n")

def todays_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all() # for accessing rows
    print("Today:")
    if len(rows) == 0:
        print("Nothing to do!\n")
        return
    for count, row in enumerate(rows):
        print(f"{count + 1}. {row}")
    print("")

def weeks_tasks():
    today = datetime.today() - timedelta(days=1)
    for _day in range(7):
        today += timedelta(days=1)
        rows = session.query(Table).filter(Table.deadline == today.date()).all() # for accessing rows
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        print(days_of_week[today.weekday()], today.day, today.strftime("%b"))
        if len(rows) == 0:
            print("Nothing to do!\n")
            continue
        for count, row in enumerate(rows):
            print(f"{count + 1}. {row}")
        print("")

def all_tasks():
    rows = session.query(Table.task, Table.deadline).order_by(Table.deadline).all()
    for count, row in enumerate(rows):
        print(f"{count + 1}. {row[0]}. {row[1].day} {row[1].strftime('%b')}.")
    print()

def delete_task():
    print("Choose the number of the task you want to delete:")
    all_tasks()
    rows = session.query(Table).all()
    specific_row = rows[int(input()) - 1]  # in case rows is not empty
    session.delete(specific_row)
    session.commit()
    print("The task has been deleted!\n")

def missed_tasks():
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    if len(rows) < 1:
        print("Nothing is missed!\n")
        return
    for count, row in enumerate(rows):
        print(f"{count + 1}. {row}")
    print()

def close():
    print("\nBye!")
    exit()

while True:
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    menu = input()
    if menu == "0":
        close()
    elif menu == "1":
        todays_tasks()
    elif menu == "2":
        weeks_tasks()
    elif menu == "3":
        all_tasks()
    elif menu == "4":
        missed_tasks()
    elif menu == "5":
        add_task()
    elif menu == "6":
        delete_task()