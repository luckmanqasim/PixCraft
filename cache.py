import json
import os
from datetime import datetime, timedelta


class ImageCache:

    def __init__(self):

        # Initiate the cache directory and json filepath
        self._cache_dir = 'cache_data'
        self._cache_file = os.path.join(self._cache_dir, 'cached_data.json')

        # If the cache directory doesnt exist, create it
        if not os.path.exists(self._cache_dir):
            os.makedirs(self._cache_dir)


    # Add timestamp to the key and oraganize the data
    def _add_time_to_data(self, image_paths, image_links):
        data = {'images': image_paths, 'links': image_links, 'timestamp': str(datetime.now())}
        return data


    # Store new data in cache
    def store_data_in_cache(self, new_key, image_paths, image_links):
        organized_data = self._add_time_to_data(image_paths, image_links)

        try:
            with open(self._cache_file, 'r') as f:
                data = json.load(f)
        except:
            # Handle the case where the file is empty or not valid JSON
            data = {}

        # Insert new data as a new key
        data[new_key] = organized_data

        with open(self._cache_file, 'w') as f:
            json.dump(data, f, indent=4)


    # Retrieve a data assoicated with a key from the JSON file and return it as a list of image paths and full image links
    def retrieve_data(self, query):

            try:
                # Look for the time stamp of the query
                with open(self._cache_file, 'r') as f:
                    cache_data = json.load(f)
                    timestamp = datetime.fromisoformat(cache_data[query]['timestamp'])

                    # Check if the cache is still valid (e.g., within 24 hours)
                    if datetime.now() - timestamp <= timedelta(hours=24):
                        path_and_link = [cache_data[query]['images'], cache_data[query]['links']]
                        return path_and_link
                    
            except (IOError, json.JSONDecodeError) as e:
                print(f'Error processing cache file: {e}')
            except KeyError:
                print('Key not Found!')
                return None


    # Remove data older than 24 hours from the JSON file
    def remove_old_data(self):
        
        try:
            with open(self._cache_file, 'r') as f:
                data = json.load(f)

            current_time = datetime.now()

            # Look for the timestamp of the data
            for key, value in list(data.items()):
                timestamp = datetime.fromisoformat(value['timestamp'])

                # Deletes the images if the timestamp is more than 24 hours old
                if current_time - timestamp > timedelta(hours=24):
                    for image in data[key]['images']:
                        os.remove(image)

                    # Deletes the directory
                    key_dir = os.path.join(self._cache_dir, key)
                    os.removedirs(key_dir)
                    del data[key]
            
            # save the new modified data into the json file
            with open(self._cache_file, 'w') as f:
                json.dump(data, f, indent=4)

        except (IOError, json.JSONDecodeError) as e:
            print(f'Error processing cache file: {e}')
        except KeyError:
            print('Key not Found!')
