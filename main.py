import batch_helper
import meraki
from xkcdpass import xkcd_password as xp


def __main__():

    # words that we will use to generate some actions
    random_word_list = xp.generate_wordlist(min_length=2, max_length=5)

    dashboard = meraki.DashboardAPI(suppress_logging=True)

    organization_id = "607985949695019579"  # upgrade demo org
    target_networks = dashboard.organizations.getOrganizationNetworks("607985949695019579")

    # create some action lists
    action_list_1 = list()
    action_list_2 = list()
    action_list_3 = list()
    all_actions = list()

    for network in target_networks:

        new_ssid_name = xp.generate_xkcdpassword(random_word_list, numwords=3)
        action1 = dashboard.batch.wireless.updateNetworkWirelessSsid(network['id'], 0, name=new_ssid_name)
        action_list_1.append(action1)

        new_network_name = xp.generate_xkcdpassword(random_word_list, numwords=5)
        action2 = dashboard.batch.networks.updateNetwork(network['id'], name=new_network_name)
        action_list_2.append(action2)

        action3 = dashboard.batch.networks.updateNetwork(network['id'], timeZone="America/Los_Angeles")
        action_list_3.append(action3)

    all_actions.extend(action_list_1)
    all_actions.extend(action_list_2)
    all_actions.extend(action_list_3)

    print(len(all_actions))

    test_helper = batch_helper.BatchHelper(dashboard, organization_id, all_actions, linear_new_batches=True, actions_per_new_batch=50)

    test_helper.prepare()
    test_helper.generate_preview()
    test_helper.execute()

    print(f'helper status is {test_helper.status}')

    batches_report = dashboard.organizations.getOrganizationActionBatches(organization_id)
    new_batches_statuses = [{'id': batch['id'], 'status': batch['status']} for batch in batches_report if batch['id'] in test_helper.submitted_new_batches_ids]
    failed_batch_ids = [batch['id'] for batch in new_batches_statuses if batch['status']['failed']]
    print(f'Failed batch IDs are as follows: {failed_batch_ids}')


if __name__ == "__main__":
    __main__()
