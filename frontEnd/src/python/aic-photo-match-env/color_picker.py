'''Take in a user submitted image file (jpg, jpeg, or png), analyize dominant color, search csv for
another image with the user dominant color within the top three dominant colors, return results as
json'''

import sys
import numpy
import pandas
from colorthief import ColorThief #installed

def dominant_color(image_path):
    '''Function to get dominant color from uploaded photo'''
    c_t = ColorThief(image_path)
    dom_col = c_t.get_color(quality=8)
    red = dom_col[0]
    green = dom_col[1]
    blue = dom_col[2]
    return {"user_img_colors" : {
        "red" : red,
        "green" : green,
        "blue" : blue
    }
            }

def euclidean_distance(row1, row2):
    '''Calculate Euclidian distance between two vectors'''
    distance = 0.0
    for i in range(len(row1)-1):
        distance += (row1[i] - row2[i])**2
        return numpy.sqrt(distance)

def get_neighbors(train, test_row, num_neighbors):
    '''Get nearest neighbor'''
    distances = list()
    for train_row in train:
        dist = euclidean_distance(test_row, train_row)
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(num_neighbors):
        neighbors.append(distances[i][0])
        return neighbors

def lambda_handler(event):
    '''Take JSON input from user image and match to AIC painting'''
    # User Colors
    user_red = event['user_img_colors']['red']
    user_green = event['user_img_colors']['green']
    user_blue = event['user_img_colors']['blue']
    user_colors = [user_red, user_green, user_blue]
    # Run function to get closet painting
    neighbors = get_neighbors(aic_colors, user_colors, 1)
    neighborsred = [neighbors[0][0]]
    neighborsgreen = [neighbors[0][1]]
    neighborsblue = [neighbors[0][2]]
    # Get URL for closest painting and return color and URL info
    match_url = df[(df['red'].isin(neighborsred)) &
                   (df['green'].isin(neighborsgreen)) &
                   (df['blue'].isin(neighborsblue))]['url'].tolist()
    return {
        "aic colors" :
        {"red" : int(neighborsred[0]),
         "green" : int(neighborsgreen[0]),
         "blue" : int(neighborsblue[0]),
         "url" : str(match_url[0])
         },
        "user colors" :
        {"user_red" : user_red,
         "user_green" : user_green,
         "user_blue" : user_blue
         }
    }

# need to load the file into the script
df = pandas.read_csv('aic_color_final_2-1.csv')
aic_colors = df[['red', 'green', 'blue']].values

# call the script
print(lambda_handler(dominant_color(sys.argv[1])))
