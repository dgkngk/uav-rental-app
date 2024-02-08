from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UAV, Rental
from .views import home_view, rent_uav, return_uav, update_rental, profile_view

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.uav = UAV.objects.create(brand='TestBrand', model='TestModel', weight=10.0, category='TestCategory')

    # Test success cases for each view
    def test_home_view_success(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_rent_uav_success(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('rent_uav', kwargs={'uav_id': self.uav.id}), {'start_date': '2023-01-01', 'end_date': '2023-01-10'})
        self.assertEqual(response.status_code, 302)  # Assuming successful redirection after renting

    def test_return_uav_success(self):
        self.client.login(username='testuser', password='password')
        rental = Rental.objects.create(user=self.user, uav=self.uav, rental_start='2023-01-01', rental_end='2023-01-10', is_active=True)
        response = self.client.post(reverse('return_uav', kwargs={'rental_id': rental.id}))
        self.assertEqual(response.status_code, 302)  # Assuming successful redirection after returning UAV

    def test_update_rental_success(self):
        self.client.login(username='testuser', password='password')
        rental = Rental.objects.create(user=self.user, uav=self.uav, rental_start='2023-01-01', rental_end='2023-01-10', is_active=True)
        response = self.client.post(reverse('update_rental', kwargs={'rental_id': rental.id}), {'start_date': '2023-01-02', 'end_date': '2023-01-11'})
        self.assertEqual(response.status_code, 302)  # Assuming successful redirection after updating rental

    def test_profile_view_success(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    # Test failure cases for each view
    def test_home_view_failure(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('home'))

    def test_rent_uav_failure(self):
        response = self.client.post(reverse('rent_uav', kwargs={'uav_id': self.uav.id}), {'start_date': '2023-01-01', 'end_date': '2023-01-10'})
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('rent_uav', kwargs={'uav_id': self.uav.id}))

    def test_return_uav_failure(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('return_uav', kwargs={'rental_id': 1234}))  # Assuming rental ID does not exist
        self.assertEqual(response.status_code, 404)  # Assuming 404 error for non-existing rental ID

    def test_update_rental_failure(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('update_rental', kwargs={'rental_id': 1235}))  # Assuming rental ID does not exist
        self.assertEqual(response.status_code, 404)  # Assuming 404 error for non-existing rental ID

    def test_profile_view_failure(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('profile'))
