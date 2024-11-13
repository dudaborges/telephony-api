TORTOISE_ORM = {
    'connections': {
        'default': 'postgres://telephony_api:telephony_api@db:5432/telephony_api_dev'
    },
    'apps': {
        'models': {
            'models': ['database.models', 'aerich.models'],
            'default_connection': 'default',
        }
    },
}
