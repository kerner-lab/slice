/**
 * @fileoverview Downloads the S2 Images given the coordinates of the region of interest
 * @param {ee.Geometry} region The region of interest
 * @param {string} output_path The path where the images will be downloaded
 * @param {string} start_date The start date of the images to download
 * 
 */


var region =  ee.Geometry.Polygon([[
    [0.817637200222991, 43.71880490494066],
    [2.0768077353481242, 43.71880490494066],
    [2.0768077353481242, 42.347232877570896],
    [0.817637200222991, 42.347232877570896]
]]);
var output_path = 'data/images';
var start_date = '2021-01-01';
var end_date = '2021-12-31';
    
var s2Clouds = ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY');

var BANDS = [
    "B2",
    "B3",
    "B4",
    "B5",
    "B6",
    "B7",
    "B8",
    "B8A",
    "B9",
    "B11",
    "B12"
]


//var region = ee.Geometry.Rectangle(
//    {coords: [-0.89,46.08,0.77,47.3], geodesic: false});
Map.centerObject(region, 9);
Map.addLayer(region);
/**
 * Function to mask clouds using the Sentinel-2 QA band
 * @param {ee.Image} image Sentinel-2 image
 * @return {ee.Image} cloud masked Sentinel-2 image
 */
function maskS2clouds(image) {
    var qa = image.select('QA60');

    // Bits 10 and 11 are clouds and cirrus, respectively.
    var cloudBitMask = 1 << 10;
    var cirrusBitMask = 1 << 11;

    // Both flags should be set to zero, indicating clear conditions.
    var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
        .and(qa.bitwiseAnd(cirrusBitMask).eq(0));

    return image.updateMask(mask).divide(10000);
}

function addLatLong(image) {
    var latlon = ee.Image.pixelLonLat()//.reproject(proj)
    return image.addBands(latlon.select('longitude','latitude'))

}

// Map the function over one year of data and take the median.
// Load Sentinel-2 TOA reflectance data.
var region_images = ee.ImageCollection('COPERNICUS/S2')
                .filterDate(start_date, end_date)
                .filterBounds(region)
                .map(function(image){return image.clip(region)})
                // Pre-filter to get less cloudy granules.
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                .map(addLatLong)
                .map(maskS2clouds);
    
var region_images = region_images.median();


var rgbVis = {
    min: 0.0,
    max: 0.2,
    bands: ['B4', 'B3', 'B2'],
};

Map.addLayer(
    region_images,
    rgbVis,
    '2021-France', true
);
  

// Save the images to disk
Export.image.toDrive({
    image: region_images,
    description: '2021-France',
    scale: 10
})