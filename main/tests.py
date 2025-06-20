from django.test import TestCase
from django.urls import reverse
from .models import *
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.

class CVViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        skill_python = Skill.objects.create(name='Test_skill Python')
        project_test = Project.objects.create(name='Test_project PROJECTNAME', description='Long description about test project.')
        cls.cv = CV.objects.create(
            firstname='FirstNameTest',
            lastname='LastNameTest',
            bio='Some user bio.',
            contacts={'Testcontact': 'test@test.test'}
        )
        cls.cv.skills.add(skill_python)
        cls.cv.projects.add(project_test)

    def test_cv_list_view(self):
        url = reverse('cv_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'main/cv_list.html') 

        # User Name
        self.assertContains(response, 'FirstNameTest LastNameTest') 
        # User skill bage
        self.assertContains(response, 'Test_skill Python') 

    def test_cv_detail_view(self):
        url = reverse('cv_detail', args=[self.cv.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/cv_detail.html')
        
        # User bio
        self.assertContains(response, 'Some user bio.') 
        
        # User skill bage
        self.assertContains(response, 'Test_skill Python') 
        
        # project name
        self.assertContains(response, 'Test_project PROJECTNAME') 
        
        # contact
        self.assertContains(response, 'Testcontact: test@test.test') 
        


class CVAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cv = CV.objects.create(firstname="API", lastname="user", bio="test")

    def test_create_cv(self):
        url = reverse('api_cv_list') 
        data = {'firstname': 'new', 'lastname': 'lastname', 'bio': 'test bio 2'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CV.objects.count(), 2)
        self.assertEqual(CV.objects.get(id=response.data['id']).firstname, 'new') # type:ignore

    def test_list_cvs(self):
        url = reverse('api_cv_list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # type:ignore

    def test_retrieve_cv(self):
        url = reverse('api_cv_detail', args=[self.cv.pk])
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['firstname'], 'API') # type:ignore

    def test_update_cv(self):
        url = reverse('api_cv_detail', args=[self.cv.pk])
        data = {'firstname': 'updated', 'lastname': 'User', 'bio': 'updated Bio'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.cv.refresh_from_db()
        self.assertEqual(self.cv.firstname, 'updated')

    def test_delete_cv(self):
        url = reverse('api_cv_detail', args=[self.cv.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CV.objects.count(), 0)


class LoggingTest(TestCase):

    def test_create_log(self):
        self.assertEqual(RequestLog.objects.count(), 0)
        url = reverse('request_log_list')
        self.client.get(url)
        self.assertEqual(RequestLog.objects.count(), 1)

        self.client.post(url)
        self.assertEqual(RequestLog.objects.count(), 2)

        first_log = RequestLog.objects.first()

        self.assertEqual(first_log.method, "GET") #type: ignore
        self.assertEqual(first_log.path, url) #type: ignore

        last_log = RequestLog.objects.last()

        self.assertEqual(last_log.method, "POST") #type: ignore
        self.assertEqual(last_log.path, url) #type: ignore

