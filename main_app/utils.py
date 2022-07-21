from dataclasses import dataclass


@dataclass
class MenuElement:
    title: str
    url_name: str
    icon_class: str


menu = [
    MenuElement('Главная', 'home', 'fi fi-rr-home'),
    MenuElement('Мои Заказы', 'orders', 'fi fi-rr-document'),
    MenuElement('Продавцы', 'sellers', 'fi fi-rr-users'),
    MenuElement('Корзина', 'cart', 'fi fi-rr-shopping-cart')
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