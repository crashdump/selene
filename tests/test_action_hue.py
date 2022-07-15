from unittest import TestCase
import selene.logger
import plugins.actions.hue


class TestHue(TestCase):
    def test_on(self):
        h = plugins.actions.hue.Hue()
        results = h.on(config={
            'hue.Hue': {
                'duration': 30,
                'ip': '192.168.1.22',
                'secret': 'nDDyA1QBTzEMHrpvBcnudX6vXWFBQ2K4zv1ENFmq',
                "lights": [{
                        "id": 19,
                        "state": "on",
                    }]
            }
        })

        for result in results:
            print(result)

    # def test_off(self):
    #     h = plugins.actions.hue.Hue()
    #     result = h.off(config={
    #         'hue.Hue()': {
    #             'duration': 30,
    #             'ip': '192.168.1.22',
    #         }
    #     })
    #
    #     print(result)
        # assert result["current_transport_status"] == "OK"
        # assert result["current_transport_state"] in ["TRANSITIONING", "STOPPED"]


