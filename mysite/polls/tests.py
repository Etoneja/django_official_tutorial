from datetime import timedelta

from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text, days_offset):
    pub_date = timezone.now() + timedelta(days=days_offset)
    return Question.objects.create(
        question_text=question_text, pub_date=pub_date
    )


class QuestionModelText(TestCase):

    def test_was_published_recently_with_future_question(self):

        future_question = create_question("test", 1)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):

        future_question = create_question("test", -2)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_default_pub_date_question(self):

        future_question = Question(
            question_text="test_text"
        )
        self.assertIs(future_question.was_published_recently(), True)

    def test_was_published_recently_with_recent_question(self):

        pub_date = timezone.now() + timedelta(hours=-2)
        future_question = Question(
            question_text="test_text",
            pub_date=pub_date
        )
        self.assertIs(future_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):

    url_index = reverse("polls:index")

    def test_no_question(self):
        response = self.client.get(self.url_index)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No questions")
        self.assertTemplateUsed(response, "polls/index.html")
        self.assertQuerysetEqual(
            response.context["question_list"], []
        )

    def test_future_question(self):

        create_question("past", 2)

        response = self.client.get(self.url_index)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No questions")
        self.assertQuerysetEqual(
            response.context["question_list"], []
        )

    def test_past_question(self):

        create_question("past", -2)

        response = self.client.get(self.url_index)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No questions")
        self.assertQuerysetEqual(
            response.context["question_list"], ["<Question: 1 - past>"]
        )

    def test_past_and_future_questions(self):

        create_question("past", -2)
        create_question("past", 2)

        response = self.client.get(self.url_index)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No questions")
        self.assertQuerysetEqual(
            response.context["question_list"], ["<Question: 1 - past>"]
        )

    def test_two_past_questions(self):

        create_question("past 1", -2)
        create_question("past 2", -1)

        response = self.client.get(self.url_index)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No questions")
        self.assertQuerysetEqual(
            response.context["question_list"], [
                "<Question: 2 - past 2>",
                "<Question: 1 - past 1>",
            ]
        )


class QuestionDetailsViewTest(TestCase):

    def test_future_question(self):
        future_question = create_question("future", 1)
        url = reverse("polls:details", args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_question_with_no_answers(self):
        question = create_question("test", -2)
        url = reverse("polls:details", args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No answers for question")
        self.assertContains(response, "test")
        self.assertEqual(
            response.context["question"], question
        )

    def test_question_with_answer(self):
        question = create_question("test question", -2)
        question.answer_set.create(choice_text="test answer")
        url = reverse("polls:details", args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No answers for question")
        self.assertContains(response, "test question")
        self.assertContains(response, "test answer")
        self.assertEqual(
            response.context["question"], question
        )


class QuestionResultsViewTest(TestCase):

    def test_future_question(self):
        future_question = create_question("future", 1)
        url = reverse("polls:results", args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_question_with_no_answers(self):
        question = create_question("test", -2)
        url = reverse("polls:results", args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No answers")
        self.assertContains(response, "test")
        self.assertEqual(
            response.context["question"], question
        )
