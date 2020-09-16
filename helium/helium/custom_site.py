from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = "Helium"
    site_title = "Helium 管理后台"
    index_title = "首页"

custom_site = CustomSite("cus_admin")
