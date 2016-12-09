"""Class that defines several financial calculators."""

import math
import locale


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
        self.pv = pv
        self.r = r
        self.m = m
        self.t = t
        locale.setlocale(locale.LC_MONETARY, '')

    def future_value(self):
        """Prints the future value of an investment."""
        fv = self.pv * math.pow(1 + self.r / self.m, self.m * self.t)
        print(locale.currency(fv, grouping=True))

    def future_value_yearly(self):
        """Prints the yearly return of the investment."""
        current_value = self.pv
        for year in range(1, self.t + 1):
            current_value *= math.pow(1 + self.r / self.m, self.m)
            print('Year {}: {}'.format(year,
                  locale.currency(current_value, grouping=True)))

    def future_value_periodic(self):
        """Prints the periodic return of the investment."""
        current_value = self.pv
        for period in range(1, self.m * self.t + 1):
            current_value *= 1 + self.r / self.m
            print('Period {}: {}'.format(period,
                  locale.currency(current_value, grouping=True)))

    def effective_interest_rate(self):
        """Prints effective interest rate """
        print(round(math.pow(1 + self.r / self.m, self.m) - 1, 4))
