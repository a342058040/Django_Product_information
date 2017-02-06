from django.shortcuts import render
from MDjango.models import Info
from django.core.paginator import Paginator


# ============================================== <<<< DATA GENS >>>> ====================================================

# 不同区域发帖量前8名
def topx(date1, date2, area, limit):
	pipeline = [
		{'$match': {'$and': [{'pub_date': {'$gte': date1, '$lte': date2}}, {'area': {'$all': area}}]}},
		{'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
		{'$limit': limit},
		{'$sort': {'counts': -1}}
	]

	for i in Info._get_collection().aggregate(pipeline):
		data = {
			'name': i['_id'][0],
			'data': [i['counts']],
			'type': 'column'
		}
		yield data


series_CY = [i for i in topx('2015.12.28', '2016.1.10', ['朝阳'], 8)]
series_TZ = [i for i in topx('2015.12.28', '2016.1.10', ['通州'], 8)]
series_HD = [i for i in topx('2015.12.28', '2016.1.10', ['海淀'], 8)]
series_DC = [i for i in topx('2015.12.28', '2016.1.10', ['东城'], 8)]
series_CP = [i for i in topx('2015.12.28', '2016.1.10', ['昌平'], 8)]
series_YJ = [i for i in topx('2015.12.28', '2016.1.10', ['燕郊'], 8)]

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# # 数据中发帖总量柱状图
def total_post():
	pipeline = [
		{'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
	]

	for i in Info._get_collection().aggregate(pipeline):
		print(i)
		data = {
			'name': i['_id'][0],
			'y': i['counts']
		}
		yield data


series_post = [i for i in total_post()]
#
#
# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def one_day_deal_cate():
	pipeline = [
		{'$match': {'$and': [{'pub_date': {'$gte': '2015.12.25', '$lte': '2016.01.11'}}, {'time': 1}]}},
		{'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
		{'$sort': {'counts': 1}}
	]

	for i in Info._get_collection().aggregate(pipeline):
		data = {
			'name': i['_id'][0],
			'y': i['counts']
		}
		yield data


def one_day_deal_area():
	pipeline = [
		{'$match': {'$and': [{'pub_date': {'$gte': '2015.12.25', '$lte': '2016.01.11'}}, {'time': 1}]}},
		{'$group': {'_id': {'$slice': ['$area', 1]}, 'counts': {'$sum': 1}}},
		{'$sort': {'counts': 1}}
	]

	for i in Info._get_collection().aggregate(pipeline):
		data = {
			'name': i['_id'][0],
			'y': i['counts']
		}
		yield data


pie1_data = [i for i in one_day_deal_cate()]
pie2_data = [i for i in one_day_deal_area()]


# ============================================== <<<< PAGE VIEWS >>>> ===================================================


def index(request):
	limit = 15 # 每页显示的记录数
	m_info = Info.objects
	paginatior = Paginator(m_info, limit)  # 实例化一个分页对象
	page = request.GET.get('page', 1) # 获取页码
	print(request)
	print(request.GET)
	loaded = paginatior.page(page) # 获取某页对应的记录

	context = {
		'Info': loaded,
		'counts': m_info.count(),
		'last_time': m_info.order_by('-pub_date').limit(1),

	}

	return render(request, 'index_data.html', context)


def chart(request):
	context = {
		'chart_CY': series_CY,
		'chart_TZ': series_TZ,
		'chart_HD': series_HD,
		'chart_DC': series_DC,
		'chart_CP': series_CP,
		'chart_YJ': series_YJ,
		'series_post': series_post,
		'pie1_data': pie1_data,
		'pie2_data': pie2_data
	}
	return render(request, 'chart2.html', context)
