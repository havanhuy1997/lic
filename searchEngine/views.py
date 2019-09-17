from django.http import HttpResponse , JsonResponse
from django.shortcuts import render
from .forms import searchForm , LoginForm , OtpForm
from .models import reviewData
from searchEngine.utils import myfunc, getreviews
from selenium import webdriver
import time
from selenium.webdriver.common import keys
import pandas as pd
import json
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import Select
from datetime import date
import os
from selenium.webdriver.common.action_chains import ActionChains
import easygui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.views.decorators.csrf import csrf_exempt

dict_drivers = {}

@csrf_exempt
def fun1(request):
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            idInput = form.cleaned_data['username']
            pswdInput = form.cleaned_data['password']
            dobInput = form.cleaned_data['dob']
            
            driver = webdriver.Chrome()

            #request.session[idInput] = driver
            ###   Session management 
            ### Baically the username would contain the driver instance
            ### DIDN'T WORK

            dict_drivers[idInput] = driver

            driver.get('https://ebiz.licindia.in/D2CPM/#Login')

            driver.maximize_window()
            while True:
                try:
                    driver.find_elements_by_class_name('x-form-item-body')[2]
                    print("Page is ready!")
                    time.sleep(5)
                    break # it will break from the loop once the specific element will be present. 
                except:
                    time.sleep(5)
                    print("Loading took too much time!-Try again")    
                    
            time.sleep(5)
            
            driver.find_elements_by_class_name('x-form-item-body')[2].click()
            actions = ActionChains(driver)
            actions.move_to_element(driver.find_elements_by_class_name('x-boundlist-item')[0]).click().perform()
            time.sleep(2)
            
            actions = ActionChains(driver)
            actions.move_to_element(driver.find_elements_by_class_name('x-form-item-body')[3]).click().perform()
            actions.move_to_element(driver.find_elements_by_class_name('x-form-item-body')[3]).send_keys(str(idInput)).perform()
            time.sleep(2)
            
            actions = ActionChains(driver)
            actions.move_to_element(driver.find_elements_by_class_name('x-form-item-body')[4]).click().perform()
            actions.move_to_element(driver.find_elements_by_class_name('x-form-item-body')[4]).send_keys(str(pswdInput)).perform()
            time.sleep(2)
            
            actions = ActionChains(driver)
            actions.move_to_element(driver.find_elements_by_class_name('x-form-item-body')[5]).click().perform()
            actions.move_to_element(driver.find_elements_by_class_name('x-form-item-body')[5]).send_keys(str(dobInput)).perform()
            time.sleep(2)
            
            login_url = driver.current_url

            actions = ActionChains(driver)
            actions.move_to_element(driver.find_elements_by_class_name('x-box-layout-ct')[12]).click().perform()
            
            ##Waiting
            time.sleep(10)

            if login_url == driver.current_url:
                print('Wrong Credentials')
                return_response = {
                    'status':0# O means credentials are wrong 
                }
                driver.quit()
                return JsonResponse(return_response)
            else:
                print('Credentials Worked')
                return_response = {
                    'status':1# 1 means credentials worked now ask for otp and send it to url: /search/otp 
                }
                return JsonResponse(return_response)

        else:
            print('Invalid Form Data')
            return_response = {
                'status':3 # 3 means invalid form data sent 
            }
            return JsonResponse(return_response) 
    
    else:
        return_response = {
            'status':2 # 1 means get or any other request is used instead of  
        }
        return JsonResponse(return_response)

@csrf_exempt
def fun2(request):
    if request.method == "POST":
        form = OtpForm(request.POST)  
        if form.is_valid():
            idInput = form.cleaned_data['username']
            otpcode = form.cleaned_data['otp']
            
            #driver = request.session[idInput]
            driver = dict_drivers[idInput]
            ###   Session management 
            ### Baically the username would contain the driver instance
            
            actions = ActionChains(driver)
            actions.move_to_element(driver.find_elements_by_class_name('x-form-item-body')[2]).click().perform()
            actions.move_to_element(driver.find_elements_by_class_name('x-form-item-body')[2]).send_keys(str(otpcode)).perform()
            
            time.sleep(6)
            
            url_check = driver.current_url

            submitbutt = driver.find_elements_by_class_name('x-btn')

            for i in submitbutt:
                if 'Submit' in i.text:
                    actions = ActionChains(driver)
                    actions.move_to_element(i).click().perform()
                    break

            time.sleep(20)

            if url_check == driver.current_url:
                driver.quit()
                return_response = {
                    'status':0 # O means otp didn't work 
                }
                return JsonResponse(return_response)
          
            while True:
                try:
                    actions = ActionChains(driver)
                    actions.move_to_element(driver.find_elements_by_class_name('x-form-item-body')[2]).click().perform()
                    time.sleep(2)
                    break # it will break from the loop once the specific element will be present. 
                except:
                    time.sleep(5)
                    print("Loading took too much time!-Try again")

            while True:
                try:
                    actions = ActionChains(driver)
                    actions.move_to_element(driver.find_elements_by_class_name('x-boundlist-item')[3]).click().perform()
                    time.sleep(2)
                    break # it will break from the loop once the specific element will be present. 
                except:
                    time.sleep(5)
                    print("Loading took too much time!-Try again")
            
            driver.find_elements_by_class_name('x-form-item-body')[7].click()
            actions = ActionChains(driver)
            actions.move_to_element(driver.find_elements_by_class_name('x-form-item-body')[7]).send_keys('01/01/1950').perform()
            time.sleep(2)
            
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            
            driver.find_elements_by_class_name('x-form-item-body')[8].click()
            actions = ActionChains(driver)
            actions.move_to_element(driver.find_elements_by_class_name('x-form-item-body')[8]).send_keys(d1).perform()
            
            time.sleep(15)
            
            actions = ActionChains(driver)
            actions.move_to_element(driver.find_element_by_class_name('x-btn-icon-el-TransbluebtnUI-small')).click().perform()
            time.sleep(10)
            
            sino = []
            policynumber = []
            name = []
            doc = []
            premium = []
            mode = []
            fup = []
            agentcode = []
            plan = []
            term = []
            sumassured = []
            status = []
            
            while True:            
                time.sleep(10)
                try:
                    df = pd.read_html(driver.find_elements_by_class_name('x-panel-bodyWrap')[3].get_attribute('innerHTML')) ###<-- List
                    
                    for i in df:
                        sino.append(i[0].item())
                        policynumber.append(i[1].item())
                        name.append(i[2].item())
                        doc.append(i[3].item())
                        premium.append(i[4].item())
                        mode.append(i[5].item())
                        fup.append(i[6].item())
                        agentcode.append(i[7].item())
                        plan.append(i[8].item())
                        term.append(i[9].item())
                        sumassured.append(i[10].item())
                        status.append(i[11].item())
                except BaseException as e:
                    print(str(e))
                    pass        
                try:
                    driver.find_elements_by_class_name('x-btn-plain-toolbar-small')[2].click()
                    time.sleep(15)
                except:
                    print('here')
                    break
            
            df = pd.DataFrame(columns=['SI#','Policy Number','Customer Name','Doc','Premium','Mode','Fup','Agent Code','Plan','Term','Sum Assured','Status'], data={'SI#':sino,'Policy Number':policynumber,'Customer Name':name,'Doc':doc,'Premium':premium,'Mode':mode,'Fup':fup,'Agent Code':agentcode,'Plan':plan,'Term':term,'Sum Assured':sumassured,'Status':status}) 
            #df.to_csv("./OUTPUT" + str(idInput) +".csv", sep=',', index=False) 
            
            driver.quit()

            print(df.to_json())
            return JsonResponse(df.to_json()) 

        else:
            return_response = {
                'status':3 # 3 means invalid form data sent 
            }
            return JsonResponse(return_response) 
    
    else:
        return_response = {
            'status':2 # 1 means get or any other request is used instead of  
        }
        return JsonResponse(return_response)
