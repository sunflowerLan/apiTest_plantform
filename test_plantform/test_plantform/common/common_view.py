from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def pageInation(query_obj, default_item, get_page):
    """
    分页功能实现
    :param query_obj:
    :param default_item:
    :param get_page:
    :return:
    """
    # 默认每页显示default_item条
    paginator = Paginator(query_obj, default_item)
    try:
        # 获取第get_page页
        contacts = paginator.page(get_page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    # 返回分页结果
    return contacts