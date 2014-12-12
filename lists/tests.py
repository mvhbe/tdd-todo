from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from lists.models import Item
from lists.views import home_page


# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_geeft_correct_html_terug(self):
        request = HttpRequest()
        expected_html = render_to_string("home.html")

        response = home_page(request)

        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST["item_text"] = 'A new list item'

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, 'A new list item')

    def test_home_page_redirects_after_post(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST["item_text"] = 'A new list item'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

    def testHomePageOnlySavesItemsWhenNecessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):

    def testSavingAndRetrievingItems(self):
        firstItem = Item()
        firstItem.text = "The first (ever) list item"
        firstItem.save()

        SecondItem = Item()
        SecondItem.text = "Item the second"
        SecondItem.save()

        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(), 2)

        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]
        self.assertEqual(firstSavedItem.text, "The first (ever) list item")
        self.assertEqual(secondSavedItem.text, "Item the second")
