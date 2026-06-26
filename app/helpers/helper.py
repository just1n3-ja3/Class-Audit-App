from datetime import datetime

class app_helper:
    
    def float_parse(self, value):
        try:
            return True, float(value)
        except (ValueError, TypeError):
            return False, 0.0

    def int_parse(self, value):
        try:
            return True, int(value)
        except (ValueError, TypeError):
            return False, 0

    from datetime import datetime
    
    def try_parse_date(self, value, date_format="%Y-%m-%d"):
        try:
            return True, datetime.strptime(value, date_format)
        except (ValueError, TypeError):
            return False, None
