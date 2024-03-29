from dataclasses import dataclass


@dataclass
class MenuElement:
    title: str
    url_name: str
    icon_class: str
    needs_auth: bool = False


menu = [
    MenuElement('Главная', 'home', 'fi fi-rr-home'),
    MenuElement('Мои Заказы', 'orders', 'fi fi-rr-document', True),
    MenuElement('Продавцы', 'sellers', 'fi fi-rr-users'),
    MenuElement('Пункты выдачи', 'pick_point_map', 'fi fi-rr-marker'),
    MenuElement('Корзина', 'cart', 'fi fi-rr-shopping-cart'),
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu[:-1]
        user = self.request.user
        if user.is_authenticated:
            context['cart_menu_element'] = menu[-1]
            context['cart_goods_count'] = self.request.user.cart.cart_goods.count()
        return context
