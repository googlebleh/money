#!/usr/bin/env python3


def sprint_dollars(float_):
    # adapted from https://stackoverflow.com/a/21208495
    return f"${float_:,.2f}"


def tax_for_short_term_capital(gains):
    tiers_2021 = {
        9950: 0.10,
        40525: 0.12,
        86375: 0.22,
        164925: 0.24,
        209425: 0.32,
        523600: 0.35,
    }
    tiers_2022 = {
        10275: 0.10,
        41775: 0.12,
        89075: 0.22,
        170050: 0.24,
        215950: 0.32,
        539900: 0.35,
    }
    return tiered_tax_rate(tiers_2022, gains)


def tax_for_long_term_capital(gains):
    tiers_2021 = {
        0: 0.00,
        40400: 0.15,
        445850: 0.20,
    }
    tiers_2022 = {
        0: 0.00,
        41675: 0.15,
        459750: 0.20,
    }
    return tiered_tax_rate(tiers_2022, gains)


def tiered_tax_rate(tiers, gains):
    thresholds = sorted(tiers.keys())
    tax = 0
    for i, threshold in enumerate(thresholds):
        taxable_amount = gains
        if i+1 < len(thresholds):
            taxable_amount -= thresholds[i+1]
        if gains > threshold:
            taxable_amount -= threshold

        tax_rate = tiers[threshold]
        tax += taxable_amount * tax_rate

    return tax


def spx_options_tax(gains):
    long_term_gains = 0.6 * gains
    short_term_gains = 0.4 * gains

    return tax_for_long_term_capital(long_term_gains) + tax_for_short_term_capital(short_term_gains)


def main():
    initial_account_value = 50 * 1000
    cumulative_gains = 0

    nweeks_off = 2 * 4  # take 2 months off per year
    for week in range(52 - nweeks_off):
        # for now, ignore when SPX expiry != SPXW
        for day in ["mon", "wed", "fri"]:
            buying_power = initial_account_value + cumulative_gains
            cumulative_gains += (buying_power * 0.03)

    cumulative_profits = cumulative_gains - spx_options_tax(cumulative_gains)

    print("Initial account value:", sprint_dollars(initial_account_value))
    print("Cumulative profits:", sprint_dollars(cumulative_profits))
    print("Total account value:", sprint_dollars(initial_account_value + cumulative_profits))


if __name__ == "__main__":
    main()
