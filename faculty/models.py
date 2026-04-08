from django.db import models


# Create your models here.

# Create table facultydetails (
#facultyid int,
#facultyname varchar(100),
#facultyage int,
#acultyresearch text)

# When the class is defined and a primary key feild is undefined django will create a new coumn called id
# and assign it as the primary key

#To push the changes to the database execute the following commands in the terminal
# python manage.py makemigrations
# python manage.py migrate

#When django creates the table from the class, the name of the table will have the following structure:
# appname_classname 
class StudentDetails(models.Model):
    studentid = models.IntegerField(primary_key=True)
    firstname = models.TextField(max_length=100)
    lastname = models.TextField(max_length=100)
    major = models.TextField()
    year = models.TextField()
    gpa = models.FloatField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class BookDetails(models.Model):
    bookid = models.IntegerField(primary_key=True)
    bookname = models.TextField(max_length=100)
    authorname = models.TextField(max_length=100)
    currentlycheckedout = models.BooleanField(default=False)
    numberoftimescheckedout = models.IntegerField()
    
    def __str__(self):
        return self.bookname


class BookReservation(models.Model):
    studentid = models.ForeignKey(StudentDetails, on_delete=models.CASCADE)
    firstname = models.TextField(max_length=100)  # Make sure this exists
    lastname = models.TextField(max_length=100)  # Make sure this exists
    bookname = models.TextField(max_length=100)
    bookid = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.studentid.firstname} reserved {self.bookid.bookname}"
