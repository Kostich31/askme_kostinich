from django.core.management.base import BaseCommand
from app.models import User, Tag, Like, Question, Answer
from faker import Faker
import random
from random import choice

class Command(BaseCommand):
    faker = Faker()

    def add_arguments(self, parser):
        parser.add_argument('--users')
        parser.add_argument('--tags')
        parser.add_argument('--question')
        parser.add_argument('--answer')
        

    def fill_users(self, count):
        last_user = User.objects.all().last()
        if last_user is None:
            last_id = 0
        else:
            last_id = last_user.id

        users = []
        for i in range(count):
            users.append(User(username=self.faker.user_name() + str(i)))
        User.objects.bulk_create(users, count)

    def fill_tags(self, count):
        tags = []
        for i in range(count):
            tags.append(Tag(name=self.faker.word() + str(i)))
        Tag.objects.bulk_create(tags, count)

    def fill_question(self, count):
        question = []
        all_users_id = list(
            User.objects.values_list(
                'id', flat=True
            )
        )

        for i in range(count):
            question.append(Question(author=User.objects.all().get(id=random.choice(all_users_id)),
                                     title=self.faker.sentence()[:30], text=self.faker.paragraph(nb_sentences=5),
                                     rating=random.randint(0, 1000)))
        Question.objects.bulk_create(question, count)

        question = Question.objects.all()
        all_tags = Tag.objects.all()
        for q in question:
            for i in range(random.randint(1, 3)):
                q.tags.add(random.choice(all_tags))

    def fill_answer(self, count):
        all_user_id = list(
            User.objects.values_list(
                'id', flat=True
            )
        )

        all_question_id = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        answer = []
        for i in range(count):
            answer.append(Answer(author=User.objects.all().get(id=random.choice(all_user_id)),
                                 what_question=Question.objects.all().get(id=random.choice(all_question_id)),
                                 text=self.faker.paragraph(nb_sentences=3),
                                 rating=random.randint(0, 1000)))
        Answer.objects.bulk_create(answer, count)

    def handle(self, *args, **options):
        if options['users']:
            self.fill_users(10)
        if options['tags']:
            self.fill_tags(20)
        if options['question']:
            self.fill_question(10)
        if options['answer']:
            self.fill_answer(300)
