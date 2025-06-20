from django.test import TestCase
from django.urls import reverse
from .models import *

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
        
