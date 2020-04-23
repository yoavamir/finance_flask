import pandas as pd
import os
from datetime import datetime
from utils.Consts import FileConsts, CALFileConsts, MAXFileConsts


def get_combined_df():

    file_2356 = CalFileUtils('2356.xlsx').prepare_df()[{FileConsts.SHOP_NAME, FileConsts.TRANSACTION_DATE,
                                                        FileConsts.TRANSACTION_AMOUNT}]
    file_9973 = CalFileUtils('2356.xlsx').prepare_df()[{FileConsts.SHOP_NAME, FileConsts.TRANSACTION_DATE,
                                                        FileConsts.TRANSACTION_AMOUNT}]
    file_5121_4048 = MaxFileUtils('5121_4048.xlsx').prepare_df()[{FileConsts.SHOP_NAME, FileConsts.TRANSACTION_DATE,
                                                                  FileConsts.TRANSACTION_AMOUNT}]
    # abroad_file_5121_4048 = MaxFileUtils('5121_4048.xlsx').prepare_abroad_df()[
    #     {FileConsts.SHOP_NAME, FileConsts.TRANSACTION_DATE, FileConsts.TRANSACTION_AMOUNT}]
    combined_df = file_2356.append([file_9973, file_5121_4048], ignore_index=True)
    return combined_df


def get_mock_df():
    mock_df = MaxFileUtils('mock.xlsx').prepare_df()[{FileConsts.SHOP_NAME, FileConsts.TRANSACTION_DATE,
                                                                  FileConsts.TRANSACTION_AMOUNT}]
    return mock_df

def get_amount_from_cell(cell):
    split = cell.split(' ')
    return split[-1]


class FileUtils:
    def __init__(self):
        self._time_format = '%m-%Y'
        self._combined_df = None

    @property
    def combined_df(self):
        if self._combined_df is None:
            self._combined_df = get_mock_df()
        return self._combined_df

    def get_months_from_file(self):
        file_df = self.combined_df.copy(deep=True)
        file_df = file_df[{FileConsts.TRANSACTION_DATE}]
        file_df.drop_duplicates(ignore_index=True, inplace=True)
        months_list = file_df.values.tolist()
        months_list.sort(key=lambda x: datetime.strptime(x[0], self._time_format))
        flat_list = [item for sublist in months_list for item in sublist]
        return flat_list

    def get_shops_from_file(self):
        file_df = self.combined_df.copy(deep=True)
        file_df = file_df[{FileConsts.SHOP_NAME}]
        file_df.drop_duplicates(ignore_index=True, inplace=True)
        file_df = file_df.groupby(FileConsts.SHOP_NAME, as_index=False).all()
        shops_list = file_df.values.tolist()
        flat_list = [item for sublist in shops_list for item in sublist]
        return flat_list

    # def get_months_from_all_files(self):
    #     cal_file = CalFileUtils('Transactions_18_04_2020.xlsx')
    #     cal_months = cal_file.get_months_from_file()
    #     max_file = MaxFileUtils('transaction-details_export_1586955191879.xlsx')
    #     max_months = max_file.get_months_from_file()
    #     in_cal_file = set(cal_months)
    #     in_max_file = set(max_months)
    #
    #     in_second_but_not_in_first = in_max_file - in_cal_file
    #     result = cal_months + list(in_second_but_not_in_first)
    #     return result


class CalFileUtils(FileUtils):
    def __init__(self, filename):
        FileUtils.__init__(self)
        self._filename = filename
        self._file_path = os.path.join(FileConsts.BASE_LOCATION, filename)
        self._file_df = pd.read_excel(self._file_path, skiprows=2, converters={})

    def prepare_df(self):
        file_df = self._file_df.copy(deep=True)
        file_df = file_df.rename(columns={CALFileConsts.TRANSACTION_DATE_HEBREW: CALFileConsts.TRANSACTION_DATE,
                                          CALFileConsts.SHOP_NAME_HEBREW: CALFileConsts.SHOP_NAME,
                                          CALFileConsts.TRANSACTION_AMOUNT_HEBREW: CALFileConsts.TRANSACTION_AMOUNT})
        file_df[CALFileConsts.TRANSACTION_DATE] = file_df[CALFileConsts.TRANSACTION_DATE].apply(lambda x: x[3:])
        file_df[CALFileConsts.TRANSACTION_DATE] = file_df[CALFileConsts.TRANSACTION_DATE]\
            .apply(lambda x: '{}-20{}'.format(x[:2], x[3:]))
        file_df = file_df.astype({FileConsts.TRANSACTION_AMOUNT: str})
        file_df[CALFileConsts.TRANSACTION_AMOUNT] = \
            file_df[CALFileConsts.TRANSACTION_AMOUNT].apply(lambda x: get_amount_from_cell(x))
        file_df = file_df.astype({FileConsts.TRANSACTION_AMOUNT: float})
        return file_df

    def get_months_from_file(self):
        file_df = self._file_df.copy(deep=True)
        file_df = file_df.rename(columns={CALFileConsts.TRANSACTION_DATE_HEBREW: CALFileConsts.TRANSACTION_DATE}
                                 )[{CALFileConsts.TRANSACTION_DATE}]
        file_df[CALFileConsts.TRANSACTION_DATE] = file_df[CALFileConsts.TRANSACTION_DATE].apply(lambda x: x[3:])
        file_df = file_df.groupby(CALFileConsts.TRANSACTION_DATE, as_index=False).all()
        file_df = file_df.applymap(lambda x: '{}-20{}'.format(x[:2], x[3:]))
        months_list = file_df.values.tolist()
        months_list.sort(key=lambda x: datetime.strptime(x[0], self._time_format))
        flat_list = [item for sublist in months_list for item in sublist]
        return flat_list


class MaxFileUtils(FileUtils):
    def __init__(self, filename):
        FileUtils.__init__(self)
        self._filename = filename
        self._file_path = '/mock.xlsx'
        self._file_df = pd.read_excel(self._file_path, skiprows=3)
        # self._abroad_file_df = pd.read_excel(self._file_path, sheet_name='עסקאות חו"ל ומט"ח', skiprows=3)

    @property
    def file_df(self):
        return self._file_df

    # @property
    # def abroad_file_df(self):
    #     return self._abroad_file_df

    def prepare_df(self):
        file_df = self._file_df.copy(deep=True)
        file_df = file_df.rename(columns={MAXFileConsts.TRANSACTION_DATE_HEBREW: MAXFileConsts.TRANSACTION_DATE,
                                          MAXFileConsts.SHOP_NAME_HEBREW: MAXFileConsts.SHOP_NAME,
                                          MAXFileConsts.TRANSACTION_AMOUNT_HEBREW: MAXFileConsts.TRANSACTION_AMOUNT})
        file_df[MAXFileConsts.TRANSACTION_DATE] = file_df[MAXFileConsts.TRANSACTION_DATE].replace(0, '07-05-2019')

        file_df[MAXFileConsts.TRANSACTION_DATE] = file_df[MAXFileConsts.TRANSACTION_DATE].apply(lambda x: x[3:])

        return file_df

    # def prepare_abroad_df(self):
    #     file_df = self._abroad_file_df.copy(deep=True)
    #     file_df = file_df.rename(columns={MAXFileConsts.TRANSACTION_DATE_HEBREW: MAXFileConsts.TRANSACTION_DATE,
    #                                       MAXFileConsts.SHOP_NAME_HEBREW: MAXFileConsts.SHOP_NAME,
    #                                       MAXFileConsts.TRANSACTION_AMOUNT_HEBREW: MAXFileConsts.TRANSACTION_AMOUNT})
    #     file_df[MAXFileConsts.TRANSACTION_DATE] = file_df[MAXFileConsts.TRANSACTION_DATE].apply(lambda x: x[3:])
    #     return file_df

    def get_months_from_file(self):
        file_df = self._file_df.copy(deep=True)
        file_df = file_df.rename(columns={MAXFileConsts.TRANSACTION_DATE_HEBREW: MAXFileConsts.TRANSACTION_DATE}
                                 )[{MAXFileConsts.TRANSACTION_DATE}]
        file_df[MAXFileConsts.TRANSACTION_DATE] = file_df[MAXFileConsts.TRANSACTION_DATE].apply(lambda x: x[3:])
        file_df = file_df.groupby(MAXFileConsts.TRANSACTION_DATE, as_index=False).all()
        months_list = file_df.values.tolist()
        months_list.sort(key=lambda x: datetime.strptime(x[0], self._time_format))
        flat_list = [item for sublist in months_list for item in sublist]
        return flat_list

    def get_shops_from_file(self):
        file_df = self._file_df.copy(deep=True)
        file_df = file_df.rename(columns={MAXFileConsts.SHOP_NAME_HEBREW: MAXFileConsts.SHOP_NAME})[
            {MAXFileConsts.SHOP_NAME}]
        file_df = file_df.groupby(FileConsts.SHOP_NAME, as_index=False).all()
        shops_list = file_df.values.tolist()
        flat_list = [item for sublist in shops_list for item in sublist]
        return flat_list


if __name__ == '__main__':
    a = get_mock_df()
    print(1)
