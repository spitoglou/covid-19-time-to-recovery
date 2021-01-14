# import matplotlib.pyplot as plt
from statistics import mean, stdev
import pprint
import pandas
from loguru import logger


def load_remote_data(category: str) -> pandas.DataFrame:
    url = "https://raw.githubusercontent.com/" \
        "CSSEGISandData/COVID-19/master/" \
        "csse_covid_19_data/csse_covid_19_time_series/" \
        "time_series_covid19_{}_global.csv".format(category)
    df = pandas.read_csv(url)
    df.set_index(["Country/Region"], inplace=True)
    # calculate sums for each country/region (distorts the spatial data (lat, long))
    df = df.groupby(level="Country/Region").sum()
    return df


def create_new_dict(series):
    counter = 0
    new_dict = {}
    for date, value in series.items():
        # pass
        diff = value - counter
        # print(date, value)
        new_dict[date] = diff
        counter = value
    return new_dict


def new_aggregated_dicts(country: str) -> dict:
    if country == 'Global':
        confirmed_country = confirmed.sum()[3:]
        deaths_country = deaths.sum()[3:]
        recovered_country = recovered.sum()[3:]
    else:
        confirmed_country = confirmed.loc[country][3:]
        deaths_country = deaths.loc[country][3:]
        recovered_country = recovered.loc[country][3:]

    new_confirmed_dict = create_new_dict(confirmed_country)

    new_deaths_dict = create_new_dict(deaths_country)

    new_recovered_dict = create_new_dict(recovered_country)
    return {
        'confirmed': new_confirmed_dict,
        'deaths': new_deaths_dict,
        'recovered': new_recovered_dict,
        'no_days': len(new_confirmed_dict)
    }


def create_distinct(dictionary: dict) -> list:
    result = []
    day_index = 0
    for key, value in dictionary.items():
        day_index = day_index + 1
        if value == 0:
            pass
        for i in range(int(value)):
            result.append(day_index)
    return result


def interval_sets(confirmed, deaths, recovered, no_days, verbose=True):
    continue_loop = True
    intervals = []
    unmatched_intervals = []
    while continue_loop:
        if verbose:
            print('-' * 30)
            print('Remaining Confirmed: {}'.format(len(confirmed)))
            print('Remaining Deaths: {}'.format(len(deaths)))
            print('Remaining Recovered: {}'.format(len(recovered)))
        if len(confirmed) > 0:
            confcase = confirmed.pop(0)
            if verbose:
                print('Current Confirmed Case - Day {}'.format(confcase))
            if len(deaths) > 0 and len(recovered) > 0:
                if verbose:
                    print('Both deaths and recoveries exist')
                if min(deaths) > min(recovered):
                    reccase = recovered.pop(0)
                    if verbose:
                        print('Earliest existing recovery - Day {}'.format(reccase))
                    to_append = reccase - confcase
                    intervals.append(to_append)
                else:
                    deathcase = deaths.pop(0)
                    if verbose:
                        print('Earliest existing death - Day {}'.format(deathcase))
                    to_append = deathcase - confcase
                    intervals.append(to_append)
            elif len(deaths) > 0 and len(recovered) == 0:
                deathcase = deaths.pop(0)
                if verbose:
                    print('Earliest existing death - Day {}'.format(deathcase))
                to_append = deathcase - confcase
                intervals.append(to_append)
            elif len(deaths) == 0 and len(recovered) > 0:
                reccase = recovered.pop(0)
                if verbose:
                    print('Earliest existing recovery - Day {}'.format(reccase))
                to_append = reccase - confcase
                intervals.append(to_append)

            else:
                if verbose:
                    print(
                        'Unmatched confirmed case \nTotal No of days : {}'.format(no_days))
                to_append = no_days - confcase
                unmatched_intervals.append(to_append)
            if verbose:
                print('Appended value : {}'.format(to_append))
        else:
            continue_loop = False

        # print(confcase)
    return {
        'matched': intervals,
        'unmatched': unmatched_intervals
    }


def run_country(country: str, print_case_by_case=False, print_sets=False):
    def replace_if_less(input_array, threshold_value):
        new_array = []
        for item in input_array:
            if item < threshold_value:
                new_array.append(threshold_value)
            else:
                new_array.append(item)
        return new_array
    new_cases = new_aggregated_dicts(country)
    # logger.info(new_cases['confirmed'])
    # logger.info(new_cases['no_days'])

    confirmed_time_array = create_distinct(new_cases['confirmed'])
    deaths_time_array = create_distinct(new_cases['deaths'])
    recovered_time_array = create_distinct(new_cases['recovered'])
    no_days = new_cases['no_days']

    results = interval_sets(confirmed_time_array,
                            deaths_time_array,
                            recovered_time_array,
                            no_days,
                            verbose=print_case_by_case)

    matched_intervals = results['matched']
    unmatched_intervals = results['unmatched']

    unmatched_new_intervals = replace_if_less(
        unmatched_intervals, mean(matched_intervals))

    complete = matched_intervals + unmatched_new_intervals
    # print(len(matched_intervals),
    #       matched_intervals,
    #       len(unmatched_intervals),
    #       unmatched_intervals)
    if print_sets:
        print('Matched Intervals Set (len={}'.format(len(matched_intervals)))
        print(matched_intervals)
        print('UnMatched Intervals Set (len={}'.format(len(unmatched_intervals)))
        print(unmatched_intervals)
        print('UnMatched New Intervals Set (len={}'.format(
            len(unmatched_new_intervals)))
        print(unmatched_new_intervals)
        print('Complete Set (len={}'.format(
            len(complete)))
        print(complete)

    # logger.info(mean(matched_intervals))
    # logger.info(stdev(matched_intervals))
    return {
        # 'matched_set': matched_intervals,
        # 'unmatched_set': unmatched_intervals,
        'no_days': no_days,
        'matched_len': len(matched_intervals),
        'matched_mean': mean(matched_intervals),
        'matched_stdev': stdev(matched_intervals),
        'unmatched_len': len(unmatched_intervals),
        'unmatched_mean': mean(unmatched_intervals),
        'unmatched_stdev': stdev(unmatched_intervals),
        'unmatched_new_len': len(unmatched_new_intervals),
        'unmatched_new_mean': mean(unmatched_new_intervals),
        'unmatched_new_stdev': stdev(unmatched_new_intervals),
        'complete_len': len(complete),
        'complete_mean': mean(complete),
        'complete_stdev': stdev(complete),
    }


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    confirmed = load_remote_data('confirmed')
    deaths = load_remote_data('deaths')
    recovered = load_remote_data('recovered')

    # logger.info(recovered)
    countries = [
        'China',
        'Netherlands',
        'France',
        'US',
        'Spain',
        'United Kingdom',
        'Iran',
        'Germany',
        'Italy',
        'Greece',
        'Global'
    ]
    data = {}
    for country in countries:
        logger.info('Starting Country ' + country)
        results = run_country(country)
        data[country] = results
        logger.info('Finished Country ' + country)
    pp.pprint(data)
    result_dataframe = pandas.DataFrame.from_dict(data, orient='index')
    print(result_dataframe)
    result_dataframe.to_excel("results.xlsx")
