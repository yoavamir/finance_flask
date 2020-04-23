class FileConsts:
    def __init__(self):
        pass

    BASE_LOCATION = '../files'
    TRANSACTION_DATE = 'transaction_date'
    TRANSACTION_AMOUNT = 'transaction_amount'
    SHOP_NAME_HEBREW = 'שם בית העסק'
    SHOP_NAME = 'shop_name'


class MAXFileConsts(FileConsts):
    def __init__(self):
        FileConsts.__init__(self)

    TRANSACTION_DATE_HEBREW = 'תאריך עסקה'
    TRANSACTION_AMOUNT_HEBREW = 'סכום חיוב'


class CALFileConsts(FileConsts):
    def __init__(self):
        FileConsts.__init__(self)

    TRANSACTION_DATE_HEBREW = 'תאריך העסקה'
    TRANSACTION_AMOUNT_HEBREW = 'סכום החיוב'
