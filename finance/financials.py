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
            pv: float: present value
            r: float: interest rate.
            m: int: compound periods per year.
            t: int: duration of investment in years.
        """
        self.pv = decimal.Decimal(pv)
        self.r = decimal.Decimal(r)
        self.m = int(m)
        self.t = int(t)
        locale.setlocale(locale.LC_MONETARY, '')
        self._cents = decimal.Decimal('0.01')
        self._up = decimal.ROUND_HALF_UP

    def future_value(self):
        """Returns the future value of an investment."""
        return decimal.Decimal(self.pv * math.pow(1 + self.r / self.m,
                               self.m * self.t)).quantize(
                               self._cents, rounding=self._up)
        # print(locale.currency(fv, grouping=True))

    def future_value_yearly(self):
        """Returns in a list the yearly return of the investment."""
        current_value = self.pv
        # yearly = []
        for year in range(self.t):
            current_value *= decimal.Decimal(math.pow(1 + self.r / self.m,
                                             self.m))
            # current_value* *= decimal.Decimal(math.pow(1 + self.r / self.m, self.m))
            # yearly.append(decimal.Decimal(current_value).quantize(
                          # self._cents, rounding=self._up))
            yield current_value.quantize(self._cents, rounding=self._up)
        # return yearly

    def future_value_periodic(self):
        """Returns in a list the periodic return of the investment."""
        current_value = self.pv
        periodic = []
        for period in range(1, self.m * self.t + 1):
            current_value *= 1 + self.r / self.m
            periodic.append(decimal.Decimal(current_value).quantize(
                            self._cents, rounding=self._up))
            # print('Period {}: {}'.format(period,
            #       locale.currency(current_value, grouping=True)))
        return periodic

    def effective_interest_rate(self):
        """Returns the effective interest rate """
        return decimal.Decimal(math.pow(
                               1 + self.r / self.m, self.m) - 1).quantize(
                               decimal.Decimal('0.00001'))
