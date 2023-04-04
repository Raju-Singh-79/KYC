from ..database_models.client_super_master import client_super_master


def all_client_code():
    client_data = client_super_master.objects.all().values_list('clientCode', flat=True)
    return client_data
