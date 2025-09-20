######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
######################################################################

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps

Steps file for web interactions with Selenium
"""
import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions

ID_PREFIX = 'product_'

##################################################################
# Navigation
##################################################################
@when('I visit the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)

@then('I should see "{message}" in the title')
def step_impl(context, message):
    assert message in context.driver.title

@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    element = context.driver.find_element(By.TAG_NAME, 'body')
    assert text_string not in element.text

##################################################################
# Text Fields
##################################################################
@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)

@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)

@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute('value') == u''

##################################################################
# Dropdowns
##################################################################
@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = Select(context.driver.find_element(By.ID, element_id))
    element.select_by_visible_text(text)

@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = Select(context.driver.find_element(By.ID, element_id))
    assert element.first_selected_option.text == text

##################################################################
# Copy & Paste Simulation
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

##################################################################
# Buttons
##################################################################
@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    btn = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.element_to_be_clickable((By.ID, button_id))
    )
    btn.click()

##################################################################
# Field / Results Validation
##################################################################
@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    assert found

@then('I should see "{text}" in the results')
def step_impl(context, text):
    results_id = "results"
    results = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, results_id))
    )
    assert text in results.text, f'Expected "{text}" in results'

@then('I should not see "{text}" in the results')
def step_impl(context, text):
    results_id = "results"
    results = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, results_id))
    )
    assert text not in results.text, f'Did not expect "{text}" in results'

##################################################################
# Flash Messages
##################################################################
@then('I should see the message "Success"')
def step_impl(context):
    body = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    assert "Success" in body.text, 'Expected to see "Success" message on the page'

@then('I should see the message "Product has been Deleted!"')
def step_impl(context):
    body = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    assert "Product has been Deleted!" in body.text, 'Expected to see deletion message on the page'

@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    assert found
