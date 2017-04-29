"""Class that defines several financial calculators."""

import math
import locale
import decimal


class CompoundInterest(object):
    """Calculates compound interest of an investment.

    Given an initial investment, interest rate, compound period, and
    investment duration, a class is created with methods to calculate;
    the future value of an investment, yearly return, periodic return
    and effective interest rate.

    Attributes:
        pv: present value or initial investment.
        r: interest rate in decimal form.
        m: compound interval, i.e. monthly, yearly, etc.
        t: duration of investment in years.

    """

    def __init__(self, pv, r, m=1, t=1):
        """Initiates CompoundInterest class with initial investment
        and interest rate. Default values are a yearly compound and a
        one year duration.

        Args:
            pv: decimal.Decimal. present value
            r: decimal.Decimal. interest rate.
            m: int. compound periods per year.
            t: int. duration of investment in years.
        """
        self.pv = decimal.Decimal(pv)
        self.r = decimal.Decimal(r)
        self.m = int(m)
        self.t = int(t)
        self._i = decimal.Decimal(self.r / self.m)
        self._cents = decimal.Decimal('0.01')
        self._up = decimal.ROUND_HALF_UP

    def future_value(self):
        """Returns the future value of an investment."""
        value = self.pv * self._rate_compound(compound=self.m, time=self.t)
        return decimal.Decimal(value).quantize(self._cents, rounding=self._up)

    def future_value_yearly(self):
        """Returns in a generator of the yearly return of the investment."""
        current_value = self.pv
        for year in range(self.t):
            current_value *= self._rate_compound(compound=self.m)
            yield current_value.quantize(self._cents, rounding=self._up)

    def future_value_periodic(self):
        """Returns in a generator of the periodic return of the investment."""
        current_value = self.pv
        for period in range(self.t * self.m):
            current_value *= self._rate_compound()
            yield current_value.quantize(self._cents, rounding=self._up)

    def effective_rate(self):
        """Returns the effective interest rate as a string."""
        rate = decimal.Decimal(
            (self._rate_compound(self.m) - 1) * 100).quantize(
            decimal.Decimal('1.0000'))
        return '{interest}%'.format(interest=rate)

    def _rate_compound(self, compound=1, time=1):
        """Returns the interest rate per compound period."""
        return decimal.Decimal(math.pow(1 + self._i, compound * time))

    def print_money(self, func):
        locale.setlocale(locale.LC_MONETARY, '')
        try:
            print('\nPrinting money values for {}:\n'.format(func.__name__))
            for x in func():
                print(locale.currency(x, grouping=True))
        except TypeError:
            print(locale.currency(func(), grouping=True))
