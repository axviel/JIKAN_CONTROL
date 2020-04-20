from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.db import connection

from django.contrib.auth.models import User

import time

class TestProject(StaticLiveServerTestCase):

  delay = 10

  def setUp(self):
    self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
    self.browser.maximize_window()
    # self.url = self.live_server_url
    self.url = 'http://127.0.0.1:8000'
    self.browser.get(self.url)

  def tearDown(self):
    self.browser.close()

  def test01_signup_page_loads(self):
    self.go_to_signup_page()
    signup_url = self.url + '/accounts/signup'

    # Validate if URLs are the same
    self.assertEquals(
      self.browser.current_url,
      signup_url,
      'Signup page did not load'
    )

  def test02_signup(self):
    # Sign Up Process
    self.sign_up()

    # Validate if was redirected to Login page
    # login_url = self.url + 'accounts/login'
    login_url = self.url + '/accounts/login'

    self.assertEquals(
      self.browser.current_url,
      login_url,
      'Account was not created'
    )

  def test03_login(self):
    # Login Process
    self.login()

    # Validate if was redirected to Calendar page
    calendar_url = self.url + '/jikancalendar/'

    self.assertEquals(
      self.browser.current_url,
      calendar_url,
      'Did not login'
    )

  def test04_create_event_in_calendar(self):
    self.login()

    # Click day
    self.browser.find_element_by_xpath('//*[@id="calendar"]/div/div[3]/div[16]').click()

    # Wait until Current Day Modal appears
    WebDriverWait(self.browser, self.delay).until(EC.visibility_of_element_located((By.ID, 'current-day-modal')))

    # Create the event
    self.browser.find_element_by_id('add-event-btn').click()
    self.browser.find_element_by_id('title').send_keys('Selenium Event Test')
    self.browser.find_element_by_id('description').send_keys('Desc: Selenium Event Test')
    self.browser.find_element_by_id('start_time').send_keys('07:00AM')
    self.browser.find_element_by_id('end_time').send_keys('09:00AM')
    self.browser.find_element_by_id('save-event-form-btn').click()

    # Wait until event list is visible
    WebDriverWait(self.browser, self.delay).until(EC.visibility_of_element_located((By.ID, 'current-day-event-list')))

    found_event_list = len(self.browser.find_elements_by_xpath('//*[@id="calendar"]/div/div[3]/div[16]')) > 0

    # Close modal
    self.browser.find_element_by_xpath('//*[@id="current-day-modal"]/div/div/div[1]/button').click()

    self.assertTrue(
      found_event_list,
      'Did not create the event'
    )
    
  def test05_create_event_in_detail(self):
    self.login()

    # Go to event list page
    self.menu_navigation('events')

    # Validate if was redirected to Event list page
    expected_url = self.url + '/events/list'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Is not in event list page'
    )

    # Go to event detail page
    self.browser.find_element_by_id('new-event-btn').click()

    # Validate if was redirected to Event list page
    expected_url = self.url + '/events/detail'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Is not in event detail page'
    )

    # Fill event form
    self.browser.find_element_by_id('title').send_keys('Selenium Event Test 2')
    self.browser.find_element_by_id('description').send_keys('Desc: Selenium Event Test 2')
    self.browser.find_element_by_id('start_date').send_keys('04182020')
    self.browser.find_element_by_id('start_time').send_keys('07:00AM')
    self.browser.find_element_by_id('end_time').send_keys('09:00AM')
    self.browser.find_element_by_id('save-event-btn').click()

    # Validate event was created
    alert_text = self.browser.find_element_by_id('message').text

    self.assertEquals(
      alert_text,
      '×\nSuccess Event created successfully',
      'Event was not created'
    )

  def test06_create_course(self):
    self.login()

    # Go to event list page
    self.menu_navigation('courses')

    # Validate if was redirected to Event list page
    expected_url = self.url + '/courses/list'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Is not in event list page'
    )

    # Go to event detail page
    self.browser.find_element_by_id('new-course-btn').click()

    # Validate if was redirected to Event list page
    expected_url = self.url + '/courses/detail'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Is not in course detail page'
    )

    # Fill event form
    self.browser.find_element_by_id('title').send_keys('Selenium Course Test')
    self.browser.find_element_by_id('description').send_keys('Desc: Selenium Course Test')
    self.browser.find_element_by_id('save-course-btn').click()

    # Validate event was created
    alert_text = self.browser.find_element_by_id('message').text

    self.assertEquals(
      alert_text,
      '×\nSuccess Course created successfully',
      'Course was not created'
    )

  def test07_create_exam(self):
    self.login()

    # Go to next month
    self.browser.find_element_by_xpath('//*[@id="calendar"]/div/div[1]/div/i[2]').click()

    # Click day
    self.browser.find_element_by_xpath('//*[@id="calendar"]/div/div[3]/div[16]').click()

    # Wait until Current Day Modal appears
    WebDriverWait(self.browser, self.delay).until(EC.visibility_of_element_located((By.ID, 'current-day-modal')))

    # Create the event
    self.browser.find_element_by_id('add-event-btn').click()
    self.browser.find_element_by_id('title').send_keys('Selenium Event Test')
    self.browser.find_element_by_id('description').send_keys('Desc: Selenium Event Test')
    self.browser.find_element_by_id('start_time').send_keys('07:00AM')
    self.browser.find_element_by_id('end_time').send_keys('09:00AM')

    # Select Exam Type
    event_type = Select(self.browser.find_element_by_name('event_type'))
    event_type.select_by_value('4')

    self.browser.find_element_by_id('save-event-form-btn').click()

    WebDriverWait(self.browser, self.delay).until(EC.visibility_of_element_located((By.ID, 'current-day-event-list')))

    # Return to form and go click the exam button
    self.browser.find_element_by_xpath('//*[@id="current-day-event-list"]/div[2]/div[2]/ul/li[1]').click()

    WebDriverWait(self.browser, self.delay).until(EC.visibility_of_element_located((By.ID, 'exam-btn')))

    self.browser.find_element_by_id('exam-btn').click()

    # Validate that was redirected to exam detail page
    expected_url = self.url + '/exams/detail'

    WebDriverWait(self.browser, self.delay).until(EC.title_contains('Exam'))

    self.assertTrue(
      expected_url in self.browser.current_url,
      'Is not in exam detail page'
    )

    # Create the exam
    self.browser.find_element_by_id('title').send_keys('Selenium Event Test 2')
    self.browser.find_element_by_id('description').send_keys('Desc: Selenium Event Test 2')
    self.browser.find_element_by_id('predicted_study_hours').send_keys('12')
    self.browser.find_element_by_id('predicted_score').send_keys('95')
    self.browser.find_element_by_id('save-exam-btn').click()

    # Validate event was created
    alert_text = self.browser.find_element_by_id('message').text

    self.assertEquals(
      alert_text,
      '×\nSuccess Exam saved successfully',
      'Exam was not created'
    )

  def test08_create_note(self):
    self.login()

    # Go to event list page
    self.menu_navigation('notes')

    # Validate if was redirected to Event list page
    expected_url = self.url + '/notes/list'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Is not in note list page'
    )

    # Go to event detail page
    self.browser.find_element_by_id('new-note-btn').click()

    # Validate if was redirected to Event list page
    expected_url = self.url + '/notes/detail'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Is not in note detail page'
    )

    # Fill event form
    self.browser.find_element_by_id('title').send_keys('Selenium Note Test')
    self.browser.find_element_by_id('description').send_keys('Desc: Selenium Note Test')
    self.browser.find_element_by_id('save-note-btn').click()

    # Validate event was created
    alert_text = self.browser.find_element_by_id('message').text

    self.assertEquals(
      alert_text,
      '×\nSuccess Note saved successfully',
      'Note was not created'
    )

  def test09_delete_note(self):
    self.login()

    # Go to event list page
    self.menu_navigation('notes')

    # Validate if was redirected to Event list page
    expected_url = self.url + '/notes/list'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Is not in note list page'
    )

    # Go to existing note detail
    self.browser.find_element_by_xpath('//*[@id="note-list"]/tbody/tr[1]/td[4]/div/a').click()

    # Validate if was redirected to Event list page
    expected_url = self.url + '/notes/detail'

    self.assertTrue(
      expected_url in self.browser.current_url,
      'Is not in note detail page'
    )

    # Delete note
    self.browser.find_element_by_id('remove-note-btn').click()

    # Validate delete was successful
    expected_url = self.url + '/notes/list'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Did not delete note'
    )

  def test10_delete_exam(self):
    self.login()

    # Go to event list page
    self.menu_navigation('exams')

    # Validate if was redirected to Event list page
    expected_url = self.url + '/exams/list'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Is not in exam list page'
    )

    # Go to existing exam detail
    self.browser.find_element_by_xpath('//*[@id="exam-list"]/tbody/tr/td[7]/div/a').click()

    # Validate if was redirected to Exam detail page
    expected_url = self.url + '/exams/detail'

    self.assertTrue(
      expected_url in self.browser.current_url,
      'Is not in exam detail page'
    )

    # Delete note
    self.browser.find_element_by_id('remove-exam-btn').click()

    # Validate delete was successful
    expected_url = self.url + '/exams/list'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Did not delete exam'
    )

  def test11_delete_course(self):
    self.login()

    # Go to course list page
    self.menu_navigation('courses')

    # Validate if was redirected to Course list page
    expected_url = self.url + '/courses/list'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Is not in course list page'
    )

    # Go to existing course detail
    self.browser.find_element_by_xpath('//*[@id="course-list"]/tbody/tr/td[3]/div/a').click()

    # Validate if was redirected to Courses detail page
    expected_url = self.url + '/courses/detail'

    self.assertTrue(
      expected_url in self.browser.current_url,
      'Is not in course detail page'
    )

    # Delete course
    self.browser.find_element_by_id('remove-course-btn').click()

    # Validate delete was successful
    expected_url = self.url + '/courses/list'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Did not delete course'
    )

  def test12_delete_event(self):
    self.login()

    # Go to event list page
    self.menu_navigation('events')

    # Validate if was redirected to Event list page
    expected_url = self.url + '/events/list'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Is not in event list page'
    )

    # Go to existing event detail
    self.browser.find_element_by_xpath('//*[@id="event-list"]/tbody/tr[1]/td[7]/div/a').click()

    # Validate if was redirected to Event detail page
    expected_url = self.url + '/events/detail'

    self.assertTrue(
      expected_url in self.browser.current_url,
      'Is not in event detail page'
    )

    # Delete course
    self.browser.find_element_by_id('remove-event-btn').click()

    # Validate delete was successful
    expected_url = self.url + '/events/list'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Did not delete event'
    )

  def test13_edit_profile(self):
    self.login()

    # Go to event list page
    self.menu_navigation('profile')

    # Validate if was redirected to Event list page
    expected_url = self.url + '/user/user_detail'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Is not in profile page'
    )

    # Fill event form
    self.browser.find_element_by_id('first_name').send_keys('SeleniumTestEdited')
    self.browser.find_element_by_id('last_name').send_keys('SeleniumTestEdited')
    self.browser.find_element_by_id('email').send_keys('edited@jikan.com')
    self.browser.find_element_by_id('save-profile-btn').click()

    # Validate event was created
    alert_text = self.browser.find_element_by_id('message').text

    self.assertEquals(
      alert_text,
      '×\nSuccess Profile updated successfully',
      'Profile was not saved'
    )
  
  def test14_logout(self):
    self.login()

    # Go to event list page
    self.menu_navigation('logout')

    # Validate if was redirected to Event list page
    expected_url = self.url + '/accounts/login'

    self.assertEquals(
      self.browser.current_url,
      expected_url,
      'Did not logout'
    )

  def go_to_signup_page(self):
    self.browser.find_element_by_id('signup-link').click()

  def sign_up(self):
    self.go_to_signup_page()

    # Fill the account form information
    self.browser.find_element_by_id('first-name').send_keys('SeleniumTest')
    self.browser.find_element_by_id('last-name').send_keys('SeleniumTest')
    self.browser.find_element_by_id('username').send_keys('SeleniumTest')
    self.browser.find_element_by_id('email').send_keys('selenium@jikan.com')
    self.browser.find_element_by_id('password').send_keys('12345')
    self.browser.find_element_by_id('password2').send_keys('12345')

    # Create the account
    self.browser.find_element_by_id('signup-btn').click()

    # Wait until notification appears
    WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.ID, 'message')))

  def login(self):
    # Sign Up Process
    # self.sign_up()

    # Fill login form
    self.browser.find_element_by_id('username').send_keys('SeleniumTest')
    self.browser.find_element_by_id('password').send_keys('12345')

    # Login
    self.browser.find_element_by_id('login-btn').click()

    # Wait calendar section appears
    WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.ID, 'calendar')))

  def menu_navigation(self, item):
    self.browser.find_element_by_id('sidebar-collapse').click()

    # Wait until menu appears
    WebDriverWait(self.browser, self.delay).until(EC.visibility_of_element_located((By.ID, 'sidebar')))

    if item == 'calendar':
      self.browser.find_element_by_xpath('//*[@id="sidebar"]/ul[1]/li[1]/a').click()
      WebDriverWait(self.browser, self.delay).until(EC.url_contains('jikancalendar'))
    elif item == 'events':
      self.browser.find_element_by_xpath('//*[@id="sidebar"]/ul[1]/li[2]/a').click()
      WebDriverWait(self.browser, self.delay).until(EC.url_contains('events'))
    elif item == 'notes':
      self.browser.find_element_by_xpath('//*[@id="sidebar"]/ul[1]/li[3]/a').click()
      WebDriverWait(self.browser, self.delay).until(EC.url_contains('notes'))
    elif item == 'exams':
      self.browser.find_element_by_xpath('//*[@id="sidebar"]/ul[1]/li[4]/a').click()
      WebDriverWait(self.browser, self.delay).until(EC.url_contains('exams'))
    elif item == 'courses':
      self.browser.find_element_by_xpath('//*[@id="sidebar"]/ul[1]/li[5]/a').click()
      WebDriverWait(self.browser, self.delay).until(EC.url_contains('courses'))
    elif item == 'profile':
      WebDriverWait(self.browser, self.delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sidebar"]/ul[2]/li[1]/a')))
      self.browser.find_element_by_xpath('//*[@id="sidebar"]/ul[2]/li[1]/a').click()
      WebDriverWait(self.browser, self.delay).until(EC.url_contains('user'))
    elif item == 'logout':
      WebDriverWait(self.browser, self.delay).until(EC.visibility_of_element_located((By.ID, 'logout-btn')))
      self.browser.find_element_by_id('logout-btn').click()
      WebDriverWait(self.browser, self.delay).until(EC.url_contains('login'))
