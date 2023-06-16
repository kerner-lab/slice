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