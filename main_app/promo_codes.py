import decimal


class PromoCode:
    def activate(self, cart) -> (bool, str):
        pass


class DiscountPromoCode(PromoCode):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, cart) -> (bool, str):
        cart.total_with_discount = cart.total - cart.total * decimal.Decimal(self.amount * 0.01)
        return True, f'Скидка {self.amount} %'


promo_codes = {
    ('DISCOUNT_5', 'Скидка 5%'): DiscountPromoCode(5),
    ('DISCOUNT_10', 'Скидка 10%'): DiscountPromoCode(10),
    ('DISCOUNT_20', 'Скидка 20%'): DiscountPromoCode(20),
}
