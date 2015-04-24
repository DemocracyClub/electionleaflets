# -*- coding: utf-8 -*-
import os
import json

from lxml import html

from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.management import call_command

from lettuce import *
from lettuce.django import django_url



@before.all
def set_browser():
    world.browser = Client()

@before.all
def load_fixtures():
    call_command('loaddata', 'fixtures', 'constituencies')

@step(r'I access the url "(.*)"')
def access_url(step, url):
    full_url = django_url(url)
    response = world.browser.get(full_url)
    world.dom = html.fromstring(response.content)

@step(r'I see the header "(.*)"')
def see_header(step, text):
    for header in world.dom.cssselect('h1,h2'):
        if header.text == text:
            assert True
            return
    assert False

@step(r'I pick the file (.*):')
def set_file(step, name):
    file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),'../tests/test_images/', name))
    if os.path.exists(file_path):
        world.data = {'image': open(file_path, 'r')}
        assert True
        return
    assert False

@step(r'submit the image (.*) form')
def submit_image_form(step, form_name):
    world.data['leaflet_upload_wizzard-current_step'] = form_name
    world.response = world.browser.post(
            reverse('upload_step', kwargs={'step':form_name}),
            world.data,
            follow=True,
            format='multipart'
        )

@step(r'see the url "(.*)"')
def check_url(step, url):
    assert world.response.request['PATH_INFO'] == url

@step(r'I submit the form with:')
def fill_journey(step):
    for form in step.hashes:
        for k,v in form.items():
            if k not in ['step_name','image', 'action']:
                form["%s-%s" % (form['step_name'], k)] = v

        if 'image' in form.keys() and form['image']:
            set_file(step, form['image'])
            form['%s-image' % form['step_name']] = world.data['image']
        form_name = form['step_name']
        form['leaflet_upload_wizzard-current_step'] = form_name
        if 'action' in form.keys() and form['action']:
            form[form['action']] = True

        world.response = world.browser.post(
                reverse('upload_step', kwargs={'step':form_name}),
                form,
                follow=True,
                format='multipart'
            )

@step(r'and I should see (.*) leaflet images')
def count_images(step, number):
    world.dom = html.fromstring(world.response.content)
    assert len(world.dom.cssselect('.leaflet_images figure')) == int(number)

@step(r'in the constituency "(.*)"')
def find_constituency(step, constituency_name):
    world.dom = html.fromstring(world.response.content)
    text = world.dom.cssselect('article')[0].text_content()
    search = "in %s" % constituency_name
    assert search in text