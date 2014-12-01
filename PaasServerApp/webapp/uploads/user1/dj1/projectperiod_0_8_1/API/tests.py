from random import randint
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from API import views
from Core.models import *
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.conf import settings
from rest_framework.test import APIClient
from django.utils.translation import ugettext as _
from Core.crypto import Crypto

import requests, json

crypto = Crypto()

class AccountTests(APITestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'

        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

    def test_wrong_credentials(self):
        r = requests.get("http://127.0.0.1/ProjectPeriodDev/api/projects/?format=json", auth=('admin2', 'test2'))
        self.assertEqual(r.status_code, 401)

    def test_list_accounts_denied(self):
        user = User.objects.create_user(
            username='jacob2', email='jacob', password='top_secret')

        url = '/api/users/'
        data = {}

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_accounts(self):
        url = '/api/users/'
        data = {}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.get(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class API_Customer_Test(TestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'

        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        self.customer = Customer(name = 'test', street = '-', postcode = '-', city = '-', status = 0)
        self.customer.save()

    def test_customers_list(self):
        url = '/api/customers/'
        data = {}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.get(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_add(self):
        url = '/api/customers/'
        data = {"name": 'TestCustomer',
                "street": "Test",
                "postcode": "11111",
                "city": "Test",
                "country": "DE",
                "status": 0}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_customer_mod(self):
        idCustomer = Customer.objects.filter(name='test')[0].id

        url = '/api/customers/' + str(idCustomer) + '/'
        data = {"id": idCustomer,
                "name": 'TestCustomerMod',
                "street": "Test",
                "postcode": "11111",
                "city": "Test",
                "country": "DE",
                "status": 0}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_del(self):
        idCustomer = Customer.objects.filter(name='test')[0].id

        url = '/api/customers/' + str(idCustomer) + '/'
        data = {}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.delete(url, data, format='json')

        self.assertEqual(len(Customer.objects.all()), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class API_Project_Test(TestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'

        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        self.customer = Customer(name = 'test', street = '-', postcode = '-', city = '-', status = 0)
        self.customer.save()

        self.project = Project(name = 'test', description = '-', responsible = self.user, customer = self.customer, status = 1, budget = 10000, hourly_rate = 100, billing = 1)
        self.project.save()

    def test_projects_list(self):
        url = '/api/projects/'
        data = {}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.get(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_add(self):
        url = '/api/projects/'
        data = {"name": 'TestProject',
                "description": "Pro",
                "responsible": self.user.id,
                "customer": self.customer.id,
                "status": 0,
                "budget": 1000,
                "billing": 1,
                "hourly_rate": 100}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_project_mod(self):
        idProject = Project.objects.filter(name='test')[0].id

        url = '/api/projects/' + str(idProject) + '/'
        data = {"id": idProject,
                "name": 'testMod',
                "description": "Pro",
                "responsible": self.user.id,
                "customer": self.customer.id,
                "status": 0,
                "budget": 1000,
                "billing": 0,
                "hourly_rate": 100}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.put(url, data, format='json')

        self.assertEqual(len(Project.objects.filter(name='testMod')), 1)
        self.assertEqual(len(Project.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_del(self):
        idProject = Project.objects.filter(name='test')[0].id

        url = '/api/projects/' + str(idProject) + '/'
        data = {}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.delete(url, data, format='json')

        self.assertEqual(len(Project.objects.all()), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class API_Acquisition_Test(TestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'

        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        self.customer = Customer(name = 'test', street = '-', postcode = '-', city = '-', status = 0)
        self.customer.save()

        self.project = Project(name = 'test', description = '-', responsible = self.user, customer = self.customer, status = 1, budget = 10000, hourly_rate = 100, billing = 1)
        self.project.save()

        self.location = Location(name = 'test', street = '-', postcode = '-', city = '-', status = 0)
        self.location.save()

        self.acquisitions = Acquisition(user = self.user, start = '2014-04-03T10:42:00', end = '2014-04-03T10:48:00', project = self.project, location = self.location, comment = '-')
        self.acquisitions.save()

    def test_acquisitions_list(self):
        url = '/api/acquisitions/'
        data = {}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.get(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_acquisition_add(self):
        url = '/api/acquisitions/'
        data = {"user": self.user.id,
                "start": "2014-04-03T10:42:00",
                "end": "2014-04-03T10:48:00",
                "project": self.project.id,
                "location": self.location.id,
                "comment": "-",
                "billable": 1}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_acquisition_mod(self):
        idAcquisition= Acquisition.objects.all()[0].id

        url = '/api/acquisitions/' + str(idAcquisition) + '/'
        data = {"id": Acquisition.objects.all()[0].id,
                "user": self.user.id,
                "start": "2014-04-03T10:42:00",
                "end": "2014-04-03T11:48:00",
                "project": self.project.id,
                "location": self.location.id,
                "comment": "Mod"}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.put(url, data, format='json')

        self.assertEqual(len(Acquisition.objects.filter(comment='Mod')), 1)
        self.assertEqual(len(Acquisition.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_acquisition_del(self):
        idAcquisition = Acquisition.objects.all()[0].id

        url = '/api/acquisitions/' + str(idAcquisition) + '/'
        data = {}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.delete(url, data, format='json')

        self.assertEqual(len(Acquisition.objects.all()), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class API_Location_Test(TestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'

        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        self.customer = Customer(name = 'test', street = '-', postcode = '-', city = '-', status = 0)
        self.customer.save()

        self.location = Location(name = 'test', street = '-', postcode = '-', city = '-', status = 0)
        self.location.save()

    def test_locations_list(self):
        url = '/api/locations/'
        data = {}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.get(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_location_add(self):
        url = '/api/locations/'
        data = {"name": 'TestLocation',
                "street": "Test",
                "postcode": "11111",
                "city": "City",
                "country": "DE",
                "status": "0"}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_location_add_customer(self):
        idCustomer = Customer.objects.filter(name='test')[0].id

        url = '/api/locations/'
        data = {"name": 'TestLocation',
                "street": "Test",
                "postcode": "11111",
                "city": "City",
                "country": "DE",
                "customer": idCustomer,
                "status": "0"}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_location_mod(self):
        idCustomer = Customer.objects.filter(name='test')[0].id
        idLocation = Location.objects.filter(name='test')[0].id

        url = '/api/locations/' + str(idLocation) + '/'
        data = {"id": idLocation,
                "name": 'TestMod',
                "street": "Test Street",
                "postcode": "11111",
                "city": "City",
                "country": "DE",
                "customer": idCustomer,
                "status": "0"}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.put(url, data, format='json')

        self.assertEqual(len(Location.objects.filter(name='TestMod')), 1)
        self.assertEqual(len(Location.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_location_del(self):
        idLocation = Location.objects.filter(name='test')[0].id

        url = '/api/locations/' + str(idLocation) + '/'
        data = {}

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.delete(url, data, format='json')

        self.assertEqual(len(Location.objects.all()), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TheBugGenieTest(TestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')
        self.customer = Customer(name = 'test', street = '-', postcode = '-', city = '-', status = 0)
        self.customer.save()

        self.project = Project(name = 'test', description = '-', responsible = self.user, customer = self.customer, status = 1, budget = 10000, hourly_rate = 100, billing = 1)
        self.project.save()

    def test_show_no_integration(self):
        idProject = Project.objects.all()[0].id
        request = self.factory.get('/api_getWorkItems/', {'id_project': idProject})

        request.user = self.user

        response = views.api_getWorkItems(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('No Integration found'))

    def test_show_issues_denied(self):
        self.integrationDeny = Integration(user = self.user, tool = 0, project = self.project, url = 'http://10.0.0.1/thebuggenie/thebuggenie/projectperiod', username = 'test', password = 'deny')
        self.integrationDeny.save()

        idProject = Project.objects.all()[0].id
        request = self.factory.get('/api_getWorkItems/', {'id_project': idProject})

        request.user = self.user

        response = views.api_getWorkItems(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('WorkItems could not be read'))

    def test_show_issues(self):
        self.integration = Integration(user = self.user, tool = 0, project = self.project, url = 'http://10.0.0.1/thebuggenie/thebuggenie/projectperiod', username = 'administrator', password = 'admin')
        self.integration.save()

        idProject = Project.objects.all()[0].id
        request = self.factory.get('/api_getWorkItems/', {'id_project': idProject})

        request.user = self.user

        response = views.api_getWorkItems(request)
        self.assertEqual(response.status_code, 200)

class PolarionTest(TestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')
        self.customer = Customer(name = 'test', street = '-', postcode = '-', city = '-', status = 0)
        self.customer.save()

        self.project = Project(name = 'test', description = '-', responsible = self.user, customer = self.customer, status = 1, budget = 10000, hourly_rate = 100, billing = 1)
        self.project.save()

    def test_show_issues_denied(self):
        self.integrationDeny = Integration(user = self.user, tool = 1, project = self.project, url = 'http://10.0.0.1/polarion', username = 'test', password = crypto.encrypt('wrong'))
        self.integrationDeny.save()

        idProject = Project.objects.all()[0].id
        request = self.factory.get('/api_getWorkItems/', {'id_project': idProject})

        request.user = self.user

        response = views.api_getWorkItems(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('WorkItems could not be read'))

    def test_show_issues(self):
        self.integration = Integration(user = self.user, tool = 1, project = self.project, url = 'http://10.0.0.1/polarion', username = 'admin', password = crypto.encrypt('admin'), query = 'project.id:ProjectPeriod AND type:defect')
        self.integration.save()

        idProject = Project.objects.all()[0].id
        request = self.factory.get('/api_getWorkItems/', {'id_project': idProject})

        request.user = self.user

        response = views.api_getWorkItems(request)
        self.assertEqual(response.status_code, 200)