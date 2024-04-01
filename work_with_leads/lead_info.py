def lead_data_func(name, phone_number, email, comment):
    lead_data = {
        'fields': {
            "NAME": name,
            "STATUS_ID": "NEW",
            "OPENED": "Y",
            "ASSIGNED_BY_ID": 1,
            "CURRENCY_ID": "RUB",
            "PHONE": [{"VALUE": phone_number,
                       "VALUE_TYPE": "WORK"}],
            "EMAIL": [{"VALUE": email,
                       "VALUE_TYPE": "WORK"}],
            "COMMENTS": comment
        },
        'params': {
            "REGISTER_SONET_EVENT": "Y"
        }
    }
    return lead_data
