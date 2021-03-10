import argparse

import pandas as pd
import requests


def main():
    # Run like `python get_who_theme.py "Overweight and Obesity"`
    parser = argparse.ArgumentParser()
    parser.add_argument("theme_name")
    args = parser.parse_args()

    requested_indicators = pd.read_csv("requestedIndicators.csv")

    theme = get_theme(args.theme_name, requested_indicators)
    transform_theme(theme)
    write_excel(theme)
    write_csv(theme)


def get_theme(theme_name: str, requested_indicators: pd.DataFrame) -> pd.DataFrame:
    theme = pd.DataFrame()

    theme_indicators = requested_indicators[
        (requested_indicators["Theme"] == theme_name)
        & (requested_indicators["HostingReference"] == "WHO")
    ]
    theme_indicators = theme_indicators.drop_duplicates("IndicatorCodeDS")

    for _, indicator in theme_indicators.iterrows():
        indicator_data = get_indicator_data(indicator["IndicatorCodeDS"])
        indicator_values = get_indicator_values(indicator_data, indicator)
        theme = theme.append(indicator_values)

    return theme


def get_indicator_data(indicator_code: str) -> list:
    api_url = f"https://ghoapi.azureedge.net/api/{indicator_code}"
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()["value"]


def get_indicator_values(indicator_data: list, indicator: pd.Series) -> pd.DataFrame:
    # TODO: Add rows for each item in  `indicator_data`, ala `retrieveIndData`
    # `pd.DataFrame.from_records` might be a much simpler approach
    indicator_values = pd.DataFrame(...)

    # TODO: Add `indicator` elements to `indicator_values`
    # See lines 99-105 of `allWHOData`

    return indicator_values


def transform_theme(theme: pd.DataFrame) -> None:
    # TODO: Apply all the necessary cleaning and transformation to `theme`
    pass


def write_excel(theme: pd.DataFrame) -> None:
    pass


def write_csv(theme: pd.DataFrame) -> None:
    pass


if __name__ == "__main__":
    main()
