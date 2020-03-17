from django.test import TestCase
from django.shortcuts import reverse
from .views import homepage,board_topics
from .models import Board
from django.urls import resolve
import pdb
# Create your tests here.


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url=reverse('homepage')
        response=self.client.get(url)
        self.assertEquals(response.status_code,200)

    def test_home_url_resolves_home_view(self):
        view=resolve('/')
        self.assertEquals(view.func,homepage)
        # pdb.set_trace()


class BoardTopicsTest(TestCase):
    def setUp(self):
        Board.objects.create(name='Django 3.0',description="Its a board about django you can discuss here")

    def test_board_topics_view_success_status_code(self):
        url=reverse("board_topics",kwargs={"pk":1})
        response=self.client.get(url)
        self.assertEquals(response.status_code,200)

    def test_board_topics_view_not_found_status_code(self):
        url=reverse("board_topics",kwargs={'pk':1})
        response=self.client.get(url)
        self.assertEquals(response.status_code,200)

    def test_board_topics_url_resolves_board_topics_view(self):
        view=resolve("/board/1/")
        self.assertEquals(view.func,board_topics)
