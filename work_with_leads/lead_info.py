webhook_url = 'https://b24-6v5j8c.bitrix24.ru/rest/1/dq0qu52knpxu26rn/crm.lead.add.json'
webhook_url2 = "https://b24-5ui6b2.bitrix24.ru/rest/1/7byl8jii47a6pdbb/crm.lead.add.json"


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
