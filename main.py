import customtkinter
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageTk
import pixabay.core
import requests
import os
from dotenv import load_dotenv
from cache import ImageCache


# File containing the API KEY
def configure():
    load_dotenv()


# Set customtkinter default theme
customtkinter.set_appearance_mode('System')  # Modes: 'System' (standard), 'Dark', 'Light'
customtkinter.set_default_color_theme('blue')  # Themes: 'blue' (standard), 'green', 'dark-blue'


class App(customtkinter.CTk):

    def __init__(self):

        super().__init__()

        # run the function to load up the API key
        configure()

        # initialize the Cache
        self.cache = ImageCache()

        # configure window
        self.title('Image Editor')
        self.geometry(f'{1100}x{580}')

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=14)
        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        # right sidebar frame with buttons
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text='Image Editor', font=customtkinter.CTkFont(size=20, weight='bold'))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text='Import Image', command=self.load_image)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text='Save Image As', command=self.save_image_as)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text='Save Image', command=self.save_image)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)

        self.undo_button = customtkinter.CTkButton(self.sidebar_frame, text='Undo', command=self.undo)
        self.undo_button.grid(row=4, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text='Appearance Mode:', anchor='w')
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=['Light', 'Dark', 'System'],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text='UI Scaling:', anchor='w')
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=['80%', '90%', '100%', '110%', '120%'],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


        # create the image path label at the botton of the app
        self.path_label = customtkinter.CTkLabel(self, text='')
        self.path_label.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky='nsew')


        # create canvas for image display
        self.canvas = customtkinter.CTkCanvas(self, bg='#242424', bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=1, rowspan=3, padx=(20, 0), pady=(20, 0), sticky='nsew')


        # create left sidebar with tabview
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=2, rowspan=3, padx=(20, 20), pady=(20, 0), sticky='nsew')
        self.tabview.add('Filters')
        self.tabview.add('Enhance')
        self.tabview.add('Pixabay')


        # configure grid of individual tabs
        self.tabview.tab('Filters').grid_columnconfigure(0, weight=1)  
        self.tabview.tab('Enhance').grid_columnconfigure(0, weight=1)
        self.tabview.tab('Pixabay').grid_columnconfigure(0, weight=2)
        self.tabview.tab('Pixabay').grid_columnconfigure(1, weight=1)
        self.tabview.tab('Pixabay').grid_rowconfigure(1, weight=1)


        # create filters tab
        self.filters_option_label = customtkinter.CTkLabel(self.tabview.tab('Filters'), text='Filters')
        self.filters_option_label.grid(row=0, column=0, padx=20, pady=10)

        self.filters_option = customtkinter.CTkOptionMenu(self.tabview.tab('Filters'), dynamic_resizing=False,
                                                        values=['Blur', 'Contour', 'Detail', 'Edge Enhance', 'Emboss', 'Sharpen', 'Smooth', 'None'], command=self.filter_selected)
        self.filters_option.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.colors_option_label = customtkinter.CTkLabel(self.tabview.tab('Filters'), text='Colors')
        self.colors_option_label.grid(row=2, column=0, padx=20, pady=10)

        self.colors_option = customtkinter.CTkOptionMenu(self.tabview.tab('Filters'),
                                                    values=['Black and White', 'Invert', 'Equalize', 'None'], command=self.colour_selected)
        self.colors_option.grid(row=3, column=0, padx=20, pady=(10, 10))

        self.transform_label = customtkinter.CTkLabel(self.tabview.tab('Filters'), text='Transform')
        self.transform_label.grid(row=4, column=0, padx=20, pady=10)

        self.flip_button = customtkinter.CTkButton(self.tabview.tab('Filters'), text='Flip',
                                                           command=self.flip_image)
        self.flip_button.grid(row=5, column=0, padx=20, pady=(10, 10))

        self.mirror_button = customtkinter.CTkButton(self.tabview.tab('Filters'), text='Mirror',
                                                           command=self.mirror_image)
        self.mirror_button.grid(row=6, column=0, padx=20, pady=(10, 10))


        # create enchancements tab
        self.box_blur_label = customtkinter.CTkLabel(self.tabview.tab('Enhance'), text='Box Blur')
        self.box_blur_label.grid(row=0, column=0, padx=20, pady=10)

        self.box_blur_slider = customtkinter.CTkSlider(self.tabview.tab('Enhance'), from_=0, to=10, number_of_steps=10, command=self.box_blur)
        self.box_blur_slider.grid(row=1, column=0, padx=(10, 10), pady=(0, 10), sticky='ew')
        
        self.gauss_blur_label = customtkinter.CTkLabel(self.tabview.tab('Enhance'), text='Gaussian Blur')
        self.gauss_blur_label.grid(row=2, column=0, padx=20, pady=10)

        self.gauss_blur_slider = customtkinter.CTkSlider(self.tabview.tab('Enhance'), from_=0, to=10, number_of_steps=10, command=self.gauss_blur)
        self.gauss_blur_slider.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky='ew')
      
        self.color_label = customtkinter.CTkLabel(self.tabview.tab('Enhance'), text='Color')
        self.color_label.grid(row=4, column=0, padx=20, pady=10)

        self.color_slider = customtkinter.CTkSlider(self.tabview.tab('Enhance'), from_=0, to=5, number_of_steps=100, command=self.colour)
        self.color_slider.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky='ew')
       
        self.contrast_label = customtkinter.CTkLabel(self.tabview.tab('Enhance'), text='Contrast')
        self.contrast_label.grid(row=6, column=0, padx=20, pady=10)

        self.contrast_slider = customtkinter.CTkSlider(self.tabview.tab('Enhance'), from_=0, to=5, number_of_steps=100, command=self.contrast)
        self.contrast_slider.grid(row=7, column=0, padx=(10, 10), pady=(0, 10), sticky='ew')
       
        self.brightness_label = customtkinter.CTkLabel(self.tabview.tab('Enhance'), text='Brightness')
        self.brightness_label.grid(row=8, column=0, padx=20, pady=10)

        self.brightness_slider = customtkinter.CTkSlider(self.tabview.tab('Enhance'), from_=0, to=5, number_of_steps=100, command=self.brightness)
        self.brightness_slider.grid(row=9, column=0, padx=(10, 10), pady=(0, 10), sticky='ew')
       
        self.sharpness_label = customtkinter.CTkLabel(self.tabview.tab('Enhance'), text='Sharpness')
        self.sharpness_label.grid(row=10, column=0, padx=20, pady=10)

        self.sharpnes_slider = customtkinter.CTkSlider(self.tabview.tab('Enhance'), from_=0, to=5, number_of_steps=100, command=self.sharpness)
        self.sharpnes_slider.grid(row=11, column=0, padx=(10, 10), pady=(0, 10), sticky='ew')


        # create Pixabay API tab
        self.img_searchbox = customtkinter.CTkEntry(self.tabview.tab('Pixabay'))
        self.img_searchbox.grid(row=0, column=0, padx=5, pady=10, sticky='ew')

        self.img_search_button = customtkinter.CTkButton(self.tabview.tab('Pixabay'), text='Search', command=self.display_results)
        self.img_search_button.grid(row=0, column=1, padx=5, pady=10, sticky='ew')

        # create scroll frame to display search results
        self.images_scrollbar = customtkinter.CTkScrollableFrame(self.tabview.tab('Pixabay'))
        self.images_scrollbar.grid(row=1, column=0, padx=0, pady=0, columnspan=2, sticky='nsew')
        self.images_scrollbar.grid_columnconfigure((0, 1), weight=1)

        # credits to Pixabay
        self.pixabay_label = customtkinter.CTkLabel(self.tabview.tab('Pixabay'), text='Images downloaded from www.pixabay.com.')
        self.pixabay_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky='ew')
        
     
        # default values
        self.appearance_mode_optionemenu.set('Dark')
        self.scaling_optionemenu.set('100%')
        self.filters_option.set('NO FILTER')
        self.colors_option.set('None')


        # key binds
        self.bind('<Control-z>', lambda event: self.undo())
        self.bind('<Control-s>', lambda event: self.save_image_as())


        # create stack to keep a record of all changes
        self.all_saves = []

        # timeout for the sliders
        self.save_changes_timeout = None



    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace('%', '')) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        

    # resize image and display it on the canvas
    def display_image(self, edited_img):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # resize the image to fit the canvas
        self.image_width, self.image_height = self.edited_img.size
        self.width_scale = canvas_width / self.image_width
        self.height_scale = canvas_height / self.image_height
        self.scale = min(self.width_scale, self.height_scale)
        new_size = (self.image_width, self.image_height) = int(self.scale*self.image_width), int(self.scale*self.image_height)
        resized_img = edited_img.resize(new_size)
        
        # calculate the new coordinates to center the image
        self.image_x = (canvas_width - self.image_width) // 2
        self.image_y = (canvas_height - self.image_height) // 2

        # create and display the image on canvas
        self.displayed_img = ImageTk.PhotoImage(resized_img)
        self.canvas.create_image(self.image_x, self.image_y, anchor='nw', image=self.displayed_img)


    # load image from local storage
    def load_image(self):
        self.img_path = customtkinter.filedialog.askopenfilename(initialdir='', title='Select an image', filetypes=(('PNG files', '*.png'), ('JPG files', '*.jpg')))
        self.original_img = self.edited_img = Image.open(self.img_path)
        
        # append the history/undo list
        self.all_saves.append(self.edited_img)

        # clear the canvas
        self.canvas.delete('all')

        # update the image path
        self.path_label.configure(text=self.img_path)

        return self.display_image(self.edited_img)


    # save the current image as
    def save_image_as(self):
        save_path = customtkinter.filedialog.asksaveasfilename(initialdir='', title='Save location', filetypes=(('PNG files', '*.png'), ('JPG files', '*.jpg')))
        self.edited_img.save(save_path)
        
        # update image path
        self.path_label.configure(text=save_path)
        self.img_path = save_path


    # save the current image button
    def save_image(self):
        self.edited_img.save(self.img_path)


    # save the changes to the image and append the history/undo list
    def _save_changes(self):
        self.all_saves.append(self.edited_img)
        self.original_img = self.edited_img


    # undo function, goes back to last change in image
    def undo(self):
        if len(self.all_saves) > 1:
            self.all_saves.pop()
            self.edited_img = self.original_img = self.all_saves[-1]
            self.display_image(self.edited_img)
        else:
            self.canvas.delete('all')
            self.path_label.configure(text='')
            
        
    # add filter to the image
    def filter_selected(self, filter):
        if filter == 'Blur':
            self.edited_img = self.original_img.filter(ImageFilter.BLUR)
        elif filter == 'Contour':
            self.edited_img = self.original_img.filter(ImageFilter.CONTOUR)
        elif filter == 'Detail':
            self.edited_img = self.original_img.filter(ImageFilter.DETAIL)
        elif filter == 'Edge Enhance':
            self.edited_img = self.original_img.filter(ImageFilter.EDGE_ENHANCE)
        elif filter == 'Emboss':
            self.edited_img = self.original_img.filter(ImageFilter.EMBOSS)
        elif filter == 'Sharpen':
            self.edited_img = self.original_img.filter(ImageFilter.SHARPEN)
        elif filter == 'Smooth':
            self.edited_img = self.original_img.filter(ImageFilter.SMOOTH)
        elif filter == 'None':
            self.edited_img = self.original_img
        
        self._save_changes()
        return self.display_image(self.edited_img)
    
    # change the color scheme of the image
    def colour_selected(self, colour):
        if colour == 'Black and White':
            self.edited_img = ImageOps.grayscale(self.original_img)
        elif colour == 'Invert':
            self.edited_img = ImageOps.invert(self.original_img)
        elif colour == 'Equalize':
            self.edited_img = ImageOps.equalize(self.original_img)
        elif colour == 'None':
            self.edited_img = self.original_img

        self._save_changes()
        return self.display_image(self.edited_img)
    

    # function to flip image vertically
    def flip_image(self):
        self.edited_img = ImageOps.flip(self.original_img)
        self._save_changes()
        return self.display_image(self.edited_img)
    

    # function to flip/mirror image horizontally
    def mirror_image(self):
        self.edited_img = ImageOps.mirror(self.original_img)
        self._save_changes()
        return self.display_image(self.edited_img)
    
    # save changes after you leave the slider
    def _changes_timeout(self):
        # cancel any existing timeout
        if self.save_changes_timeout is not None:
            self.after_cancel(self.save_changes_timeout)

        # start a new timeout after moving the slider
        self.save_changes_timeout = self.after(500, self._save_changes)

    
    # enhancement sliders
    def box_blur(self, radius):
        self._changes_timeout()
        self.edited_img = self.original_img.filter(ImageFilter.BoxBlur(radius))
        return self.display_image(self.edited_img)
    
    def gauss_blur(self, radius):
        self._changes_timeout()

        self.edited_img = self.original_img.filter(ImageFilter.GaussianBlur(radius))
        return self.display_image(self.edited_img)
    
    def colour(self, factor):
        self._changes_timeout()
        enhancer = ImageEnhance.Color(self.original_img)
        self.edited_img = enhancer.enhance(factor)
        return self.display_image(self.edited_img)
    
    def contrast(self, factor):
        self._changes_timeout()

        enhancer = ImageEnhance.Contrast(self.original_img)
        self.edited_img = enhancer.enhance(factor)
        return self.display_image(self.edited_img)

    def sharpness(self, factor):
        self._changes_timeout()
        enhancer = ImageEnhance.Sharpness(self.original_img)
        self.edited_img = enhancer.enhance(factor)
        return self.display_image(self.edited_img)

    def brightness(self, factor):
        self._changes_timeout()
        enhancer = ImageEnhance.Brightness(self.original_img)
        self.edited_img = enhancer.enhance(factor)
        return self.display_image(self.edited_img)
    

    # searches images in cache if not availble gets them from pixabay
    def _search_images(self):

        # save the paths of all the downloaded previews
        downloaded_images = []

        # save the full image links of all previews
        download_links = []

        self.image_query = self.img_searchbox.get()

        # check for the query in local cache
        check_cache = self.cache.retrieve_data(self.image_query)
        
        if check_cache:
            downloaded_images = check_cache[0]
            download_links = check_cache[1]

        else:
            # get the api key from .env and search pixabay for the query
            px = pixabay.core(os.getenv('PIXABAY_API_KEY'))
            results = px.query(self.image_query)

            dir_path = os.path.join('cache_data', self.image_query)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            # save the urls of first 50 results
            query_results = []
            for i in range(50):
                query_results.append(results[i])

            # download thumbnails and save their filepaths to downloaded_images list and their fullHD urls to download_links
            for i, url in enumerate(query_results):
                try:
                    response = requests.get(url.getPreviewURL())

                    if response.status_code == 200:
                        image_path = os.path.join('cache_data', self.image_query, f'image_{i}.jpg')

                        with open(image_path, 'wb') as f:
                            f.write(response.content)

                        # append downloaded_images
                        downloaded_images.append(image_path)
                        print(f'Image {i} downloaded successfully.')

                        # append download_linkd
                        download_link = url.getLargeImageURL()
                        download_links.append(download_link)
                    
                    else:
                        print(f'Failed to download Image {i}. Status code: {response.status_code}')
                except Exception as e:
                    print(f'Error downloading Image {i}: {e}')
            
        # store the filepaths an full image links to cache for 24 hours
        self.cache.store_data_in_cache(self.image_query, downloaded_images, download_links)
        self.cache.remove_old_data()

        return [downloaded_images, download_links]


    # implement Pixabay API to search for images using keywords and import them into the application.
    def display_results(self):

        downloaded_images, download_links = self._search_images()

        # destroy all existing buttons from the scroll frame
        for widget in self.images_scrollbar.winfo_children():
            widget.destroy()

        for i in range(len(downloaded_images)):
            image_obj = ImageTk.PhotoImage(Image.open(downloaded_images[i]))

            # display the images as buttons
            self.image_preview = customtkinter.CTkButton(self.images_scrollbar, text='', image=image_obj, border_width=0, command=lambda link=download_links[i]: self.open_web_image(link))
            self.image_preview.grid(row=i//2, column=i%2)


    # download and load the image on canvas when the button is clicked
    def open_web_image(self, event):

        # download the full image
        response = requests.get(event)
        if response.status_code == 200:
            with open(f'{self.image_query}.jpg', 'wb') as f:
                f.write(response.content)

            # load the image onto the canvas
            image_obj = Image.open(f'{self.image_query}.jpg')
            self.edited_img = image_obj
            self._save_changes()
            self.display_image(self.edited_img) 

            # update the file path label at the bottom of the window
            self.img_path = os.path.abspath(f'{self.image_query}.jpg')
            self.path_label.configure(text=f'{self.img_path} - Image downloaded from Pixabay')

            # remove the image from the local storage
            os.remove(f'{self.image_query}.jpg')

        else:
            print(f'Failed to download Image. Status code: {response.status_code}')


# run the app
if __name__ == '__main__':
    app = App()
    app.mainloop()
