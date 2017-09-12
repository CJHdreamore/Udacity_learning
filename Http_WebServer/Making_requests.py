import requests
r = requests.get('https://api.github.com/events')
p = requests.post('http://httpbin.org/post',data={'key':'value'})
payload = {'key1':'value1','key2': 'value2'}
b = requests.get('http://httpbin.org/get',params=payload)
print (b)





