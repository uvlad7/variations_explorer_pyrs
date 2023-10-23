import pytest

from variations_explorer_pyrs import VariationsGraph


def create_graph(data):
    vg = VariationsGraph()
    for prod_md5, variations_md5 in data:
        vg.insert(prod_md5, variations_md5)
    return vg


def hex_str(val):
    return f'{val:x}'


@pytest.fixture
def full_group():
    return create_graph([
        ("1", ["2", "3"]),
        ("2", ["1", "3"]),
        ("3", ["1", "2"]),
    ])


@pytest.fixture
def single_prods():
    return create_graph([
        ("1", []),
        ("2", []),
        ("3", []),
    ])


@pytest.fixture
def partial_group():
    return create_graph([
        ("1", ["2", "3"]),
        ("2", ["1", "3"]),
        ("3", ["1", "2"]),
    ])


@pytest.fixture
def loops():
    return create_graph([
        ("1", ["1"]),
        ("2", ["2", "3"]),
        ("3", ["2", "3"]),
    ])


@pytest.fixture
def duplicates():
    return create_graph([
        ("1", ["2", "3"]),
        ("1", ["1", "3", "4"]),
        ("2", ["1", "3"]),
        ("3", ["1", "2"]),
    ])


@pytest.fixture
def source_node():
    return create_graph([
        ("1", ["2"]),
        ("2", ["1"]),
        ("3", ["1", "2"])  # source node
    ])


@pytest.fixture
def virtual_source_node():
    return create_graph([
        ("1", ["2"]),
        # 2 - virtual node, that connects 1 and 3 source nodes
        ("3", ["2", "4"]),
        ("4", ["2"])
    ])


@pytest.fixture
def db_data():
    # 51006824,51006825,51484778,51484781,60415063,60415065,81895007,81895008,113366845,174767834
    # return {
    #     "locations": [
    #         {
    #             "product_id": 51006824,
    #             "url_key": "0x62AAA1D3AB54318E8281F4B96A5A05F3"
    #         },
    #         {
    #             "product_id": 51006825,
    #             "url_key": "0x62AAA1D3AB54318E8281F4B96A5A05F3"
    #         },
    #         {
    #             "product_id": 51484778,
    #             "url_key": "0x058CC2D6F3129742D8FDD8FF7EEA178E"
    #         },
    #         {
    #             "product_id": 51484781,
    #             "url_key": "0x058CC2D6F3129742D8FDD8FF7EEA178E"
    #         },
    #         {
    #             "product_id": 60415063,
    #             "url_key": "0x86480EBF8E1E7458F4E4E3ABE1E9C22F"
    #         },
    #         {
    #             "product_id": 60415065,
    #             "url_key": "0x86480EBF8E1E7458F4E4E3ABE1E9C22F"
    #         },
    #         {
    #             "product_id": 81895007,
    #             "url_key": "0x77BFCBEEB0BE1847BBDBD1AE44D2786A"
    #         },
    #         {
    #             "product_id": 81895008,
    #             "url_key": "0x77BFCBEEB0BE1847BBDBD1AE44D2786A"
    #         },
    #         {
    #             "product_id": 113366845,
    #             "url_key": "0xD976C4251C89CB5AE7E411C18C6B23B7"
    #         },
    #         {
    #             "product_id": 174767834,
    #             "url_key": "0x62256ECDDE3F2411B6492A4997C26801"
    #         }
    #     ],
    #     "product_variations": [
    #         {
    #             "product_id": 51006824,
    #             "urls_md5": "[\"d254e7cf6e8b1f0b1463b3dc631021a6\", "
    #                         "\"c4c94c6f80c8e05a1db252249372c655\", "
    #                         "\"f7940f60a25f846ed1aca767bc2d4560\", "
    #                         "\"de1bc963c94a59d5290d91d323e4cbbf\"]"
    #         },
    #         {
    #             "product_id": 51006825,
    #             "urls_md5": "[\"d254e7cf6e8b1f0b1463b3dc631021a6\", "
    #                         "\"c4c94c6f80c8e05a1db252249372c655\", "
    #                         "\"f7940f60a25f846ed1aca767bc2d4560\", "
    #                         "\"de1bc963c94a59d5290d91d323e4cbbf\"]"
    #         },
    #         {
    #             "product_id": 51484778,
    #             "urls_md5": "[\"db369f4e7f738987f13b401ca696a935\"]"
    #         },
    #         {
    #             "product_id": 51484781,
    #             "urls_md5": "[\"db369f4e7f738987f13b401ca696a935\"]"
    #         },
    #         {
    #             "product_id": 60415063,
    #             "urls_md5": "[\"e4954a95da6519c91d955e63d431968a\", "
    #                         "\"331bf0861640ab91b31c68b9efa36e86\", "
    #                         "\"c9f177baa15768774449cee754e62cc3\", "
    #                         "\"a4e18da69e6f55101313524d821f8ed4\"]"
    #         },
    #         {
    #             "product_id": 60415065,
    #             "urls_md5": "[\"e4954a95da6519c91d955e63d431968a\", "
    #                         "\"331bf0861640ab91b31c68b9efa36e86\", "
    #                         "\"c9f177baa15768774449cee754e62cc3\", "
    #                         "\"a4e18da69e6f55101313524d821f8ed4\"]"
    #         },
    #         {
    #             "product_id": 81895007,
    #             "urls_md5": "[\"55be2a60b7ef26b2de48685de2592eb0\"]"
    #         },
    #         {
    #             "product_id": 81895008,
    #             "urls_md5": "[\"55be2a60b7ef26b2de48685de2592eb0\"]"
    #         },
    #         {
    #             "product_id": 113366845,
    #             "urls_md5": "[\"900d37cf8c6ab074aa2592a27aa8aa6f\", "
    #                         "\"b24398c72c9d2e6d2dbf18ae352bf7ec\"]"
    #         },
    #         {
    #             "product_id": 174767834,
    #             "urls_md5": "[\"f36cfd7c791957988b71e021ea57380d\", "
    #                         "\"c830b29f16cb0d439d9d6bddca501caa\", "
    #                         "\"9594aea11df64357b63db20ac4d6c628\", "
    #                         "\"f8d001c35da11ef07d60e9d63f1ed202\", "
    #                         "\"d939bb6e0c99e55be900c6f62ae95b14\", "
    #                         "\"9b7d42e622f6fcb0d6f1e5844d8dda1d\", "
    #                         "\"56abbc599d73ae32d86b21f249f7e5cf\", "
    #                         "\"9b4a460d3b900315fe54dd94ef78b161\", "
    #                         "\"9eed7659034d0e02d7cff5f96aa2077a\", "
    #                         "\"99cf933ceeaaac4be99bcef0ce74fa0a\", "
    #                         "\"5d9649f3fd618c2a9cb77424af58bd84\", "
    #                         "\"91e59f056d1c88af27a22752a86ec33c\", "
    #                         "\"d5445229ff4b765d2ee61db34765a081\", "
    #                         "\"274123685a7f0f3a92f83f87402735a6\"]"
    #         }
    #     ]
    # }
    return {
        # product_id, url_key
        # int.from_bytes((bytearray(b'b\xaa\xa1\xd3\xabT1\x8e\x82\x81\xf4\xb9jZ\x05\xf3')),
        # byteorder='big')
        # == 0x62AAA1D3AB54318E8281F4B96A5A05F3
        # vg.db_data_insert(bytearray((42).to_bytes(16, byteorder='big')), b'["10"]')
        # vg.db_data_insert([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42], b'["10"]')
        #  vg.db_data_insert(bytearray(b'b\xaa\xa1\xd3\xabT1\x8e\x82\x81\xf4\xb9jZ\x05\xf3'),
        #  b'["7621e62b00ce610586cd76ddfdb0f35c", "418fbc5c442f308f07f482730b1d601d", '
        #  b'"07f204c36e6585ea9322a3c903ad134f", "92ef390f514e3d638d5a41e3d6197f41"]')
        "locations": [
            (51006824, bytearray(b'b\xaa\xa1\xd3\xabT1\x8e\x82\x81\xf4\xb9jZ\x05\xf3')),
            (51006825, bytearray(b'b\xaa\xa1\xd3\xabT1\x8e\x82\x81\xf4\xb9jZ\x05\xf3')),
            (51484778, bytearray(b'\x05\x8c\xc2\xd6\xf3\x12\x97B\xd8\xfd\xd8\xff~\xea\x17\x8e')),
            (51484781, bytearray(b'\x05\x8c\xc2\xd6\xf3\x12\x97B\xd8\xfd\xd8\xff~\xea\x17\x8e')),
            (60415063, bytearray(b'\x86H\x0e\xbf\x8e\x1etX\xf4\xe4\xe3\xab\xe1\xe9\xc2/')),
            (60415065, bytearray(b'\x86H\x0e\xbf\x8e\x1etX\xf4\xe4\xe3\xab\xe1\xe9\xc2/')),
            (81895007, bytearray(b'w\xbf\xcb\xee\xb0\xbe\x18G\xbb\xdb\xd1\xaeD\xd2xj')),
            (81895008, bytearray(b'w\xbf\xcb\xee\xb0\xbe\x18G\xbb\xdb\xd1\xaeD\xd2xj')),
            (113366845, bytearray(b'\xd9v\xc4%\x1c\x89\xcbZ\xe7\xe4\x11\xc1\x8ck#\xb7')),
            (174767834, bytearray(b'b%n\xcd\xde?$\x11\xb6I*I\x97\xc2h\x01'))
        ],
        # product_id, urls_keys
        "product_variations": [
            (51006824,
             b'["7621e62b00ce610586cd76ddfdb0f35c", "418fbc5c442f308f07f482730b1d601d", '
             b'"07f204c36e6585ea9322a3c903ad134f", "92ef390f514e3d638d5a41e3d6197f41"]'),
            (51006825,
             b'["7621e62b00ce610586cd76ddfdb0f35c", "418fbc5c442f308f07f482730b1d601d", '
             b'"07f204c36e6585ea9322a3c903ad134f", "92ef390f514e3d638d5a41e3d6197f41"]'),
            (51484778, b'["335fef298b7fbd2c212bbbdec037e5c6"]'),
            (51484781, b'["335fef298b7fbd2c212bbbdec037e5c6"]'),
            (60415063,
             b'["23301b3420084b461cb1369e31d1e0b7", "bf93560f5410fb959deb6dc3d1455c46", '
             b'"bbcd4a541e0e0889171a10ddfe19fbf1", "cf98d8b8c143bd669a7a939d33443b4c"]'),
            (60415065,
             b'["23301b3420084b461cb1369e31d1e0b7", "bf93560f5410fb959deb6dc3d1455c46", '
             b'"bbcd4a541e0e0889171a10ddfe19fbf1", "cf98d8b8c143bd669a7a939d33443b4c"]'),
            (81895007, b'["fa578b039f655df101004ddef9972a0e"]'),
            (81895008, b'["fa578b039f655df101004ddef9972a0e"]'),
            (
                113366845,
                b'["a310d2c53c6d0158d755222badcf0222", "a777572383956f7eeea4ea46c92877b2"]'),
            (174767834,
             b'["f432b52bd5262979c8cf12e52c6cc081", "3b1825a4d6b274026f8080052e69433d", '
             b'"a32b5de0aae82c638bde53b31646ff1d", "cb8746dd217a76e73bc90e76360a572e", '
             b'"fd717a060b634914fabe4223db0e1b53", "d938c141d0093936df9808d507a6a8f3", '
             b'"4447bbc24f5c5407fb1feeb8ca821f29", "c70b42b816416e4fc0b2ccbea5c4d449", '
             b'"c6f7cfeb543f2d0e55cc0896ffd61ac4", "fbe335a912276a366334dc41f845ca4e", '
             b'"65366402812ab347d2d976fc0d05b345", "3bbe5b8dbecadf4b68927840592eb894", '
             b'"2e9d84a9425f47be0731fd60b831e32c", "f621114cee075913841fd75fc178d7f3"]'
             )
        ]
    }
