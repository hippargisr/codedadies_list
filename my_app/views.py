import requests
from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLS_URL = 'https://pune.craigslist.org/search/jjj?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')

def new_search(request):
	search = request.POST.get('search')
	models.Search.objects.create(search=search)
	final_url = BASE_CRAIGSLS_URL.format(quote_plus(search))
	response = requests.get(final_url)
	data = response.text
	soup = BeautifulSoup(data, features='html.parser')

	post_list = soup.find_all('li', {'class': 'result-row'})

	if post_list:
		post_title = post_list[0].find(class_ = 'result-title').text
		post_url = post_list[0].find('a').get('href')
		# post_price = post_list[0].find(class_ = 'result-price').text
		# print(post_title,post_url)
		final_posting = []
		for post in post_list:
			post_title = post.find(class_ = 'result-title').text
			post_url = post.find('a').get('href')

			if post_list[0].find(class_ = 'result-price'):
				post_price = post.find(class_='result-price').text
			else:
				post_price = 'N/A'

			if post.find(class_ = 'result-image').get('data-ids'):
				post_image_id = post.find(class_ = 'result-image').get('data-ids').split(',')[0].split(':')[1]
				post_image_url = BASE_IMAGE_URL.format(post_image_id)
				print('image--->',post_image_url)
			else:
				post_image_url = 'https://craigslist.org/images/peace.jpg'

			final_posting.append((post_title, post_url, post_price, post_image_url))
	else:
		error_message = "Search not found",

	context = {
		'search': search,
		'final_posting': final_posting,
		'error_message': error_message,
	}
	return render(request, 'my_app/new_search.html', context)
