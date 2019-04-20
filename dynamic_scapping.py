from selenium import webdriver
import json

def get_repo_name(url):
    return '_'.join(url.split('/')[-2:])

url = 'https://github.com/porbs/todo-manager-mobile-client'
sufix = '/graphs/contributors'
driver = webdriver.Firefox()
driver.implicitly_wait(5)
driver.get(url + sufix)

contributors = driver.find_elements_by_xpath(".//*[contains(@class,'contrib-person')]/span/h3/a[contains(@class, 'text-normal')]")
commits_amount = driver.find_elements_by_xpath(".//*[contains(@class,'contrib-person')]/span/h3/span[contains(@class, 'd-block')]/span[contains(@class, 'cmeta')]/a")
lines_added = driver.find_elements_by_xpath(".//*[contains(@class,'contrib-person')]/span/h3/span[contains(@class, 'd-block')]/span[contains(@class, 'cmeta')]/span[contains(@class, 'text-green')]")
lines_deleted = driver.find_elements_by_xpath(".//*[contains(@class,'contrib-person')]/span/h3/span[contains(@class, 'd-block')]/span[contains(@class, 'cmeta')]/span[contains(@class, 'text-red')]")

contr = []
commt = []
lin_a = []
lin_d = []

print('contributors: ')
for contributor in contributors:
    contr.append(contributor.text)

print('commits amount')
for ca in commits_amount:
    text = ca.text
    commits = text.split(' ')[0]
    commt.append(commits)

print('lines added')
for la in lines_added:
    text = la.text
    result = text.split(' ')[0]
    lin_a.append(result)

print('lines removed')
for ld in lines_deleted:
    text = ld.text
    result = text.split(' ')[0]
    lin_d.append(result)

result_array = []

for i in range(len(contributors)):
    res_obj = {
        "contributor": contr[i],
        "commits_amount": commt[i],
        "lines_added": lin_a[i],
        "lines_deleted": lin_d[i]
    }
    result_array.append(res_obj)

with open(get_repo_name(url) + '.json', 'w') as fp:
    json.dump(result_array, fp)

