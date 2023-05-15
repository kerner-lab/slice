import planet
import asyncio
from get_image_ids import get_image_ids


geojson_geometry = {
    "type": "Polygon",
    "coordinates": [
        [
            [-1.7561090783389053, 43.68447623835922],
            [0.34560151015968726, 43.68447623835922],
            [0.34560151015968726, 42.691920066961416],
            [-1.7561090783389053, 42.691920066961416]
        ]
    ]
}



# PLANET_API_KEY = 'PLAK510abcf8ded84aaba5a07e2b577020b4'
PLANET_API_KEY = 'PLAKc7c90a1810c14ddd9e86b1266e9def6e'

auth = planet.Auth.from_key(PLANET_API_KEY)
image_ids = get_image_ids(geojson_geometry, PLANET_API_KEY)

# print(image_ids)

# Google Earth Engine configuration
cloud_config = planet.order_request.google_earth_engine(
    project='ee-mnthnaidsf', collection='ps-fra-21')
# Order delivery configuration
delivery_config = planet.order_request.delivery(cloud_config=cloud_config)

# Product description for the order request
data_products = [
    planet.order_request.product(item_ids=image_ids,
                                 product_bundle='analytic_sr_udm2',
                                 item_type='PSScene')
]

# Build the order request
image_order = planet.order_request.build_request(name='france-2021-2',
                                                products=data_products,
                                                delivery=delivery_config)

idx = ''
# Create and deliver the order
async def create_and_deliver_order(order_request, client):
    '''Create and deliver an order.

    Parameters:
        order_request: An order request
        client: An Order client object
    '''
    with planet.reporting.StateBar(state='creating') as reporter:
        # Place an order to the Orders API
        order = await client.create_order(order_request)
        idx = order['id']
        reporter.update(state='created', order_id=order['id'])
        # Wait while the order is being completed
        await client.wait(order['id'],
                          callback=reporter.update_state,
                          max_attempts=0)

    # Grab the details of the orders
    order_details = await client.get_order(order_id=order['id'])

    return order_details

async def main():
    async with planet.Session(auth=auth) as ps:
        # The Orders API client
        client = ps.client('orders')
        # Create the order and deliver it to GEE
        order_details = await create_and_deliver_order(image_order, client)
        print(await client.get_order(order_id))

asyncio.run(main())

print(order_details)


"""
20211222_105651_61_2402, 20211222_105649_32_2402, 20211222_105647_02_2402, 20211222_105644_73_2402, 20211222_105642_43_2402, 20211222_105640_14_2402, 20211222_105637_84_2402, 20211222_105635_55_2402, 20211222_105633_25_2402, 20211222_105038_74_2424, 20211222_105036_44_2424, 20211222_105034_13_2424, 20211222_105031_83_2424, 20211222_105029_52_2424, 20211222_105027_22_2424, 20211222_105024_91_2424, 20211222_105022_61_2424, 20211222_104739_88_240a, 20211222_104737_53_240a, 20211222_104735_18_240a, 20211222_104732_84_240a, 20211222_104730_49_240a, 20211222_104728_14_240a, 20211222_104725_79_240a, 20211222_104723_44_240a, 20211222_104721_09_240a, 20211222_103412_1038, 20211222_103411_1038, 20211222_103410_1038, 20211222_103409_1038, 20211222_103408_1038, 20211222_103407_1038, 20211222_103406_1038, 20211222_103405_1038, 20211222_103404_1038, 20211222_103403_1038, 20211222_103402_1038, 20211222_103401_1038, 20211222_103400_1038, 20211222_103359_1038, 20211222_103358_1038, 20211222_103357_1038, 20211222_103356_1038, 20211222_103220_1025, 20211222_103219_1025, 20211222_103218_1025, 20211222_103217_1025, 20211222_103216_1025, 20211222_103215_1025, 20211222_103214_1025, 20211222_103213_1025, 20211222_103212_1025, 20211222_103211_1025, 20211222_103210_1025, 20211222_103209_1025, 20211222_103208_1025, 20211222_103207_1025, 20211222_103206_1025, 20211222_103205_1025, 20211222_103204_1025, 20211222_103203_1025, 20211222_102456_1003, 20211222_102455_1003, 20211222_102454_1003, 20211222_102453_1003, 20211222_102452_1003, 20211222_102451_1003, 20211222_102450_1003, 20211222_102449_1003, 20211222_102448_1003, 20211222_102447_1003, 20211222_102446_1003, 20211222_100332_98_2463, 20211222_100330_68_2463, 20211222_100328_38_2463, 20211222_100326_08_2463, 20211222_100323_78_2463, 20211222_100321_48_2463, 20211222_095955_75_106a, 20211222_095954_25_106a, 20211222_095952_75_106a, 20211222_095951_25_106a, 20211222_095949_75_106a, 20211222_095948_25_106a, 20211222_095946_75_106a, 20211222_095945_25_106a, 20211222_095943_75_106a, 20211222_095942_25_106a, 20211222_095940_75_106a, 20211222_095939_25_106a
"""